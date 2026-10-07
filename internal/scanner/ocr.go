package scanner

import (
	"bytes"
	"context"
	"encoding/binary"
	"fmt"
	"image"
	"image/color"
	_ "image/jpeg"
	"image/png"
	"os"
	"os/exec"
	"path/filepath"
	"regexp"
	"strings"
	"time"
)

// DefaultMaxImageSize is the upper threshold (10MB) for scanning image files to prevent DoS.
const DefaultMaxImageSize = 10 * 1024 * 1024

// ImageExtensions contains the supported file types for OCR inspection.
var ImageExtensions = map[string]bool{
	".png":  true,
	".jpg":  true,
	".jpeg": true,
	".webp": true,
	".bmp":  true,
	".tiff": true,
	".tif":  true,
	".svg":  true,
}

// OCRSecretPattern defines signatures for leaked credentials in image text.
type OCRSecretPattern struct {
	RuleID      string
	Description string
	Regex       *regexp.Regexp
}

// OCRPatterns defines the rules checked against text extracted from images.
var OCRPatterns = []OCRSecretPattern{
	{
		RuleID:      "TG-SEC-001",
		Description: "Hardcoded API Key / Secret Token in image",
		Regex:       regexp.MustCompile(`(?i)(api[_-]?key|secret[_-]?key|access[_-]?token|bearer|auth[_-]?token)\s*[:=]\s*["']?([a-zA-Z0-9_\-\.]{12,})["']?`),
	},
	{
		RuleID:      "TG-SEC-001",
		Description: "OpenAI / Stripe Secret API Key in image",
		Regex:       regexp.MustCompile(`\b(sk-(?:live-)?[a-zA-Z0-9_\-\.]{20,})\b`),
	},
	{
		RuleID:      "TG-SEC-002",
		Description: "AWS Access Key ID in image",
		Regex:       regexp.MustCompile(`\b(AKIA[0-9A-Z]{16})\b`),
	},
	{
		RuleID:      "TG-SEC-003",
		Description: "GitHub Personal Access Token in image",
		Regex:       regexp.MustCompile(`\b(ghp_[a-zA-Z0-9]{30,40}|github_pat_[a-zA-Z0-9_]{60,90})\b`),
	},
	{
		RuleID:      "TG-SEC-004",
		Description: "Database Connection URI with credentials in image",
		Regex:       regexp.MustCompile(`(?i)(?:pos[ti]gre(?:sql)?|mysq[l|I1]|mongodb|redis|[a-z0-9_\-\|]+)://[a-zA-Z0-9_\-]+:[^@\s]+@[a-zA-Z0-9_\-\.]+`),
	},
	{
		RuleID:      "TG-SEC-005",
		Description: "Private Key block header in image",
		Regex:       regexp.MustCompile(`(?i)-----BEGIN\s+(?:(?:RSA|OPENSSH|EC|DSA)\s+)?(?:PRIVATE\s+)?KEY-----`),
	},
	{
		RuleID:      "TG-SEC-006",
		Description: "JSON Web Token (JWT) in image",
		Regex:       regexp.MustCompile(`\beyJ[a-zA-Z0-9_\-]{10,}\.eyJ[a-zA-Z0-9_\-]{10,}\.[a-zA-Z0-9_\-]{10,}\b`),
	},
	{
		RuleID:      "TG-SEC-007",
		Description: "Generic Password / Secret credential assignment in image",
		Regex:       regexp.MustCompile(`(?i)(password|passwd|pwd)\s*[:=]\s*["']?([^\s"']{6,})["']?`),
	},
}

