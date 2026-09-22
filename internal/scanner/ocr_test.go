package scanner

import (
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
