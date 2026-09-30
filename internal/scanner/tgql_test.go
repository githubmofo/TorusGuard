package scanner

import (
	"os"
	"path/filepath"
	"testing"
)

func TestTGQLCustomRulesCompilation(t *testing.T) {
	tempDir, err := os.MkdirTemp("", "tgql-test-*")
	if err != nil {
		t.Fatalf("Failed to create temp dir: %v", err)
	}
	defer os.RemoveAll(tempDir)

	customDir := filepath.Join(tempDir, ".torusguard", "custom_rules")
	if err := os.MkdirAll(customDir, 0755); err != nil {
		t.Fatalf("Failed to create custom rules dir: %v", err)
	}

	// Write sample custom rule
	sampleRule := `id: TG-CUSTOM-001
severity: CRITICAL
languages: [.js, .ts]
pattern: "app.post('/api/admin', $HANDLER)"
description: "Unauthenticated administrative endpoint"
suggested_fix: "Add adminAuth middleware"
`
	rulePath := filepath.Join(customDir, "admin-rule.yaml")
	if err := os.WriteFile(rulePath, []byte(sampleRule), 0644); err != nil {
		t.Fatalf("Failed to write custom rule file: %v", err)
	}

	rules, err := LoadCustomRules(tempDir)
	if err != nil {
		t.Fatalf("LoadCustomRules failed: %v", err)
	}

	if len(rules) != 1 {
		t.Fatalf("Expected 1 custom rule, got %d", len(rules))
	}

	r := rules[0]
	if r.RuleID != "TG-CUSTOM-001" {
		t.Errorf("Expected RuleID TG-CUSTOM-001, got %s", r.RuleID)
	}
	if r.Severity != "CRITICAL" {
		t.Errorf("Expected Severity CRITICAL, got %s", r.Severity)
	}

	// Test pattern matching
	testCode := "app.post('/api/admin', handleAdminRequest)"
	if !r.Regex.MatchString(testCode) {
		t.Errorf("Expected pattern to match '%s'", testCode)
	}
}

func TestThompsonNFASimulator(t *testing.T) {
	sim := NewThompsonNFASimulator()

	// 1. Exponential backtracking
	expResult := sim.Analyze(`^([a-zA-Z0-9]+)+$`)
	if !expResult.IsVulnerable {
		t.Errorf("Expected pattern ^([a-zA-Z0-9]+)+$ to be vulnerable to exponential ReDoS")
	}
	if expResult.Complexity != "O(2^n) - Exponential Catastrophic" {
		t.Errorf("Expected O(2^n), got %s", expResult.Complexity)
	}

	// 2. Linear safe regex
	linearResult := sim.Analyze(`^[a-zA-Z0-9]+$`)
	if linearResult.IsVulnerable {
		t.Errorf("Expected pattern ^[a-zA-Z0-9]+$ to be safe linear regex")
	}
}