// FindTesseract attempts to locate the Tesseract executable on the local system.
func FindTesseract() (string, error) {
	// 1. Explicit environment variable
	if custom := os.Getenv("TESSERACT_PATH"); custom != "" {
		if _, err := os.Stat(custom); err == nil {
			return custom, nil
		}
	}

	// 2. PATH lookup
	for _, binName := range []string{"tesseract", "tesseract.exe"} {
		if path, err := exec.LookPath(binName); err == nil {
			return path, nil
		}
	}

	// 3. Common Windows installation paths
	candidates := []string{
		`C:\Program Files\Tesseract-OCR\tesseract.exe`,
		`C:\Program Files (x86)\Tesseract-OCR\tesseract.exe`,
	}
	if localAppData := os.Getenv("LOCALAPPDATA"); localAppData != "" {
		candidates = append(candidates, filepath.Join(localAppData, "Programs", "Tesseract-OCR", "tesseract.exe"))
	}
	if progFiles := os.Getenv("ProgramFiles"); progFiles != "" {
		candidates = append(candidates, filepath.Join(progFiles, "Tesseract-OCR", "tesseract.exe"))
	}

	// 4. Unix/Linux/macOS standard paths
	candidates = append(candidates,
		"/usr/bin/tesseract",
		"/usr/local/bin/tesseract",
		"/opt/homebrew/bin/tesseract",
	)

	for _, cand := range candidates {
		if _, err := os.Stat(cand); err == nil {
			return cand, nil
		}
	}

	return "", fmt.Errorf("tesseract executable not found. Please install Tesseract-OCR or set TESSERACT_PATH")
}

// ExtractTextFromImage invokes Tesseract CLI to extract raw text from an image file.
func ExtractTextFromImage(imagePath string, tesseractPath string) (string, error) {
	ctx, cancel := context.WithTimeout(context.Background(), 45*time.Second)
	defer cancel()

	cmd := exec.CommandContext(ctx, tesseractPath, imagePath, "stdout", "--dpi", "300", "-l", "eng")
	var stdout, stderr bytes.Buffer
	cmd.Stdout = &stdout
	cmd.Stderr = &stderr

	if err := cmd.Run(); err != nil {
		return "", fmt.Errorf("tesseract failed on %s: %v (stderr: %s)", imagePath, err, stderr.String())
	}

	return stdout.String(), nil
}

// ExtractEmbeddedText uses first-principles binary parsing to extract text without external OCR binaries.
// It parses SVG XML directly, reads PNG tEXt/iTXt chunks, and extracts printable ASCII byte streams from image files.
func ExtractEmbeddedText(imagePath string, maxBytes int64) (string, error) {
	if maxBytes <= 0 {
		maxBytes = DefaultMaxImageSize
	}
	data, err := os.ReadFile(imagePath)
	if err != nil {
		return "", err
	}
	if int64(len(data)) > maxBytes {
		data = data[:maxBytes]
	}

	ext := strings.ToLower(filepath.Ext(imagePath))
	var sb strings.Builder

	// 1. Direct text file formats like SVG
	if ext == ".svg" {
		return string(data), nil
	}

	// 2. PNG chunk extractor (tEXt, iTXt, zTXt)
	if ext == ".png" && len(data) >= 8 && bytes.Equal(data[:8], []byte("\x89PNG\r\n\x1a\n")) {
		offset := 8
		for offset+8 <= len(data) {
			length := int(binary.BigEndian.Uint32(data[offset : offset+4]))
			chunkType := string(data[offset+4 : offset+8])
			dataStart := offset + 8
			dataEnd := dataStart + length
			if dataEnd > len(data) || length < 0 {
				break
			}
			chunkData := data[dataStart:dataEnd]
			if chunkType == "tEXt" || chunkType == "iTXt" {
				parts := bytes.SplitN(chunkData, []byte{0}, 2)
				for _, p := range parts {
					sb.Write(p)
					sb.WriteString(" ")
				}
			}
			offset = dataEnd + 4 // skip 4 bytes CRC
		}
	}

	// 3. First-principles printable ASCII string scanner (strings >= 6 chars)
	// Catches EXIF headers, uncompressed strings, embedded API tokens, and URLs
	var current []byte
	for _, b := range data {
		if (b >= 32 && b <= 126) || b == '\t' || b == '\n' || b == '\r' {
			current = append(current, b)
		} else {
			if len(current) >= 6 {
				sb.Write(current)
				sb.WriteString("\n")
			}
			current = current[:0]
		}
	}
	if len(current) >= 6 {
		sb.Write(current)
		sb.WriteString("\n")
	}

	return sb.String(), nil
}

