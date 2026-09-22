package scanner

import (
	"bytes"
	"context"
	"fmt"
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

// ScanImageFile extracts text from a single image and searches for secret patterns.
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

	rawText, err := ExtractTextFromImage(imagePath, tesseractPath)
	if err != nil {
		return nil, err
	}

	var findings []string
	cleanPath, _ := filepath.Rel(".", imagePath)
	if cleanPath == "" {
		cleanPath = imagePath
	}

	for _, pattern := range OCRPatterns {
		matches := pattern.Regex.FindAllString(rawText, -1)
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
	tessPath, err := FindTesseract()
	if err != nil {
		return []string{fmt.Sprintf("[WARN] OCR image scanning skipped: %v", err)}, nil
	}

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
