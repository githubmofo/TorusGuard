package harden

import (
	"os"
	"path/filepath"
	"strings"
	"testing"
)

func TestReflectAndVerifySuccess(t *testing.T) {
	tempDir := t.TempDir()
	targetFile := filepath.Join(tempDir, "server.go")
	initialContent := `package main

import "fmt"

func main() {
	secret := "hardcoded-secret-token-1234"
	fmt.Println(secret)
}
`
	if err := os.WriteFile(targetFile, []byte(initialContent), 0644); err != nil {
		t.Fatalf("Failed to write initial file: %v", err)
	}

	patch := SemanticPatch{
		TargetFile:     "server.go",
		RuleID:         "TG-SEC-001",
		FindSnippet:    `secret := "hardcoded-secret-token-1234"`,
		ReplaceSnippet: `secret := os.Getenv("APP_SECRET")`,
		Rationale:      "Extract hardcoded secret to environment variable",
	}

	match, err := ReflectAndVerify(targetFile, patch)
	if err != nil {
		t.Fatalf("ReflectAndVerify failed: %v", err)
	}

	if match.MatchedLineStart != 6 {
		t.Errorf("Expected match start line 6, got %d", match.MatchedLineStart)
	}
	if match.Additions != 1 || match.Deletions != 1 {
		t.Errorf("Expected 1 addition and 1 deletion, got +%d/-%d", match.Additions, match.Deletions)
	}
	if !strings.Contains(match.NewContent, `secret := os.Getenv("APP_SECRET")`) {
		t.Errorf("New content does not contain replacement: %s", match.NewContent)
	}
}

func TestReflectAndVerifyBypassRejection(t *testing.T) {
	tempDir := t.TempDir()
	targetFile := filepath.Join(tempDir, "server.go")
	initialContent := `package main

func check() {}
`
	if err := os.WriteFile(targetFile, []byte(initialContent), 0644); err != nil {
		t.Fatalf("Failed to write initial file: %v", err)
	}

	patch := SemanticPatch{
		TargetFile:     "server.go",
		RuleID:         "TG-DIFF-001",
		FindSnippet:    "func check() {}",
		ReplaceSnippet: "func check() {} // # nosec",
	}

	_, err := ReflectAndVerify(targetFile, patch)
	if err == nil {
		t.Fatalf("Expected ReflectAndVerify to reject security bypass (# nosec), but it succeeded")
	}
	if !strings.Contains(err.Error(), "security bypass detected") {
		t.Errorf("Unexpected error message: %v", err)
	}
}

func TestReflectAndVerifyPonytailBounds(t *testing.T) {
	tempDir := t.TempDir()
	targetFile := filepath.Join(tempDir, "server.go")
	initialContent := `package main
func check() {}
`
	if err := os.WriteFile(targetFile, []byte(initialContent), 0644); err != nil {
		t.Fatalf("Failed to write initial file: %v", err)
	}

	var excessiveLines []string
	for i := 0; i < 40; i++ {
		excessiveLines = append(excessiveLines, "println(\"line\")")
	}

	patch := SemanticPatch{
		TargetFile:     "server.go",
		FindSnippet:    "func check() {}",
		ReplaceSnippet: strings.Join(excessiveLines, "\n"),
	}

	_, err := ReflectAndVerify(targetFile, patch)
	if err == nil {
		t.Fatalf("Expected ReflectAndVerify to fail with Ponytail violation (>35 additions)")
	}
	if !strings.Contains(err.Error(), "violates Ponytail bounds") {
		t.Errorf("Unexpected error message: %v", err)
	}
}
