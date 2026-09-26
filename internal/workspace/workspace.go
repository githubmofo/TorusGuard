package workspace

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"strings"

	"github.com/torusguard/torusguard/internal/termui"
)

// TorusConfig represents the persistent project configuration
type TorusConfig struct {
	Version      string   `json:"version"`
	Stack        []string `json:"stack"`
	ActiveRules  int      `json:"active_rules"`
	RulesFamily  int      `json:"rules_families"`
	MaxImageMB   int      `json:"max_image_mb"`
	PonytailMaxAdd int    `json:"ponytail_max_add"`
	PonytailMaxDel int    `json:"ponytail_max_del"`
}

// InitWorkspace scaffolds the complete .torusguard directory tree and generates configuration
func InitWorkspace(target string) error {
	tgDir := filepath.Join(target, ".torusguard")
	dirs := []string{
		filepath.Join(tgDir, "config"),
		filepath.Join(tgDir, "rules", "active"),
		filepath.Join(tgDir, "snapshots"),
		filepath.Join(tgDir, "runs"),
		filepath.Join(tgDir, "memory"),
	}

	for _, d := range dirs {
		if err := os.MkdirAll(d, 0755); err != nil {
			return fmt.Errorf("failed to create directory %s: %v", d, err)
		}
	}

	stack, _ := DetectStack(target)
	if len(stack) == 0 {
		stack = []string{"Polyglot / Generic"}
	}

	// Write config
	cfg := TorusConfig{
		Version:        "2.0.0",
		Stack:          stack,
		ActiveRules:    74,
		RulesFamily:    18,
		MaxImageMB:     10,
		PonytailMaxAdd: 35,
		PonytailMaxDel: 25,
	}

	cfgPath := filepath.Join(tgDir, "config", "torusguard.json")
	if data, err := json.MarshalIndent(cfg, "", "  "); err == nil {
		_ = os.WriteFile(cfgPath, data, 0644)
	}

	// Baseline SECURITY.md if absent
	secPath := filepath.Join(target, "SECURITY.md")
	if _, err := os.Stat(secPath); os.IsNotExist(err) {
		secContent := "# Security Policy\n\n## Reporting a Vulnerability\n" +
			"Please report security flaws to the repository maintainers.\n" +
			"This workspace is protected by TorusGuard Autonomous Security Guardrails.\n"
		_ = os.WriteFile(secPath, []byte(secContent), 0644)
	}

	fmt.Println()
	fmt.Println(termui.CardHeader("🛡️  TORUSGUARD INITIALIZED", "Workspace Provisioned", "v2.0.0", termui.Green))
	fmt.Println(termui.CardBorderTop("Configuration", termui.Green, false))
	fmt.Println(termui.FormatBoxLine(fmt.Sprintf("Primary Stack:     %s", strings.Join(stack, ", ")), 67, "│", termui.Green))
	fmt.Println(termui.FormatBoxLine(fmt.Sprintf("Active Rules:      %d canonical invariants across %d families", cfg.ActiveRules, cfg.RulesFamily), 67, "│", termui.Green))
	fmt.Println(termui.FormatBoxLine(fmt.Sprintf("Config Path:       .torusguard/config/torusguard.json"), 67, "│", termui.Green))
	fmt.Println(termui.FormatBoxLine(fmt.Sprintf("Security Policy:   SECURITY.md provisioned at root"), 67, "│", termui.Green))
	fmt.Println(termui.CardBorderBottom(termui.Green, false))
	fmt.Println()

	return nil
}

// DetectStack determines the primary languages/frameworks in the target
func DetectStack(target string) ([]string, error) {
	var stack []string

	if _, err := os.Stat(filepath.Join(target, "package.json")); err == nil {
		stack = append(stack, "Node.js / JavaScript")
	}
	if _, err := os.Stat(filepath.Join(target, "go.mod")); err == nil {
		stack = append(stack, "Go")
	}
	if _, err := os.Stat(filepath.Join(target, "requirements.txt")); err == nil {
		stack = append(stack, "Python")
	}
	if _, err := os.Stat(filepath.Join(target, "Cargo.toml")); err == nil {
		stack = append(stack, "Rust")
	}

	return stack, nil
}
