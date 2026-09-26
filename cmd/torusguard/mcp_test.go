package main

import (
	"encoding/json"
	"strings"
	"testing"
)

func TestDeclaredMCPTools(t *testing.T) {
	tools := GetDeclaredTools()
	if len(tools) == 0 {
		t.Fatalf("Expected declared MCP tools, got none")
	}

	requiredTools := map[string]bool{
		"torusguard_audit":     false,
		"torusguard_ocr_scan":  false,
		"torusguard_container": false,
		"torusguard_git_mine":  false,
		"torusguard_redos":     false,
		"torusguard_ai_guard":  false,
		"torusguard_harden":    false,
		"torusguard_recheck":   false,
		"torusguard_status":    false,
		"torusguard_verify":    false,
	}

	for _, tool := range tools {
		if _, ok := requiredTools[tool.Name]; ok {
			requiredTools[tool.Name] = true
		}
		if tool.Description == "" {
			t.Errorf("Tool %s missing description", tool.Name)
		}
		if tool.InputSchema.Type != "object" {
			t.Errorf("Tool %s input schema type must be 'object'", tool.Name)
		}
	}

	for name, found := range requiredTools {
		if !found {
			t.Errorf("Expected MCP tool '%s' to be declared", name)
		}
	}
}

func TestDeclaredMCPResources(t *testing.T) {
	resources := GetDeclaredResources()
	if len(resources) < 2 {
		t.Fatalf("Expected at least 2 declared resources, got %d", len(resources))
	}

	foundReport := false
	for _, res := range resources {
		if res.URI == "torusguard://security_report" {
			foundReport = true
			if res.MimeType != "text/markdown" {
				t.Errorf("Expected markdown mime type for security report, got %s", res.MimeType)
			}
		}
	}

	if !foundReport {
		t.Errorf("Expected torusguard://security_report resource to be declared")
	}
}

func TestTruncateOutputSafeguard(t *testing.T) {
	hugeStr := strings.Repeat("A", 40000)
	truncated := truncateOutput(hugeStr)
	if len(truncated) >= 40000 {
		t.Errorf("Output was not truncated")
	}
	if !strings.Contains(truncated, "Output truncated") {
		t.Errorf("Missing truncation notification string")
	}
}

func TestHandleStatusToolCall(t *testing.T) {
	rawArgs := json.RawMessage(`{"target": "."}`)
	res := handleMCPToolCall("torusguard_status", rawArgs)
	if res.IsError {
		t.Fatalf("Expected status call to succeed, got error")
	}
	if len(res.Content) == 0 || !strings.Contains(res.Content[0].Text, "TorusGuard Posture Status") {
		t.Errorf("Unexpected status output: %v", res.Content)
	}
}

func TestHandleVerifyToolCall(t *testing.T) {
	rawArgs := json.RawMessage(`{"target": "../.."}`)
	res := handleMCPToolCall("torusguard_verify", rawArgs)
	if res.IsError {
		t.Fatalf("Expected verify call to succeed, got error")
	}
	if len(res.Content) == 0 {
		t.Fatalf("Expected non-empty content in verify response")
	}
	if !strings.Contains(res.Content[0].Text, "Finding Evidence Verification") &&
		!strings.Contains(res.Content[0].Text, "No security_report.md found") {
		t.Errorf("Unexpected verify output: %v", res.Content)
	}
}

func TestHandleFirstPrinciplesMCPTools(t *testing.T) {
	rawArgs := json.RawMessage(`{"target": "."}`)

	// Container tool
	resCont := handleMCPToolCall("torusguard_container", rawArgs)
	if resCont.IsError {
		t.Errorf("Expected torusguard_container to succeed, got error: %v", resCont)
	}
	if len(resCont.Content) == 0 || !strings.Contains(resCont.Content[0].Text, "Container & Docker Security Audit") {
		t.Errorf("Unexpected container tool output: %v", resCont)
	}

	// Git mine tool
	resGit := handleMCPToolCall("torusguard_git_mine", rawArgs)
	if resGit.IsError {
		t.Errorf("Expected torusguard_git_mine to succeed, got error: %v", resGit)
	}
	if len(resGit.Content) == 0 || !strings.Contains(resGit.Content[0].Text, "Git Repository & History Secret Mining") {
		t.Errorf("Unexpected git mine tool output: %v", resGit)
	}

	// ReDoS tool
	resReDoS := handleMCPToolCall("torusguard_redos", rawArgs)
	if resReDoS.IsError {
		t.Errorf("Expected torusguard_redos to succeed, got error: %v", resReDoS)
	}
	if len(resReDoS.Content) == 0 || !strings.Contains(resReDoS.Content[0].Text, "ReDoS") {
		t.Errorf("Unexpected redos tool output: %v", resReDoS)
	}

	// AI Guard tool
	resAI := handleMCPToolCall("torusguard_ai_guard", rawArgs)
	if resAI.IsError {
		t.Errorf("Expected torusguard_ai_guard to succeed, got error: %v", resAI)
	}
	if len(resAI.Content) == 0 || !strings.Contains(resAI.Content[0].Text, "AI Application & RAG Pipeline Audit") {
		t.Errorf("Unexpected ai guard tool output: %v", resAI)
	}
}


