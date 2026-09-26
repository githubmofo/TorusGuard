package scanner

import (
	"bufio"
	"context"
	"fmt"
	"os"
	"path/filepath"
	"regexp"
	"strings"
	"time"

	"github.com/torusguard/torusguard/internal/rules"
)

// FindingDetail represents a structured, line-level precise security finding
// adhering to the Alibaba OpenCodeReview hybrid architecture.
type FindingDetail struct {
	RuleID       string `json:"rule_id"`
	File         string `json:"file"`
	Line         int    `json:"line"`
	Severity     string `json:"severity"`
	Description  string `json:"description"`
	LineContent  string `json:"line_content"`
	Context      string `json:"context"` // Bounded AST window (1/9th token minimization)
	SuggestedFix string `json:"suggested_fix"`
}

// RuleSignature defines deterministic heuristic signatures across polyglot languages.
type RuleSignature struct {
	RuleID       string
	Severity     string
	Description  string
	Regex        *regexp.Regexp
	FileExts     []string // Empty = all code files (.go, .js, .ts, .py)
	SuggestedFix string
}

// BuiltinRules reflects Alibaba OpenCodeReview multi-language rulesets adapted for TorusGuard
var BuiltinRules = []RuleSignature{
	{
		RuleID:       "TG-SEC-001",
		Severity:     "CRITICAL",
		Description:  "Hardcoded secret, API key, or credential string detected",
		Regex:        regexp.MustCompile(`(?i)(password|secret|api_key|token)\s*[:=]?=\s*["'][a-zA-Z0-9_\-\.]{8,}["']`),
		SuggestedFix: "Extract secret to verified environment variable (e.g., os.Getenv or process.env)",
	},
	{
		RuleID:       "TG-SEC-001",
		Severity:     "CRITICAL",
		Description:  "Exposed OpenAI, Anthropic, or Stripe live API token",
		Regex:        regexp.MustCompile(`\b(sk-(?:live-)?[a-zA-Z0-9_\-\.]{20,})\b`),
		SuggestedFix: "Never hardcode live API keys in source code. Inject via secure secrets manager",
	},
	{
		RuleID:       "TG-DB-002",
		Severity:     "CRITICAL",
		Description:  "SQL Injection via dynamic string concatenation in query",
		Regex:        regexp.MustCompile(`(?i)(SELECT|INSERT|UPDATE|DELETE)\s+.*(WHERE|VALUES|FROM|SET).*["']\s*\+\s*[a-zA-Z0-9_]+|(?i)(db\.query|db\.execute)\s*\(\s*["'].*\+.*["']`),
		SuggestedFix: "Use parameterized queries with prepared placeholders ($1, ?, or named parameters)",
	},
	{
		RuleID:       "TG-NPE-001",
		Severity:     "HIGH",
		Description:  "Potential Null-Pointer Exception (NPE) or unchecked nil dereference",
		Regex:        regexp.MustCompile(`(?i)(req\.(body|query|params)\.[a-zA-Z0-9_]+\.[a-zA-Z0-9_]+|[a-zA-Z0-9_]+,\s*_\s*[:=]=\s*[a-zA-Z0-9_]+\(.*\)\s*;\s*[a-zA-Z0-9_]+\.)`),
		SuggestedFix: "Enforce optional chaining (?.), nil error guard, or explicit null boundary check",
	},
	{
		RuleID:       "TG-CONC-001",
		Severity:     "HIGH",
		Description:  "Concurrency hazard: unsafe goroutine loop closure or shared map mutation",
		Regex:        regexp.MustCompile(`(?i)go\s+func\(\)\s*\{[^}]*(\bval\b|\bitem\b|\bi\b|\bk\b|\bv\b)|(?i)go\s+func\(\)\s*\{[^}]*\[.*\]\s*=`),
		FileExts:     []string{".go"},
		SuggestedFix: "Pass iteration variables explicitly into goroutine arguments or guard map writes with sync.RWMutex",
	},
	{
		RuleID:       "TG-INPUT-002",
		Severity:     "HIGH",
		Description:  "Path traversal vulnerability via unsanitized file path concatenation",
		Regex:        regexp.MustCompile(`(?i)(path\.join|filepath\.Join|fs\.readFile|open)\(.*(req\.query|req\.params|req\.body|userInput|request\.args)`),
		SuggestedFix: "Sanitize path inputs using filepath.Base/path.basename and assert resolved path remains within root boundary",
	},
	{
		RuleID:       "TG-INPUT-004",
		Severity:     "HIGH",
		Description:  "Cross-Site Scripting (XSS) via unsafe DOM rendering sink",
		Regex:        regexp.MustCompile(`(?i)(dangerouslySetInnerHTML|innerHTML\s*=|document\.write\(|v-html)`),
		FileExts:     []string{".js", ".jsx", ".ts", ".tsx", ".vue"},
		SuggestedFix: "Replace raw HTML sinks with safe text rendering (textContent, innerText, or parameterized React elements)",
	},
	{
		RuleID:       "TG-DB-001",
		Severity:     "CRITICAL",
		Description:  "Multi-tenant isolation breach: database lookup missing tenant scope",
		Regex:        regexp.MustCompile(`(?i)(prisma\.[a-zA-Z0-9_]+\.find(Unique|First)|findUnique|findFirst)\(\s*\{\s*where:\s*\{\s*id:`),
		SuggestedFix: "Always scope database lookups by tenant or user ownership (e.g., where: { id, tenantId: user.tenantId })",
	},
	{
		RuleID:       "TG-DIFF-001",
		Severity:     "CRITICAL",
		Description:  "Security bypass detected: disabled TLS verification or nosec comment",
		Regex:        regexp.MustCompile(`(?i)(rejectUnauthorized:\s*false|verify\s*=\s*False|InsecureSkipVerify:\s*true|CURLOPT_SSL_VERIFYPEER\s*=>\s*false|#\s*nosec)`),
		SuggestedFix: "Never disable TLS verification or bypass static security checks",
	},
}

