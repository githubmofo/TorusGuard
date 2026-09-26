package scanner

import (
	"bufio"
	"os"
	"path/filepath"
	"regexp"
	"strings"
)

var (
	// Detects regex instantiation in JS, TS, Python, Go
	reRegexDefinition = regexp.MustCompile(`(?i)(new\s+RegExp\s*\(\s*['"]|re\.compile\s*\(\s*r?['"]|regexp\.MustCompile\s*\(\s*[` + "`" + `'"]|/(?:\\/|[^/\n\r])+/[gimsuy]*)`)
	// Nested repetitions like (a+)+, ([0-9]+)*, ((\w+)\.)+
	reNestedQuantifier = regexp.MustCompile(`(\([^\(\)]+[\+\*][^\(\)]*\)\s*[\+\*]|\)[+\*][^)]*\)[+\*])`)
	// Overlapping alternation with outer repetition: (a|b)+ or (x|y)*
	reOverlappingAlt = regexp.MustCompile(`\([a-zA-Z0-9_\-]+\|[a-zA-Z0-9_\-]+\)\s*[\+\*]`)
)

// ScanReDoS scans source code files for catastrophic exponential backtracking regular expressions.
func ScanReDoS(targetDir string) ([]FindingDetail, error) {
	var findings []FindingDetail

	err := filepath.Walk(targetDir, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return err
		}
		if info.IsDir() {
			name := info.Name()
			if name == "node_modules" || name == ".git" || name == ".torusguard" || name == "dist" || name == "build" {
				return filepath.SkipDir
			}
			return nil
		}

		ext := strings.ToLower(filepath.Ext(path))
		if ext != ".js" && ext != ".jsx" && ext != ".ts" && ext != ".tsx" && ext != ".py" && ext != ".go" {
			return nil
		}

		base := info.Name()
		if strings.HasSuffix(base, "_test.go") || strings.HasSuffix(base, ".test.js") || strings.HasSuffix(base, ".test.ts") {
			return nil
		}

		file, err := os.Open(path)
		if err != nil {
			return nil
		}
		defer file.Close()

		relPath, _ := filepath.Rel(targetDir, path)
		scanner := bufio.NewScanner(file)
		lineNum := 0

		for scanner.Scan() {
			lineNum++
			line := scanner.Text()
			trimmed := strings.TrimSpace(line)

			if strings.HasPrefix(trimmed, "//") || strings.HasPrefix(trimmed, "#") {
				continue
			}

			// TG-REDOS-001: Nested quantifier (a+)+
			if reNestedQuantifier.MatchString(line) && (strings.Contains(line, "RegExp") || strings.Contains(line, "compile") || strings.Contains(line, "/") || ext == ".py" || ext == ".js" || ext == ".ts") {
				ctx, _ := ExtractContext(path, lineNum, 3)
				findings = append(findings, FindingDetail{
					RuleID:       "TG-REDOS-001",
					File:         relPath,
					Line:         lineNum,
					Severity:     "HIGH",
					Description:  "Catastrophic exponential backtracking (ReDoS) detected in regular expression",
					LineContent:  trimmed,
					Context:      ctx,
					SuggestedFix: "Eliminate nested quantifiers (e.g. rewrite (a+)+ to a+), use atomic groups, or bound input length.",
				})
			} else if reOverlappingAlt.MatchString(line) {
				// TG-REDOS-002: Overlapping alternation
				ctx, _ := ExtractContext(path, lineNum, 3)
				findings = append(findings, FindingDetail{
					RuleID:       "TG-REDOS-002",
					File:         relPath,
					Line:         lineNum,
					Severity:     "MEDIUM",
					Description:  "Unbounded overlapping alternation in regex vulnerable to polynomial slowdown",
					LineContent:  trimmed,
					Context:      ctx,
					SuggestedFix: "Ensure alternation branches are mutually exclusive or replace with dedicated parser.",
				})
			}
		}

		return nil
	})

	return findings, err
}
