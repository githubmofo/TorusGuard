package scanner

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"regexp"
	"strings"
)

// TGQLRule represents a declarative security rule definition in YAML or JSON format,
// inspired by CodeCrafters 'build-your-own' and open-source query languages like Semgrep and CodeQL.
type TGQLRule struct {
	ID           string   `json:"id" yaml:"id"`
	Severity     string   `json:"severity" yaml:"severity"`
	Languages    []string `json:"languages" yaml:"languages"`
	Pattern      string   `json:"pattern" yaml:"pattern"`
	NotInside    string   `json:"not_inside" yaml:"not_inside"`
	Description  string   `json:"description" yaml:"description"`
	SuggestedFix string   `json:"suggested_fix" yaml:"suggested_fix"`
}

// CompileMetavariablePattern transforms a declarative pattern containing metavariables
// like $FUNC, $VAR, $PATH, $HANDLER into a compiled regular expression.
func CompileMetavariablePattern(pattern string) (*regexp.Regexp, error) {
	// Escape standard regex characters except metavariables
	escaped := regexp.QuoteMeta(pattern)
	metavarRegex := regexp.MustCompile(`\\\$[A-Z0-9_]+`)

	// Replace quoted metavariables with capture/match tokens
	converted := metavarRegex.ReplaceAllString(escaped, `[a-zA-Z0-9_\-\.]+`)

	// Also replace ellipses like ... with wildcard
	converted = strings.ReplaceAll(converted, `\.\.\.`, `.*?`)

	return regexp.Compile("(?i)" + converted)
}

// LoadCustomRules discovers and compiles custom security rules from .torusguard/custom_rules/
func LoadCustomRules(workspaceDir string) ([]RuleSignature, error) {
	var signatures []RuleSignature
	customDir := filepath.Join(workspaceDir, ".torusguard", "custom_rules")

	info, err := os.Stat(customDir)
	if err != nil || !info.IsDir() {
		return signatures, nil // No custom rules directory, cleanly return
	}

	entries, err := os.ReadDir(customDir)
	if err != nil {
		return signatures, err
	}

	for _, entry := range entries {
		if entry.IsDir() {
			continue
		}
		ext := strings.ToLower(filepath.Ext(entry.Name()))
		if ext != ".json" && ext != ".yaml" && ext != ".yml" {
			continue
		}

		filePath := filepath.Join(customDir, entry.Name())
		data, err := os.ReadFile(filePath)
		if err != nil {
			continue
		}

		var rule TGQLRule
		if ext == ".json" {
			if err := json.Unmarshal(data, &rule); err != nil {
				continue
			}
		} else {
			// Minimal pure-Go YAML parser for key-value rule formats
			rule = parseSimpleYAMLRule(string(data))
		}

		if rule.ID == "" || rule.Pattern == "" {
			continue
		}

		compiledRegex, err := CompileMetavariablePattern(rule.Pattern)
		if err != nil {
			// Fallback to literal search if regex compilation fails
			compiledRegex = regexp.MustCompile(regexp.QuoteMeta(rule.Pattern))
		}

		severity := strings.ToUpper(rule.Severity)
		if severity == "" {
			severity = "HIGH"
		}

		signatures = append(signatures, RuleSignature{
			RuleID:       rule.ID,
			Severity:     severity,
			Description:  rule.Description,
			Regex:        compiledRegex,
			FileExts:     rule.Languages,
			SuggestedFix: rule.SuggestedFix,
		})
	}

	return signatures, nil
}

// parseSimpleYAMLRule parses straightforward key-value YAML strings without external dependencies
func parseSimpleYAMLRule(yamlStr string) TGQLRule {
	var rule TGQLRule
	lines := strings.Split(yamlStr, "\n")
	for _, line := range lines {
		trimmed := strings.TrimSpace(line)
		if strings.HasPrefix(trimmed, "#") || !strings.Contains(trimmed, ":") {
			continue
		}
		parts := strings.SplitN(trimmed, ":", 2)
		key := strings.TrimSpace(parts[0])
		val := strings.TrimSpace(parts[1])
		val = strings.Trim(val, `"'`)

		switch strings.ToLower(key) {
		case "id":
			rule.ID = val
		case "severity":
			rule.Severity = val
		case "pattern":
			rule.Pattern = val
		case "not_inside":
			rule.NotInside = val
		case "description":
			rule.Description = val
		case "suggested_fix":
			rule.SuggestedFix = val
		case "languages":
			// Parse languages if comma-separated or bracketed [js, ts, py]
			cleaned := strings.Trim(val, "[]")
			rawItems := strings.Split(cleaned, ",")
			for _, item := range rawItems {
				itemTrimmed := strings.TrimSpace(strings.Trim(item, `"'`))
				if itemTrimmed != "" {
					if !strings.HasPrefix(itemTrimmed, ".") {
						itemTrimmed = "." + itemTrimmed
					}
					rule.Languages = append(rule.Languages, itemTrimmed)
				}
			}
		}
	}
	return rule
}

// CountCustomRules returns the number of active custom rules in the workspace
func CountCustomRules(workspaceDir string) int {
	rules, err := LoadCustomRules(workspaceDir)
	if err != nil {
		return 0
	}
	return len(rules)
}

// FormatTGQLRuleTemplate returns a starter template for developers authoring new rules
func FormatTGQLRuleTemplate(ruleID string) string {
	return fmt.Sprintf(`# TorusGuard Declarative Security Rule (TG-QL)
id: %s
severity: HIGH
languages: [.js, .ts, .py, .go]
pattern: "$ROUTER.post($PATH, $HANDLER)"
not_inside: "authMiddleware"
description: "Unauthenticated HTTP route handler detected"
suggested_fix: "Enforce authorization middleware prior to route handler"
`, ruleID)
}
