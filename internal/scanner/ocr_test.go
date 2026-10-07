package scanner

import (
	"image"
	"image/color"
	"image/png"
	"os"
	"strings"
	"testing"
)

func TestOCRPatterns(t *testing.T) {
	testCases := []struct {
		name        string
		input       string
		expectedRule string
	}{
		{
			name:        "API Key assignment",
			input:       "API_KEY = sk-live-998877665544332211aabbcc",
			expectedRule: "TG-SEC-001",
		},
		{
			name:        "Direct OpenAI key",
			input:       "Found key sk-1234567890abcdef1234567890abcdef in header",
			expectedRule: "TG-SEC-001",
		},
		{
			name:        "AWS Access Key",
			input:       "AWS_ACCESS_KEY_ID: AKIAIOSFODNN7EXAMPLE",
			expectedRule: "TG-SEC-002",
		},
		{
			name:        "GitHub PAT",
			input:       "token = ghp_0123456789abcdefghijklmnopqrstuvwxyz",
			expectedRule: "TG-SEC-003",
		},
		{
			name:        "Postgres Database URI",
			input:       "DATABASE_URL: postgres://root:p@ssw0rd123@db.prod.internal:5432/app",
			expectedRule: "TG-SEC-004",
		},
		{
			name:        "Private Key Header",
			input:       "-----BEGIN RSA PRIVATE KEY-----",
			expectedRule: "TG-SEC-005",
		},
		{
			name:        "Password assignment",
			input:       "password = \"UltraSecretP@ssword2026!\"",
			expectedRule: "TG-SEC-007",
		},
	}

	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			matched := false
			for _, p := range OCRPatterns {
				if p.RuleID == tc.expectedRule && p.Regex.MatchString(tc.input) {
					matched = true
					break
				}
			}
			if !matched {
				t.Errorf("Expected pattern %s to match input: %s", tc.expectedRule, tc.input)
			}
		})
	}
}

func TestImageExtensionFilter(t *testing.T) {
	valid := []string{".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tiff"}
	invalid := []string{".go", ".py", ".exe", ".sh", ".md", ".json"}

	for _, ext := range valid {
		if !ImageExtensions[ext] {
			t.Errorf("Expected %s to be recognized as supported image format", ext)
		}
	}

	for _, ext := range invalid {
		if ImageExtensions[ext] {
			t.Errorf("Expected %s to NOT be recognized as image format", ext)
		}
	}
}

func TestMaxImageSizeInvariant(t *testing.T) {
	if DefaultMaxImageSize < 5*1024*1024 || DefaultMaxImageSize > 10*1024*1024 {
		t.Errorf("DefaultMaxImageSize (%d) must remain between 5MB and 10MB bounds", DefaultMaxImageSize)
	}
}

func TestExtractEmbeddedText(t *testing.T) {
	// Create temporary SVG with secret
	tmpDir := t.TempDir()
	svgPath := tmpDir + "/test_arch.svg"
	secretContent := `<svg><text>DATABASE_URL: postgres://admin:secretPass123@db.prod.internal:5432/db</text></svg>`
	if err := os.WriteFile(svgPath, []byte(secretContent), 0644); err != nil {
		t.Fatalf("Failed to create test SVG: %v", err)
	}

	extracted, err := ExtractEmbeddedText(svgPath, DefaultMaxImageSize)
	if err != nil {
		t.Fatalf("ExtractEmbeddedText failed on SVG: %v", err)
	}

	if !strings.Contains(extracted, "secretPass123") {
		t.Errorf("Expected extracted text to contain secret, got: %s", extracted)
	}

	// Test ScanImageFile with empty tesseractPath (pure first-principles mode)
	findings, err := ScanImageFile(svgPath, "", DefaultMaxImageSize)
	if err != nil {
		t.Fatalf("ScanImageFile failed in first-principles mode: %v", err)
	}
	if len(findings) == 0 {
		t.Errorf("Expected findings from SVG with database URI, got 0")
	}
}

func TestFindWorkspaceImages(t *testing.T) {
	tmpDir := t.TempDir()
	_ = os.WriteFile(tmpDir+"/arch.png", []byte("\x89PNG\r\n\x1a\n"), 0644)
	_ = os.WriteFile(tmpDir+"/flow.svg", []byte("<svg></svg>"), 0644)
	_ = os.WriteFile(tmpDir+"/readme.txt", []byte("ignore"), 0644)

	images, err := FindWorkspaceImages(tmpDir)
	if err != nil {
		t.Fatalf("FindWorkspaceImages failed: %v", err)
	}
	if len(images) != 2 {
		t.Errorf("Expected 2 images, found %d: %v", len(images), images)
	}
}

func TestEnhanceImageContrast(t *testing.T) {
	tmpDir := t.TempDir()
	testImgPath := tmpDir + "/low_contrast.png"

	// Create synthetic low-contrast raster image
	bounds := image.Rect(0, 0, 100, 100)
	img := image.NewRGBA(bounds)
	for y := 0; y < 100; y++ {
		for x := 0; x < 100; x++ {
			if x > 40 && x < 60 && y > 40 && y < 60 {
				// Faint foreground
				img.Set(x, y, color.RGBA{R: 140, G: 140, B: 140, A: 255})
			} else {
				// Faint background
				img.Set(x, y, color.RGBA{R: 110, G: 110, B: 110, A: 255})
			}
		}
	}

	f, err := os.Create(testImgPath)
	if err != nil {
		t.Fatalf("failed to create test image: %v", err)
	}
	if err := png.Encode(f, img); err != nil {
		f.Close()
		t.Fatalf("failed to encode PNG: %v", err)
	}
	f.Close()

	enhancedPath, cleanup, err := EnhanceImageContrast(testImgPath)
	if err != nil {
		t.Fatalf("EnhanceImageContrast failed: %v", err)
	}
	if _, err := os.Stat(enhancedPath); err != nil {
		t.Errorf("enhanced image file does not exist: %v", err)
	}

	cleanup()
	if _, err := os.Stat(enhancedPath); !os.IsNotExist(err) {
		t.Errorf("expected enhanced image to be removed by cleanup, but still exists")
	}
}