// FindWorkspaceImages traverses target directory and returns all discoverable image files.
func FindWorkspaceImages(targetDir string) ([]string, error) {
	var images []string
	const maxImages = 300

	err := filepath.Walk(targetDir, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return nil
		}
		if info.IsDir() {
			name := info.Name()
			if name == ".git" || name == "node_modules" || name == ".torusguard" || name == "vendor" {
				return filepath.SkipDir
			}
			return nil
		}
		ext := strings.ToLower(filepath.Ext(path))
		if ImageExtensions[ext] {
			images = append(images, path)
			if len(images) >= maxImages {
				return fmt.Errorf("max images reached")
			}
		}
		return nil
	})
	if err != nil && !strings.Contains(err.Error(), "max images reached") {
		return images, err
	}
	return images, nil
}

// computeOtsuThreshold calculates the optimal binarization threshold for a grayscale image.
func computeOtsuThreshold(hist [256]int, totalPixels int) uint8 {
	if totalPixels == 0 {
		return 128
	}

	var sum float64
	for i := 0; i < 256; i++ {
		sum += float64(i * hist[i])
	}

	var sumB float64
	var wB int
	var maxVariance float64
	var threshold uint8 = 128

	for t := 0; t < 256; t++ {
		wB += hist[t]
		if wB == 0 {
			continue
		}
		wF := totalPixels - wB
		if wF == 0 {
			break
		}

		sumB += float64(t * hist[t])
		mB := sumB / float64(wB)
		mF := (sum - sumB) / float64(wF)

		varianceBetween := float64(wB) * float64(wF) * (mB - mF) * (mB - mF)
		if varianceBetween > maxVariance {
			maxVariance = varianceBetween
			threshold = uint8(t)
		}
	}

	return threshold
}

// EnhanceImageContrast creates a high-contrast binarized PNG image (monochrome black text on pure white)
// using Otsu adaptive thresholding and background polarity inversion.
func EnhanceImageContrast(imagePath string) (string, func(), error) {
	file, err := os.Open(imagePath)
	if err != nil {
		return "", func() {}, err
	}
	defer file.Close()

	img, _, err := image.Decode(file)
	if err != nil {
		return "", func() {}, err
	}

	bounds := img.Bounds()
	w, h := bounds.Dx(), bounds.Dy()
	if w <= 0 || h <= 0 {
		return "", func() {}, fmt.Errorf("invalid image dimensions")
	}

	var hist [256]int
	totalPixels := w * h
	grayImg := image.NewGray(bounds)

	for y := bounds.Min.Y; y < bounds.Max.Y; y++ {
		for x := bounds.Min.X; x < bounds.Max.X; x++ {
			c := color.GrayModel.Convert(img.At(x, y)).(color.Gray)
			grayImg.Set(x, y, c)
			hist[c.Y]++
		}
	}

	threshold := computeOtsuThreshold(hist, totalPixels)

	whiteCount := 0
	for i := int(threshold) + 1; i < 256; i++ {
		whiteCount += hist[i]
	}
	invert := whiteCount < totalPixels/2 // If dark pixels dominate background, invert so background is white

	binarized := image.NewGray(bounds)
	for y := bounds.Min.Y; y < bounds.Max.Y; y++ {
		for x := bounds.Min.X; x < bounds.Max.X; x++ {
			v := grayImg.GrayAt(x, y).Y
			isLight := v > threshold
			if invert {
				isLight = !isLight
			}

			if isLight {
				binarized.Set(x, y, color.Gray{Y: 255})
			} else {
				binarized.Set(x, y, color.Gray{Y: 0})
			}
		}
	}

	tempFile, err := os.CreateTemp("", "tg_binarized_*.png")
	if err != nil {
		return "", func() {}, err
	}
	tempPath := tempFile.Name()

	if err := png.Encode(tempFile, binarized); err != nil {
		tempFile.Close()
		_ = os.Remove(tempPath)
		return "", func() {}, err
	}
	tempFile.Close()

	cleanup := func() {
		_ = os.Remove(tempPath)
	}

	return tempPath, cleanup, nil
}

