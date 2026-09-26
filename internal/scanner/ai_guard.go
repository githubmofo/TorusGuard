package scanner

import (
	"bufio"
	"os"
	"path/filepath"
	"regexp"
	"strings"
)

var (
	// TG-RAG-001: RAG context concatenated into system prompt
	reSystemRagInject = regexp.MustCompile(`(?i)(role['"]?\s*:\s*['"]system['"]?[\s\S]*?(content['"]?\s*:\s*f['"][^'"]*\{[^}]*(docs|context|retrieved|chunk)[^}]*\}|content['"]?\s*:\s*` + "`" + `[^` + "`" + `]*\$\{[^}]*(docs|context|retrieved|chunk)[^}]*\}|content['"]?\s*:\s*.*?\+\s*(docs|context|retrieved|chunk)))`)
	// TG-RAG-002: Autonomous tool execution to shell without sandboxing
	reUnsandboxedTool = regexp.MustCompile(`(?i)(os\.system|subprocess\.(check_output|run|Popen)\(.*shell\s*=\s*True|child_process\.(exec|execSync))\(\s*args\s*\[['"]?(cmd|command|script)['"]?\]|(?i)(os\.system|subprocess\.(check_output|run|Popen)\(.*shell\s*=\s*True|child_process\.(exec|execSync))\(\s*tool_call`)
	// TG-RAG-003: Vector database similarity query lacking tenant filter
	reVectorSearch = regexp.MustCompile(`(?i)(similarity_search|similaritySearch|pinecone_index\.query|vector_store\.query)\(\s*(query|user_query|vector)`)
)

// ScanAIGuard scans AI applications, RAG pipelines, and agent function dispatchers for safety flaws.
func ScanAIGuard(targetDir string) ([]FindingDetail, error) {
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
		if ext != ".py" && ext != ".js" && ext != ".ts" && ext != ".tsx" && ext != ".go" {
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

			// TG-RAG-001: RAG context in system prompt
			if (strings.Contains(line, "system") || strings.Contains(line, "System")) &&
				(strings.Contains(line, "context") || strings.Contains(line, "docs") || strings.Contains(line, "retrieved") || strings.Contains(line, "chunk")) &&
				(strings.Contains(line, "{") || strings.Contains(line, "$") || strings.Contains(line, "+")) {
				if reSystemRagInject.MatchString(line) {
					ctx, _ := ExtractContext(path, lineNum, 3)
					findings = append(findings, FindingDetail{
						RuleID:       "TG-RAG-001",
						File:         relPath,
						Line:         lineNum,
						Severity:     "CRITICAL",
						Description:  "Untrusted RAG context interpolated directly into system prompt (Indirect Prompt Injection)",
						LineContent:  trimmed,
						Context:      ctx,
						SuggestedFix: "Place retrieved context in user message wrapped in explicit inert delimiters (<context>...</context>).",
					})
				}
			}

			// TG-RAG-002: Autonomous tool call unsandboxed execution
			if reUnsandboxedTool.MatchString(line) {
				ctx, _ := ExtractContext(path, lineNum, 3)
				findings = append(findings, FindingDetail{
					RuleID:       "TG-RAG-002",
					File:         relPath,
					Line:         lineNum,
					Severity:     "CRITICAL",
					Description:  "Unsandboxed shell execution of AI model tool call arguments",
					LineContent:  trimmed,
					Context:      ctx,
					SuggestedFix: "Validate tool arguments against strict schemas (Pydantic/Zod), eliminate shell=True, and require human gate.",
				})
			}

			// TG-RAG-003: Unpartitioned vector search
			if reVectorSearch.MatchString(line) && !strings.Contains(line, "filter") && !strings.Contains(line, "tenant") && !strings.Contains(line, "user_id") {
				ctx, _ := ExtractContext(path, lineNum, 3)
				findings = append(findings, FindingDetail{
					RuleID:       "TG-RAG-003",
					File:         relPath,
					Line:         lineNum,
					Severity:     "HIGH",
					Description:  "Vector database similarity search missing multi-tenant metadata partition filter",
					LineContent:  trimmed,
					Context:      ctx,
					SuggestedFix: "Add tenant_id filter to vector search query: filter={'tenant_id': user.tenant_id}.",
				})
			}
		}

		return nil
	})

	return findings, err
}
