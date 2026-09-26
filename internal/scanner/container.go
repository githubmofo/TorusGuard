package scanner

import (
	"bufio"
	"fmt"
	"os"
	"path/filepath"
	"regexp"
	"strings"
)

var (
	reDockerSock      = regexp.MustCompile(`(?i)/var/run/docker\.sock`)
	rePrivileged      = regexp.MustCompile(`(?i)(privileged:\s*true|security_opt:.*seccomp:unconfined|cap_add:.*SYS_ADMIN|cap_add:.*ALL)`)
	reContainerSecret = regexp.MustCompile(`(?i)(ARG|ENV)\s+.*(password|secret|api_key|token|private_key)\s*=\s*['"]?[a-zA-Z0-9_\-\.]{4,}['"]?`)
	reRootUser        = regexp.MustCompile(`(?i)^\s*USER\s+(root|0)\b`)
	reAnyUser         = regexp.MustCompile(`(?i)^\s*USER\s+`)
)

// ScanContainerFiles scans Dockerfiles, Containerfiles, and Docker Compose configurations.
func ScanContainerFiles(targetDir string) ([]FindingDetail, error) {
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

		base := strings.ToLower(info.Name())
		isDockerfile := strings.HasPrefix(base, "dockerfile") || strings.HasSuffix(base, ".dockerfile") || base == "containerfile"
		isCompose := strings.HasPrefix(base, "docker-compose") || base == "compose.yml" || base == "compose.yaml"

		if !isDockerfile && !isCompose {
			return nil
		}

		relPath, _ := filepath.Rel(targetDir, path)
		file, err := os.Open(path)
		if err != nil {
			return nil
		}
		defer file.Close()

		var lines []string
		hasUserDirective := false
		scanner := bufio.NewScanner(file)
		for scanner.Scan() {
			lines = append(lines, scanner.Text())
		}

		for idx, line := range lines {
			lineNum := idx + 1
			trimmed := strings.TrimSpace(line)
			if strings.HasPrefix(trimmed, "#") {
				continue
			}

			// TG-CONT-002: Docker socket mount
			if reDockerSock.MatchString(line) {
				ctx, _ := ExtractContext(path, lineNum, 3)
				findings = append(findings, FindingDetail{
					RuleID:       "TG-CONT-002",
					File:         relPath,
					Line:         lineNum,
					Severity:     "CRITICAL",
					Description:  "Dangerous Docker socket mount (/var/run/docker.sock) grants root host access",
					LineContent:  trimmed,
					Context:      ctx,
					SuggestedFix: "Remove the Docker socket mount. Use rootless container tooling or a locked-down proxy.",
				})
			}

			// TG-CONT-003: Privileged mode
			if rePrivileged.MatchString(line) {
				ctx, _ := ExtractContext(path, lineNum, 3)
				findings = append(findings, FindingDetail{
					RuleID:       "TG-CONT-003",
					File:         relPath,
					Line:         lineNum,
					Severity:     "CRITICAL",
					Description:  "Privileged container mode or unconfined seccomp profile disabled",
					LineContent:  trimmed,
					Context:      ctx,
					SuggestedFix: "Remove privileged: true and drop capabilities: cap_drop: [ALL].",
				})
			}

			// TG-CONT-004: Secret in build ARG or ENV
			if isDockerfile && reContainerSecret.MatchString(line) {
				ctx, _ := ExtractContext(path, lineNum, 3)
				findings = append(findings, FindingDetail{
					RuleID:       "TG-CONT-004",
					File:         relPath,
					Line:         lineNum,
					Severity:     "HIGH",
					Description:  "Sensitive secret or credential baked into Dockerfile ARG or ENV layer",
					LineContent:  trimmed,
					Context:      ctx,
					SuggestedFix: "Use Docker BuildKit secret mounts (RUN --mount=type=secret) or runtime env vars.",
				})
			}

			// Track USER directive
			if isDockerfile {
				if reAnyUser.MatchString(line) {
					hasUserDirective = true
					if reRootUser.MatchString(line) {
						ctx, _ := ExtractContext(path, lineNum, 3)
						findings = append(findings, FindingDetail{
							RuleID:       "TG-CONT-001",
							File:         relPath,
							Line:         lineNum,
							Severity:     "HIGH",
							Description:  "Container explicitly configured to run as root user",
							LineContent:  trimmed,
							Context:      ctx,
							SuggestedFix: "Specify an unprivileged non-root user (e.g. USER appuser or USER 10001:10001).",
						})
					}
				}
			}
		}

		// TG-CONT-001: Dockerfile missing USER directive entirely
		if isDockerfile && !hasUserDirective && len(lines) > 0 {
			ctx, _ := ExtractContext(path, len(lines), 3)
			findings = append(findings, FindingDetail{
				RuleID:       "TG-CONT-001",
				File:         relPath,
				Line:         len(lines),
				Severity:     "HIGH",
				Description:  "Dockerfile missing non-root USER directive (defaults to root)",
				LineContent:  fmt.Sprintf("(End of %s)", relPath),
				Context:      ctx,
				SuggestedFix: "Add 'RUN adduser -D appuser && USER appuser' before CMD/ENTRYPOINT.",
			})
		}

		return nil
	})

	return findings, err
}
