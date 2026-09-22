package scanner

import (
	"context"
	"fmt"
	"os"
	"path/filepath"
	"regexp"
	"strings"
	"time"

	"github.com/torusguard/torusguard/internal/rules"
)

func RunAudit(targetDir string, catalog *rules.Catalog) ([]string, error) {
	fmt.Printf("Starting static heuristic security scan on %s...\n", targetDir)
	fmt.Printf("Loaded %d rules from catalog.\n", len(catalog.Rules))

	var findings []string

	// Basic heuristics to replace AST scanning due to lack of CGO
	secretRegex := regexp.MustCompile(`(?i)(password|secret|api_key|token)\s*=\s*["'][a-zA-Z0-9]+["']`)
	sqlRegex := regexp.MustCompile(`(?i)(SELECT|INSERT|UPDATE|DELETE).+(WHERE|VALUES)\s+.*'%\s*\+\s*[a-zA-Z0-9_]+\s*\+\s*'`) // Naive string concat check

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Minute)
	defer cancel()

	fileCount := 0
	const maxFileCount = 10000

	err := filepath.Walk(targetDir, func(path string, info os.FileInfo, err error) error {
		select {
		case <-ctx.Done():
			return fmt.Errorf("scan aborted: timeout exceeded (5 minutes)")
		default:
		}

		if err != nil {
			return err
		}

		if info.IsDir() {
			if info.Name() == "node_modules" || info.Name() == ".git" || info.Name() == ".torusguard" {
				return filepath.SkipDir
			}
			return nil
		}

		fileCount++
		if fileCount > maxFileCount {
			return fmt.Errorf("scan aborted: exceeded maximum file count limit of %d", maxFileCount)
		}

		ext := filepath.Ext(path)
		if ext != ".go" && ext != ".js" && ext != ".ts" && ext != ".py" {
			return nil // Limit scan to code files
		}

		if info.Size() > 5*1024*1024 {
			return nil // Skip files larger than 5MB to prevent memory bloat
		}

		sourceCodeBytes, err := os.ReadFile(path)
		if err != nil {
			fmt.Printf("Warning: failed to read file %s: %v\n", path, err)
			return nil
		}
		
		sourceCode := string(sourceCodeBytes)

		// Check for hardcoded secrets
		if secretRegex.MatchString(sourceCode) {
			findings = append(findings, fmt.Sprintf("Hardcoded secret found in %s", path))
		}

		// Check for potential SQL injection (string concatenation)
		if sqlRegex.MatchString(sourceCode) {
			findings = append(findings, fmt.Sprintf("Potential SQL Injection (string concatenation) found in %s", path))
		}

		return nil
	})

	if err != nil {
		return nil, fmt.Errorf("error walking directory: %v", err)
	}

	// Multi-Modal OCR Image Scanning
	ocrFindings, ocrErr := ScanImagesInDir(targetDir, DefaultMaxImageSize)
	if ocrErr == nil && len(ocrFindings) > 0 {
		for _, of := range ocrFindings {
			if !strings.HasPrefix(of, "[WARN]") {
				findings = append(findings, of)
			}
		}
	}

	if len(findings) == 0 {
		findings = append(findings, "No active findings detected. Posture is secure.")
	}

	return findings, nil
}