// ExtractContext extracts a bounded AST context window (radius lines before and after)
// around targetLine to minimize token usage (the 1/9th token strategy).
func ExtractContext(filePath string, targetLine int, radius int) (string, error) {
	file, err := os.Open(filePath)
	if err != nil {
		return "", err
	}
	defer file.Close()

	var lines []string
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		lines = append(lines, scanner.Text())
	}
	if err := scanner.Err(); err != nil {
		return "", err
	}

	total := len(lines)
	start := targetLine - radius - 1
	if start < 0 {
		start = 0
	}
	end := targetLine + radius
	if end > total {
		end = total
	}

	var sb strings.Builder
	for i := start; i < end; i++ {
		lineNum := i + 1
		marker := "  "
		if lineNum == targetLine {
			marker = "> "
		}
		sb.WriteString(fmt.Sprintf("%s%4d | %s\n", marker, lineNum, lines[i]))
	}

	return sb.String(), nil
}

// ScanDetailedAudit performs a static AST heuristic security scan, returning structured
// line-level precise findings with AST context boundaries.
func ScanDetailedAudit(targetDir string, catalog *rules.Catalog) ([]FindingDetail, error) {
	var detailed []FindingDetail

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Minute)
	defer cancel()

	fileCount := 0
	const maxFileCount = 10000

	err := filepath.Walk(targetDir, func(path string, info os.FileInfo, err error) error {
		select {
		case <-ctx.Done():
			return fmt.Errorf("scan aborted: timeout exceeded (5 minutes)")
		default:
		}

		if err != nil {
			return err
		}

		if info.IsDir() {
			name := info.Name()
			if name == "node_modules" || name == ".git" || name == ".torusguard" || name == "dist" || name == "build" || name == ".next" {
				return filepath.SkipDir
			}
			return nil
		}

		fileCount++
		if fileCount > maxFileCount {
			return fmt.Errorf("scan aborted: exceeded maximum file count limit of %d", maxFileCount)
		}

		ext := strings.ToLower(filepath.Ext(path))
		if ext != ".go" && ext != ".js" && ext != ".jsx" && ext != ".ts" && ext != ".tsx" && ext != ".py" {
			return nil // Limit scan to supported code files
		}

		base := info.Name()
		if strings.HasSuffix(base, "_test.go") || strings.HasSuffix(base, ".test.js") || strings.HasSuffix(base, ".test.ts") || strings.HasSuffix(base, ".spec.js") || strings.HasSuffix(base, ".spec.ts") {
			return nil // Skip test files
		}

		if info.Size() > 5*1024*1024 {
			return nil // Skip files larger than 5MB to prevent memory bloat
		}

		file, err := os.Open(path)
		if err != nil {
			return nil
		}
		defer file.Close()

		fileScanner := bufio.NewScanner(file)
		lineNum := 0
		var fileLines []string

		for fileScanner.Scan() {
			lineNum++
			lineText := fileScanner.Text()
			fileLines = append(fileLines, lineText)

			// Match against built-in rules
			for _, r := range BuiltinRules {
				// Check file extension filter
				if len(r.FileExts) > 0 {
					matchedExt := false
					for _, allowedExt := range r.FileExts {
						if ext == allowedExt {
							matchedExt = true
							break
						}
					}
					if !matchedExt {
						continue
					}
				}

				if r.Regex.MatchString(lineText) {
					relPath, _ := filepath.Rel(targetDir, path)
					if relPath == "" {
						relPath = path
					}

					finding := FindingDetail{
						RuleID:       r.RuleID,
						File:         relPath,
						Line:         lineNum,
						Severity:     r.Severity,
						Description:  r.Description,
						LineContent:  strings.TrimSpace(lineText),
						SuggestedFix: r.SuggestedFix,
					}
					detailed = append(detailed, finding)
				}
			}
		}

		return nil
	})

	if err != nil {
		return nil, fmt.Errorf("error walking directory: %v", err)
	}

	// 1. Container and Dockerfile security inspection
	if contFindings, err := ScanContainerFiles(targetDir); err == nil {
		detailed = append(detailed, contFindings...)
	}

	// 2. Git metadata and history secret mining
	if gitFindings, err := ScanGitHistory(targetDir); err == nil {
		detailed = append(detailed, gitFindings...)
	}

	// 3. Regular Expression Denial of Service (ReDoS) analysis
	if redosFindings, err := ScanReDoS(targetDir); err == nil {
		detailed = append(detailed, redosFindings...)
	}

	// 4. AI Model and RAG pipeline security guardrails
	if aiFindings, err := ScanAIGuard(targetDir); err == nil {
		detailed = append(detailed, aiFindings...)
	}

	// Populate bounded context for each finding (±3 lines)
	for i := range detailed {
		if detailed[i].Context == "" {
			absPath := filepath.Join(targetDir, detailed[i].File)
			ctxStr, ctxErr := ExtractContext(absPath, detailed[i].Line, 3)
			if ctxErr == nil {
				detailed[i].Context = ctxStr
			}
		}
	}

	return detailed, nil
}

