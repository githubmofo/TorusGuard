package scanner

import (
	"bufio"
	"context"
	"os"
	"os/exec"
	"path/filepath"
	"regexp"
	"strings"
	"time"
)

var (
	reGitCreds   = regexp.MustCompile(`https?://[^:]+:[^@]+@`)
	reGitSecret  = regexp.MustCompile(`\b(sk-(?:live-)?[a-zA-Z0-9_\-\.]{20,}|AKIA[0-9A-Z]{16}|ghp_[a-zA-Z0-9]{36})\b`)
	reGitKeyFile = regexp.MustCompile(`(?i)(\.env|\.env\.local|id_rsa|id_ed25519|.*\.pem|.*\.key|.*\.p12)$`)
)

// ScanGitHistory performs deep inspection of Git repository metadata, config, and commit logs.
func ScanGitHistory(targetDir string) ([]FindingDetail, error) {
	var findings []FindingDetail

	gitDir := filepath.Join(targetDir, ".git")
	if info, err := os.Stat(gitDir); err != nil || !info.IsDir() {
		// Not a git repository, skip gracefully
		return findings, nil
	}

	// 1. Audit .git/config for embedded plaintext credentials
	configPath := filepath.Join(gitDir, "config")
	if file, err := os.Open(configPath); err == nil {
		scanner := bufio.NewScanner(file)
		lineNum := 0
		for scanner.Scan() {
			lineNum++
			line := scanner.Text()
			if reGitCreds.MatchString(line) {
				findings = append(findings, FindingDetail{
					RuleID:       "TG-GIT-002",
					File:         ".git/config",
					Line:         lineNum,
					Severity:     "HIGH",
					Description:  "Plaintext credentials detected in Git remote URL configuration",
					LineContent:  strings.TrimSpace(reGitCreds.ReplaceAllString(line, "https://***:***@")),
					Context:      "  Remote URL contains embedded username and password / token",
					SuggestedFix: "Remove credentials from remote URL: git remote set-url origin <clean_url> and use a credential helper.",
				})
			}
		}
		file.Close()
	}

	// 2. Audit tracked files for sensitive names
	_ = filepath.Walk(targetDir, func(path string, info os.FileInfo, err error) error {
		if err != nil || info.IsDir() {
			if info != nil && info.IsDir() {
				name := info.Name()
				if name == "node_modules" || name == ".git" || name == ".torusguard" {
					return filepath.SkipDir
				}
			}
			return nil
		}

		base := info.Name()
		if reGitKeyFile.MatchString(base) {
			relPath, _ := filepath.Rel(targetDir, path)
			// Check if file is tracked by git
			cmd := exec.Command("git", "ls-files", "--error-unmatch", relPath)
			cmd.Dir = targetDir
			if err := cmd.Run(); err == nil {
				// File is tracked by git!
				ctx, _ := ExtractContext(path, 1, 2)
				findings = append(findings, FindingDetail{
					RuleID:       "TG-GIT-003",
					File:         relPath,
					Line:         1,
					Severity:     "HIGH",
					Description:  "Sensitive secret file tracked in Git index despite .gitignore policy",
					LineContent:  relPath,
					Context:      ctx,
					SuggestedFix: "Untrack file from git: git rm --cached " + relPath + " and ensure it is in .gitignore.",
				})
			}
		}
		return nil
	})

	// 3. Scan recent commit history (last 50 commits) for leaked secrets in commit diffs
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	cmd := exec.CommandContext(ctx, "git", "log", "-n", "50", "-p", "--unified=1")
	cmd.Dir = targetDir
	output, err := cmd.Output()
	if err == nil {
		scanner := bufio.NewScanner(strings.NewReader(string(output)))
		currentCommit := "unknown"
		currentFile := "git-log"

		for scanner.Scan() {
			line := scanner.Text()
			if strings.HasPrefix(line, "commit ") {
				parts := strings.Fields(line)
				if len(parts) >= 2 {
					currentCommit = parts[1]
					if len(currentCommit) > 8 {
						currentCommit = currentCommit[:8]
					}
				}
			} else if strings.HasPrefix(line, "diff --git a/") {
				parts := strings.Fields(line)
				if len(parts) >= 3 {
					currentFile = strings.TrimPrefix(parts[2], "a/")
				}
			} else if strings.HasPrefix(line, "+") && !strings.HasPrefix(line, "+++") {
				addedContent := strings.TrimPrefix(line, "+")
				if match := reGitSecret.FindString(addedContent); match != "" {
					redacted := match[:4] + "..." + match[len(match)-4:]
					findings = append(findings, FindingDetail{
						RuleID:       "TG-GIT-001",
						File:         currentFile,
						Line:         1,
						Severity:     "CRITICAL",
						Description:  "Historical secret detected in Git commit " + currentCommit + ": " + redacted,
						LineContent:  strings.TrimSpace(addedContent),
						Context:      "  Commit " + currentCommit + " added credential matching " + redacted,
						SuggestedFix: "Revoke token immediately and purge history with: git-filter-repo --invert-paths --path " + currentFile,
					})
				}
			}
		}
	}

	return findings, nil
}
