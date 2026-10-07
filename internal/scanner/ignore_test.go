package scanner

import (
	"os"
	"path/filepath"
	"testing"
)

func TestIgnoreEngineFileAndRuleGlobs(t *testing.T) {
	tmpDir := t.TempDir()
	ignoreContent := `# Ignore entire mock folder
tests/mocks/**
*.mock.ts
**/legacy/*

# Rule-scoped suppressions
TG-SEC-001: fixtures/dummy_keys.py
TG-DB-001: internal/testdb/*
`
	err := os.WriteFile(filepath.Join(tmpDir, ".torusguardignore"), []byte(ignoreContent), 0644)
	if err != nil {
		t.Fatalf("failed to write ignore file: %v", err)
	}

	engine := LoadIgnoreEngine(tmpDir)

	// Test global file ignore
	if !engine.ShouldIgnoreFile("tests/mocks/auth.py") {
		t.Errorf("expected tests/mocks/auth.py to be ignored")
	}
	if !engine.ShouldIgnoreFile("src/services/user.mock.ts") {
		t.Errorf("expected src/services/user.mock.ts to be ignored")
	}
	if !engine.ShouldIgnoreFile("pkg/legacy/old.go") {
		t.Errorf("expected pkg/legacy/old.go to be ignored")
	}
	if engine.ShouldIgnoreFile("src/controllers/user.ts") {
		t.Errorf("expected src/controllers/user.ts NOT to be ignored")
	}

	// Test rule-scoped file ignore
	if !engine.ShouldIgnoreRuleForFile("TG-SEC-001", "fixtures/dummy_keys.py") {
		t.Errorf("expected TG-SEC-001 to be ignored in fixtures/dummy_keys.py")
	}
	if engine.ShouldIgnoreRuleForFile("TG-SEC-002", "fixtures/dummy_keys.py") {
		t.Errorf("expected TG-SEC-002 NOT to be ignored in fixtures/dummy_keys.py")
	}
	if !engine.ShouldIgnoreRuleForFile("TG-DB-001", "internal/testdb/repo.go") {
		t.Errorf("expected TG-DB-001 to be ignored in internal/testdb/repo.go")
	}
}

func TestIgnoreEngineInlineAndBlockComments(t *testing.T) {
	engine := NewIgnoreEngine()

	// Case 1: Same-line suppression
	lines1 := []string{
		`apiKey := "sk-live-1234567890abcdef1234" // torusguard-ignore TG-SEC-001`,
		`otherKey := "sk-live-9999999999abcdef9999"`,
	}
	if !engine.ShouldIgnoreFinding("TG-SEC-001", "auth.go", 1, lines1) {
		t.Errorf("expected line 1 to be suppressed via same-line comment")
	}
	if engine.ShouldIgnoreFinding("TG-SEC-001", "auth.go", 2, lines1) {
		t.Errorf("expected line 2 NOT to be suppressed")
	}

	// Case 2: Preceding-line suppression with alternative syntax (# tg-ignore)
	lines2 := []string{
		`# tg-ignore TG-SEC-001`,
		`API_SECRET = "sk-live-abcdef1234567890abcdef"`,
	}
	if !engine.ShouldIgnoreFinding("TG-SEC-001", "config.py", 2, lines2) {
		t.Errorf("expected line 2 to be suppressed via preceding line comment")
	}

	// Case 3: Block suppression
	lines3 := []string{
		`func testHelper() {`,
		`    // torusguard-ignore-start`,
		`    query := "SELECT * FROM users WHERE id=" + id`,
		`    db.Query(query)`,
		`    // torusguard-ignore-end`,
		`    db.Query("SELECT * FROM passwords WHERE id=" + id)`,
		`}`,
	}
	if !engine.ShouldIgnoreFinding("TG-DB-002", "query.go", 3, lines3) {
		t.Errorf("expected line 3 inside block to be suppressed")
	}
	if !engine.ShouldIgnoreFinding("TG-DB-002", "query.go", 4, lines3) {
		t.Errorf("expected line 4 inside block to be suppressed")
	}
	if engine.ShouldIgnoreFinding("TG-DB-002", "query.go", 6, lines3) {
		t.Errorf("expected line 6 outside block NOT to be suppressed")
	}
}
