package main

import (
	"bufio"
	"fmt"
	"os/exec"
	"path/filepath"
	"regexp"
	"strconv"
	"strings"

	"github.com/torusguard/torusguard/internal/scanner"
	"github.com/torusguard/torusguard/internal/termui"
)

// ReviewResult aggregates differential PR review outcomes
type ReviewResult struct {
	DiffRef        string                  `json:"diff_ref"`
	FilesInspected int                     `json:"files_inspected"`
	LinesAdded     int                     `json:"lines_added"`
	LinesRemoved   int                     `json:"lines_removed"`
	NewViolations  []scanner.FindingDetail `json:"new_violations"`
	Status         string                  `json:"status"` // PASSED / BLOCKED
}

// RunReview executes incremental Git diff security review against a reference branch or commit
func RunReview(targetDir string, diffRef string) (*ReviewResult, error) {
	if diffRef == "" {
		diffRef = "HEAD~1"
	}

	fmt.Println()
	fmt.Println(termui.CardHeader("🛡️  PULL REQUEST / GIT DIFF REVIEW", "Differential Incremental Security Gate", "v"+Version, termui.Cyan))

	// 1. Gather active rules (builtin + custom TG-QL)
	activeRules := append([]scanner.RuleSignature{}, scanner.BuiltinRules...)
	if customRules, err := scanner.LoadCustomRules(targetDir); err == nil && len(customRules) > 0 {
		activeRules = append(activeRules, customRules...)
	}

	// 2. Fetch git diff output
	cmd := exec.Command("git", "diff", "-U0", diffRef)
	cmd.Dir = targetDir
	output, err := cmd.CombinedOutput()
	if err != nil {
		// Fallback to git status or clean state if ref is invalid
		cmd = exec.Command("git", "diff", "-U0", "HEAD")
		cmd.Dir = targetDir
		output, _ = cmd.CombinedOutput()
	}

	res := &ReviewResult{
		DiffRef: diffRef,
		Status:  "PASSED",
	}

	diffScanner := bufio.NewScanner(strings.NewReader(string(output)))
	currentFile := ""
	currentLine := 0
	filesSet := make(map[string]bool)

	reHunk := regexp.MustCompile(`^@@ -\d+(?:,\d+)? \+(\d+)(?:,\d+)? @@`)

	for diffScanner.Scan() {
		line := diffScanner.Text()

		if strings.HasPrefix(line, "diff --git a/") {
			parts := strings.Fields(line)
			if len(parts) >= 3 {
				currentFile = strings.TrimPrefix(parts[2], "a/")
				filesSet[currentFile] = true
			}
		} else if strings.HasPrefix(line, "@@ ") {
			if match := reHunk.FindStringSubmatch(line); len(match) > 1 {
				currentLine, _ = strconv.Atoi(match[1])
			}
		} else if strings.HasPrefix(line, "+") && !strings.HasPrefix(line, "+++") {
			res.LinesAdded++
			addedContent := strings.TrimPrefix(line, "+")
			ext := strings.ToLower(filepath.Ext(currentFile))
			if ext != ".go" && ext != ".js" && ext != ".jsx" && ext != ".ts" && ext != ".tsx" && ext != ".py" {
				currentLine++
				continue
			}

			base := filepath.Base(currentFile)
			if strings.HasSuffix(base, "_test.go") || strings.HasSuffix(base, ".test.js") || strings.HasSuffix(base, ".test.ts") || strings.HasPrefix(currentFile, "tests/") || strings.HasPrefix(currentFile, "tests\\") {
				currentLine++
				continue
			}

			// Check added content against active rules
			for _, r := range activeRules {
				// Extension match check
				if len(r.FileExts) > 0 {
					matched := false
					for _, fe := range r.FileExts {
						if ext == fe {
							matched = true
							break
						}
					}
					if !matched {
						continue
					}
				}

				if r.Regex.MatchString(addedContent) {
					finding := scanner.FindingDetail{
						RuleID:       r.RuleID,
						File:         currentFile,
						Line:         currentLine,
						Severity:     r.Severity,
						Description:  r.Description,
						LineContent:  strings.TrimSpace(addedContent),
						SuggestedFix: r.SuggestedFix,
					}
					res.NewViolations = append(res.NewViolations, finding)
					if r.Severity == "CRITICAL" || r.Severity == "HIGH" {
						res.Status = "BLOCKED"
					}
				}
			}
			currentLine++
		} else if strings.HasPrefix(line, "-") && !strings.HasPrefix(line, "---") {
			res.LinesRemoved++
		}
	}

	res.FilesInspected = len(filesSet)

	// Display 75-column Terminal Box
	borderCol := termui.Green
	if res.Status == "BLOCKED" {
		borderCol = termui.Red
	}

	fmt.Println(termui.CardBorderTop("Differential Analysis Result", borderCol, false))
	fmt.Println(termui.FormatBoxLine(fmt.Sprintf("Git Reference: %s%s%s", termui.Cyan, diffRef, termui.Reset), 67, "│", borderCol))
	fmt.Println(termui.FormatBoxLine(fmt.Sprintf("Files Inspected: %d | Lines Added: +%d | Lines Removed: -%d", res.FilesInspected, res.LinesAdded, res.LinesRemoved), 67, "│", borderCol))
	fmt.Println(termui.FormatBoxLine(fmt.Sprintf("New Security Violations: %d", len(res.NewViolations)), 67, "│", borderCol))

	if len(res.NewViolations) > 0 {
		for i, v := range res.NewViolations {
			if i >= 3 {
				fmt.Println(termui.FormatBoxLine(fmt.Sprintf("... and %d more differential violations", len(res.NewViolations)-3), 67, "│", borderCol))
				break
			}
			fmt.Println(termui.FormatBoxLine(fmt.Sprintf("%s[%s]%s %s:%d - %s", termui.Red, v.RuleID, termui.Reset, v.File, v.Line, v.Description), 67, "│", borderCol))
		}
	}

	statusText := fmt.Sprintf("%sPASSED (No blocking regressions)%s", termui.Green, termui.Reset)
	if res.Status == "BLOCKED" {
		statusText = fmt.Sprintf("%sBLOCKED (New Critical/High violations introduced)%s", termui.Red, termui.Reset)
	}
	fmt.Println(termui.FormatBoxLine(fmt.Sprintf("PR Gate Decision: %s", statusText), 67, "│", borderCol))
	fmt.Println(termui.CardBorderBottom(borderCol, false))
	fmt.Println()

	return res, nil
}
