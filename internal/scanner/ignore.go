package scanner

import (
	"bufio"
	"os"
	"path/filepath"
	"regexp"
	"strings"
)

// IgnoreEngine handles file-level, rule-specific, and inline comment-level suppressions.
type IgnoreEngine struct {
	GlobalPatterns []string            // Glob patterns that ignore entire files/folders
	RulePatterns   map[string][]string // RuleID -> list of glob patterns where the rule is suppressed
}

var (
	inlineIgnoreRegex = regexp.MustCompile(`(?i)(?://|#)\s*(?:torusguard-ignore|tg-ignore)(?:[ \t]+([A-Z0-9_\-]+)|[ \t]*$)`)
	blockStartRegex   = regexp.MustCompile(`(?i)(?://|#)\s*(?:torusguard-ignore-start|tg-ignore-start)(?:[ \t]*$)`)
	blockEndRegex     = regexp.MustCompile(`(?i)(?://|#)\s*(?:torusguard-ignore-end|tg-ignore-end)(?:[ \t]*$)`)
)

// NewIgnoreEngine creates an empty IgnoreEngine.
func NewIgnoreEngine() *IgnoreEngine {
	return &IgnoreEngine{
		GlobalPatterns: []string{},
		RulePatterns:   make(map[string][]string),
	}
}

// LoadIgnoreEngine loads suppression rules from .torusguardignore and .torusguard/ignore.
func LoadIgnoreEngine(workspaceDir string) *IgnoreEngine {
	engine := NewIgnoreEngine()

	candidatePaths := []string{
		filepath.Join(workspaceDir, ".torusguardignore"),
		filepath.Join(workspaceDir, ".torusguard", "ignore"),
		filepath.Join(workspaceDir, ".torusguard", ".torusguardignore"),
	}

	for _, p := range candidatePaths {
		if data, err := os.ReadFile(p); err == nil {
			engine.parseIgnoreContent(string(data))
		}
	}

	return engine
}

// parseIgnoreContent parses ignore file syntax including comments, globs, and rule-scoped lines.
func (ie *IgnoreEngine) parseIgnoreContent(content string) {
	scanner := bufio.NewScanner(strings.NewReader(content))
	for scanner.Scan() {
		line := strings.TrimSpace(scanner.Text())
		if line == "" || strings.HasPrefix(line, "#") {
			continue
		}

		// Check for rule-scoped syntax: e.g. "TG-SEC-001: tests/fixtures/*"
		if strings.Contains(line, ":") {
			parts := strings.SplitN(line, ":", 2)
			ruleID := strings.ToUpper(strings.TrimSpace(parts[0]))
			pat := strings.TrimSpace(parts[1])
			if strings.HasPrefix(ruleID, "TG-") && pat != "" {
				ie.RulePatterns[ruleID] = append(ie.RulePatterns[ruleID], normalizePattern(pat))
				continue
			}
		}

		// Standard global file/directory ignore pattern
		ie.GlobalPatterns = append(ie.GlobalPatterns, normalizePattern(line))
	}
}

// normalizePattern ensures forward slashes for cross-platform glob matching.
func normalizePattern(pat string) string {
	pat = strings.ReplaceAll(pat, "\\", "/")
	return strings.TrimPrefix(pat, "./")
}

// matchGlob performs flexible glob matching supporting ** wildcards.
func matchGlob(pattern, target string) bool {
	pattern = normalizePattern(pattern)
	target = normalizePattern(target)

	// Direct match
	if pattern == target {
		return true
	}

	// Handle trailing /** or /*
	if strings.HasSuffix(pattern, "/**") {
		prefix := strings.TrimSuffix(pattern, "/**")
		if target == prefix || strings.HasPrefix(target, prefix+"/") {
			return true
		}
	}
	if strings.HasSuffix(pattern, "/*") {
		prefix := strings.TrimSuffix(pattern, "/*")
		if strings.HasPrefix(target, prefix+"/") && !strings.Contains(strings.TrimPrefix(target, prefix+"/"), "/") {
			return true
		}
	}

	// Leading **/ match
	if strings.HasPrefix(pattern, "**/") {
		suffix := strings.TrimPrefix(pattern, "**/")
		if strings.HasSuffix(target, suffix) || strings.Contains(target, "/"+suffix) {
			return true
		}
	}

	// Standard filepath.Match fallback
	matched, err := filepath.Match(pattern, target)
	if err == nil && matched {
		return true
	}

	// Also test basename match if pattern has no slash (e.g. "*.mock.ts" or "vendor")
	if !strings.Contains(pattern, "/") {
		base := filepath.Base(target)
		if matched, err := filepath.Match(pattern, base); err == nil && matched {
			return true
		}
		if base == pattern {
			return true
		}
	}

	return false
}

// ShouldIgnoreFile checks if the entire file path is ignored by global patterns.
func (ie *IgnoreEngine) ShouldIgnoreFile(relPath string) bool {
	for _, pat := range ie.GlobalPatterns {
		if matchGlob(pat, relPath) {
			return true
		}
	}
	return false
}

// ShouldIgnoreRuleForFile checks if a specific rule is suppressed for the given file.
func (ie *IgnoreEngine) ShouldIgnoreRuleForFile(ruleID, relPath string) bool {
	if patterns, ok := ie.RulePatterns[strings.ToUpper(ruleID)]; ok {
		for _, pat := range patterns {
			if matchGlob(pat, relPath) {
				return true
			}
		}
	}
	return false
}

// ShouldIgnoreFinding determines if a finding at lineNum is suppressed by file pattern,
// rule-scoped pattern, or inline/block comment suppression in the source code.
func (ie *IgnoreEngine) ShouldIgnoreFinding(ruleID, relPath string, lineNum int, fileLines []string) bool {
	// 1. File-level ignore
	if ie.ShouldIgnoreFile(relPath) {
		return true
	}

	// 2. Rule-scoped path ignore
	if ie.ShouldIgnoreRuleForFile(ruleID, relPath) {
		return true
	}

	if len(fileLines) == 0 || lineNum < 1 || lineNum > len(fileLines) {
		return false
	}

	// 3. Inline line suppression on current line
	currLine := fileLines[lineNum-1]
	if matchInlineSuppression(currLine, ruleID) {
		return true
	}

	// 4. Inline suppression on preceding line (only if preceding line is a standalone comment)
	if lineNum > 1 {
		prevLine := strings.TrimSpace(fileLines[lineNum-2])
		if (strings.HasPrefix(prevLine, "//") || strings.HasPrefix(prevLine, "#")) && matchInlineSuppression(prevLine, ruleID) {
			return true
		}
	}

	// 5. Block suppression check: scanning upwards for open block ignore
	inIgnoredBlock := false
	for i := 0; i < lineNum; i++ {
		trimmed := strings.TrimSpace(fileLines[i])
		if blockStartRegex.MatchString(trimmed) {
			inIgnoredBlock = true
		} else if blockEndRegex.MatchString(trimmed) {
			inIgnoredBlock = false
		}
	}
	if inIgnoredBlock {
		return true
	}

	return false
}

// matchInlineSuppression checks if a line contains a valid inline ignore comment.
func matchInlineSuppression(line, ruleID string) bool {
	matches := inlineIgnoreRegex.FindStringSubmatch(line)
	if len(matches) > 0 {
		suppressedRule := strings.ToUpper(strings.TrimSpace(matches[1]))
		// If no specific rule is specified, suppresses all rules on that line
		if suppressedRule == "" || suppressedRule == strings.ToUpper(ruleID) {
			return true
		}
	}
	return false
}
