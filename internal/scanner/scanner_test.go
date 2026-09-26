package scanner

import (
	"os"
	"path/filepath"
	"strings"
	"testing"
)

func TestExtractContext(t *testing.T) {
	tempDir := t.TempDir()
	testFile := filepath.Join(tempDir, "test.go")
	content := `package main

import "fmt"

func main() {
	apiKey := "sk-live-12345678901234567890"
	fmt.Println(apiKey)
}
`
	if err := os.WriteFile(testFile, []byte(content), 0644); err != nil {
		t.Fatalf("Failed to create test file: %v", err)
	}

	ctxStr, err := ExtractContext(testFile, 6, 2)
	if err != nil {
		t.Fatalf("ExtractContext failed: %v", err)
	}

	if !strings.Contains(ctxStr, ">    6 | \tapiKey :=") {
		t.Errorf("Expected context marker on line 6, got:\n%s", ctxStr)
	}
	if !strings.Contains(ctxStr, "   5 | func main() {") {
		t.Errorf("Expected line 5 in context, got:\n%s", ctxStr)
	}
}

func TestScanDetailedAuditRules(t *testing.T) {
	tempDir := t.TempDir()

	// 1. Create file with SQL Injection & Hardcoded Secret
	vulnCode := `package main

import "database/sql"

func queryUser(db *sql.DB, id string) {
	token := "secret_password_token_9999"
	query := "SELECT * FROM users WHERE id = '" + id + "'"
	db.Query(query)
}
`
	vulnPath := filepath.Join(tempDir, "vuln.go")
	if err := os.WriteFile(vulnPath, []byte(vulnCode), 0644); err != nil {
		t.Fatalf("Failed to write vuln.go: %v", err)
	}

	// 2. Create JS file with XSS and Path Traversal
	jsCode := `
const express = require('express');
const app = express();
const path = require('path');
const fs = require('fs');

app.get('/read', (req, res) => {
	const file = path.join(__dirname, req.query.file);
	fs.readFile(file, (err, data) => {
		document.getElementById('content').innerHTML = data;
	});
});
`
	jsPath := filepath.Join(tempDir, "app.js")
	if err := os.WriteFile(jsPath, []byte(jsCode), 0644); err != nil {
		t.Fatalf("Failed to write app.js: %v", err)
	}

	findings, err := ScanDetailedAudit(tempDir, nil)
	if err != nil {
		t.Fatalf("ScanDetailedAudit failed: %v", err)
	}

	matchedRules := make(map[string]bool)
	for _, f := range findings {
		matchedRules[f.RuleID] = true
		if f.Line == 0 {
			t.Errorf("Finding for %s has line 0", f.RuleID)
		}
		if f.Context == "" {
			t.Errorf("Finding for %s has empty context", f.RuleID)
		}
	}

	expectedRules := []string{"TG-SEC-001", "TG-DB-002", "TG-INPUT-002", "TG-INPUT-004"}
	for _, er := range expectedRules {
		if !matchedRules[er] {
			t.Errorf("Expected rule %s to match, but it was not detected. Detected: %v", er, matchedRules)
		}
	}
}