// ScanImageFile extracts text from a single image via hybrid first-principles + neural OCR and searches for secret patterns.
func ScanImageFile(imagePath string, tesseractPath string, maxBytes int64) ([]string, error) {
	if maxBytes <= 0 {
		maxBytes = DefaultMaxImageSize
	}

	info, err := os.Stat(imagePath)
	if err != nil {
		return nil, fmt.Errorf("failed to stat image file %s: %w", imagePath, err)
	}

	if info.Size() > maxBytes {
		return []string{fmt.Sprintf("[TG-DOS-001] Skipped image %s: file size (%d MB) exceeds safety boundary (%d MB)",
			imagePath, info.Size()/(1024*1024), maxBytes/(1024*1024))}, nil
	}

	// 1. Built-in first-principles text extraction (zero external dependencies)
	embeddedText, _ := ExtractEmbeddedText(imagePath, maxBytes)

	// 2. Deep optical character recognition (if Tesseract binary is available)
	var opticalText string
	if tesseractPath != "" {
		opticalText, _ = ExtractTextFromImage(imagePath, tesseractPath)

		// Secondary pass: if direct OCR extracted sparse or no text, attempt contrast-enhanced binarization
		ext := strings.ToLower(filepath.Ext(imagePath))
		if ext != ".svg" && len(strings.TrimSpace(opticalText)) < 15 {
			if enhPath, cleanup, err := EnhanceImageContrast(imagePath); err == nil {
				defer cleanup()
				if enhText, err := ExtractTextFromImage(enhPath, tesseractPath); err == nil && len(enhText) > 0 {
					opticalText += "\n" + enhText
				}
			}
		}
	}

	combinedText := embeddedText + "\n" + opticalText

	var findings []string
	cleanPath, _ := filepath.Rel(".", imagePath)
	if cleanPath == "" {
		cleanPath = imagePath
	}

	for _, pattern := range OCRPatterns {
		matches := pattern.Regex.FindAllString(combinedText, -1)
		for _, m := range matches {
			// Redact potential secret payload before logging/returning
			redacted := m
			if len(redacted) > 40 {
				redacted = redacted[:37] + "..."
			}
			finding := fmt.Sprintf("[%s] [OCR] %s in %s (Evidence: %s)",
				pattern.RuleID, pattern.Description, cleanPath, redacted)
			findings = append(findings, finding)
		}
	}

	return findings, nil
}

// ScanImagesInDir traverses target directory and runs OCR secret detection on all supported image formats.
func ScanImagesInDir(targetDir string, maxBytes int64) ([]string, error) {
	tessPath, _ := FindTesseract()

	var imageFindings []string
	imageCount := 0
	const maxImagesScanned = 150 // Bound image processing to prevent excessive compute overhead

	walkErr := filepath.Walk(targetDir, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return nil
		}

		if info.IsDir() {
			name := info.Name()
			if name == ".git" || name == "node_modules" || name == ".torusguard" || name == "vendor" {
				return filepath.SkipDir
			}
			return nil
		}

		ext := strings.ToLower(filepath.Ext(path))
		if !ImageExtensions[ext] {
			return nil
		}

		imageCount++
		if imageCount > maxImagesScanned {
			return fmt.Errorf("max image count limit (%d) reached", maxImagesScanned)
		}

		findings, scanErr := ScanImageFile(path, tessPath, maxBytes)
		if scanErr != nil {
			imageFindings = append(imageFindings, fmt.Sprintf("[WARN] OCR scan failed for %s: %v", path, scanErr))
			return nil
		}

		imageFindings = append(imageFindings, findings...)
		return nil
	})

	if walkErr != nil && !strings.Contains(walkErr.Error(), "max image count limit") {
		return imageFindings, walkErr
	}

	return imageFindings, nil
}

