package scanner

import (
	"fmt"
	"path/filepath"
	"regexp"
	"strings"
)

// TaintSourcePattern identifies statements where untrusted external user input enters execution.
var taintSourceRegex = regexp.MustCompile(`(?i)(?:` +
	// Go web frameworks (net/http, Gin, Fiber, Echo)
	`r\.URL\.Query\(\)|r\.FormValue\(|r\.PostFormValue\(|c\.Query\(|c\.Param\(|c\.PostForm\(|req\.Body|` +
	// Node.js / Express / Fastify / Next.js
	`req\.body|req\.query|req\.params|req\.headers|searchParams\.get\(|process\.argv\[|` +
	// Python (FastAPI, Flask, Django)
	`request\.args|request\.query_params|request\.form|request\.json\(\)|request\.POST|request\.GET|sys\.argv\[` +
	`)`)

// TaintSanitizerPattern identifies common sanitization and safe-conversion calls.
var taintSanitizerRegex = regexp.MustCompile(`(?i)(?:strconv\.Atoi|parseInt|parseFloat|int\(|float\(|Number\(|filepath\.Base|path\.basename|DOMPurify|escapeHtml|validator|sanitize)`)

// TaintSink defines an unsafe sink and the corresponding TorusGuard rule.
type TaintSink struct {
	RuleID       string
	Severity     string
	SinkName     string
	Regex        *regexp.Regexp
	SuggestedFix string
}

var taintSinks = []TaintSink{
	{
		RuleID:       "TG-DB-002",
		Severity:     "CRITICAL",
		SinkName:     "SQL Query Sink",
		Regex:        regexp.MustCompile(`(?i)(?:db\.Query|db\.Exec|db\.QueryRow|cursor\.execute|db\.execute|client\.query)\s*\(`),
		SuggestedFix: "Use parameterized queries with prepared placeholders ($1, ?, or named parameters)",
	},
	{
		RuleID:       "TG-INPUT-001",
		Severity:     "CRITICAL",
		SinkName:     "Command Execution Sink",
		Regex:        regexp.MustCompile(`(?i)(?:exec\.Command|child_process\.exec|child_process\.spawn|os\.system|subprocess\.call|subprocess\.Popen|subprocess\.run)\s*\(`),
		SuggestedFix: "Avoid passing concatenated strings to shell execution. Use array arguments with fixed binaries",
	},
	{
		RuleID:       "TG-INPUT-002",
		Severity:     "HIGH",
		SinkName:     "File Path Sink",
		Regex:        regexp.MustCompile(`(?i)(?:os\.Open|os\.ReadFile|os\.Create|fs\.readFile|fs\.readFileSync|open)\s*\(`),
		SuggestedFix: "Sanitize path inputs with filepath.Base and assert resolved path remains within root boundary",
	},
}

// Assignment extraction regexes for Go, JS/TS, and Python
var (
	// Go: varName := ... or varName = ...
	goAssignRegex = regexp.MustCompile(`^\s*([a-zA-Z0-9_]+)\s*[:=]=\s*(.+)$`)
	// JS/TS: const/let/var varName = ... or varName = ...
	jsAssignRegex = regexp.MustCompile(`^\s*(?:const|let|var)\s+([a-zA-Z0-9_]+)\s*=\s*(.+)$`)
	// Python: varName = ...
	pyAssignRegex = regexp.MustCompile(`^\s*([a-zA-Z0-9_]+)\s*=\s*(.+)$`)
)

// TaintedVar records the origin and lifecycle of a tainted variable within a scope.
type TaintedVar struct {
	Name       string
	SourceLine int
	SourceExpr string
	Sanitized  bool
}

// AnalyzeFileTaint performs intra-file lexical dataflow tracking across variable assignments.
func AnalyzeFileTaint(relPath string, lines []string, ignoreEngine *IgnoreEngine) []FindingDetail {
	var findings []FindingDetail
	ext := strings.ToLower(filepath.Ext(relPath))

	taintedVars := make(map[string]TaintedVar)

	for idx, rawLine := range lines {
		lineNum := idx + 1
		line := strings.TrimSpace(rawLine)

		if line == "" || strings.HasPrefix(line, "//") || strings.HasPrefix(line, "#") || strings.HasPrefix(line, "/*") {
			continue
		}

		// 1. Check for sink execution with any tainted variables
		for _, sink := range taintSinks {
			if sink.Regex.MatchString(line) {
				for tName, tVar := range taintedVars {
					if !tVar.Sanitized && containsIdentifier(line, tName) {
						if ignoreEngine != nil && ignoreEngine.ShouldIgnoreFinding(sink.RuleID, relPath, lineNum, lines) {
							continue
						}

						desc := fmt.Sprintf("Multi-hop tainted dataflow reaching %s: variable '%s' originated from untrusted input at line %d",
							sink.SinkName, tName, tVar.SourceLine)

						finding := FindingDetail{
							RuleID:       sink.RuleID,
							File:         relPath,
							Line:         lineNum,
							Severity:     sink.Severity,
							Description:  desc,
							LineContent:  line,
							SuggestedFix: sink.SuggestedFix,
						}
						findings = append(findings, finding)
						break
					}
				}
			}
		}

		// 2. Check for variable assignment and taint propagation
		varName, rhsExpr := extractAssignment(line, ext)
		if varName != "" && rhsExpr != "" {
			// Check if RHS introduces a new tainted source
			if taintSourceRegex.MatchString(rhsExpr) {
				if taintSanitizerRegex.MatchString(rhsExpr) {
					// Sanitized at source
					taintedVars[varName] = TaintedVar{Name: varName, SourceLine: lineNum, SourceExpr: rhsExpr, Sanitized: true}
				} else {
					taintedVars[varName] = TaintedVar{Name: varName, SourceLine: lineNum, SourceExpr: rhsExpr, Sanitized: false}
				}
				continue
			}

			// Check if RHS references an existing tainted variable
			for existingName, tVar := range taintedVars {
				if !tVar.Sanitized && containsIdentifier(rhsExpr, existingName) {
					if taintSanitizerRegex.MatchString(rhsExpr) {
						// Variable neutralized by sanitizer
						taintedVars[varName] = TaintedVar{Name: varName, SourceLine: tVar.SourceLine, SourceExpr: tVar.SourceExpr, Sanitized: true}
					} else {
						// Taint propagated to new variable
						taintedVars[varName] = TaintedVar{Name: varName, SourceLine: tVar.SourceLine, SourceExpr: tVar.SourceExpr, Sanitized: false}
					}
					break
				}
			}
			continue
		}
	}

	return findings
}

func extractAssignment(line, ext string) (string, string) {
	switch ext {
	case ".go":
		m := goAssignRegex.FindStringSubmatch(line)
		if len(m) == 3 {
			return m[1], m[2]
		}
	case ".js", ".jsx", ".ts", ".tsx":
		m := jsAssignRegex.FindStringSubmatch(line)
		if len(m) == 3 {
			return m[1], m[2]
		}
	case ".py":
		m := pyAssignRegex.FindStringSubmatch(line)
		if len(m) == 3 {
			return m[1], m[2]
		}
	}
	return "", ""
}

func containsIdentifier(expr, id string) bool {
	// Match identifier with word boundary
	re := regexp.MustCompile(`\b` + regexp.QuoteMeta(id) + `\b`)
	return re.MatchString(expr)
}