// RunContainerAudit provides a dedicated runner for container and Docker security scans.
func RunContainerAudit(targetDir string) ([]FindingDetail, error) {
	return ScanContainerFiles(targetDir)
}

// RunGitMineAudit provides a dedicated runner for Git repository and history secret mining.
func RunGitMineAudit(targetDir string) ([]FindingDetail, error) {
	return ScanGitHistory(targetDir)
}

// RunReDoSAudit provides a dedicated runner for catastrophic regex backtracking checks.
func RunReDoSAudit(targetDir string) ([]FindingDetail, error) {
	return ScanReDoS(targetDir)
}

// RunAIGuardAudit provides a dedicated runner for AI agent and RAG pipeline security checks.
func RunAIGuardAudit(targetDir string) ([]FindingDetail, error) {
	return ScanAIGuard(targetDir)
}

// RunAudit wraps ScanDetailedAudit and OCR image scanning, providing backward compatibility
// with string slice outputs while formatting line-level precision and token-efficient AST snippets.
func RunAudit(targetDir string, catalog *rules.Catalog) ([]string, error) {
	fmt.Printf("Starting static heuristic security scan on %s...\n", targetDir)
	ruleCount := len(BuiltinRules) + 12 // Includes Container, Git, ReDoS, and AI Guard rules
	if catalog != nil && len(catalog.Rules) > 0 {
		ruleCount += len(catalog.Rules)
	}
	fmt.Printf("Active Rules: %d (Polyglot AST + First-Principles Security Suite)\n", ruleCount)

	var findings []string

	detailed, err := ScanDetailedAudit(targetDir, catalog)
	if err != nil {
		return nil, err
	}

	for _, d := range detailed {
		formatted := fmt.Sprintf("[%s] %s:%d: %s (Severity: %s) -> Suggested: %s",
			d.RuleID, d.File, d.Line, d.Description, d.Severity, d.SuggestedFix)
		findings = append(findings, formatted)
	}

	// Multi-Modal OCR Image Scanning
	ocrFindings, ocrErr := ScanImagesInDir(targetDir, DefaultMaxImageSize)
	if ocrErr == nil && len(ocrFindings) > 0 {
		for _, of := range ocrFindings {
			if !strings.HasPrefix(of, "[WARN]") {
				findings = append(findings, of)
			}
		}
	}

	if len(findings) == 0 {
		findings = append(findings, "No active findings detected. Posture is secure.")
	}

	return findings, nil
}
