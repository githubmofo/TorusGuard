package harden

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"regexp"
	"strings"
)

// SemanticPatch represents an AI-generated structured patch using Alibaba OpenCodeReview's
// reflection pattern: semantic target matching instead of error-prone line-number guessing.
type SemanticPatch struct {
	TargetFile     string `json:"target_file"`
	RuleID         string `json:"rule_id,omitempty"`
	FindSnippet    string `json:"find_snippet"`
	ReplaceSnippet string `json:"replace_snippet"`
	Rationale      string `json:"rationale,omitempty"`
}

// ReflectionMatch captures the result of matching a semantic snippet against live source code.
type ReflectionMatch struct {
	MatchedLineStart int
	MatchedLineEnd   int
	Additions        int
	Deletions        int
	UnifiedDiff      string
	NewContent       string
}

var bypassRegex = regexp.MustCompile(`(?i)(#\s*nosec|verify\s*=\s*False|InsecureSkipVerify:\s*true|csrf\(\)\.disable\(\)|\[AllowAnonymous\]|CURLOPT_SSL_VERIFYPEER\s*=>\s*false)`)

// ReflectAndVerify locates findSnippet in targetFilePath, computes Ponytail additions/deletions,
// verifies zero security bypasses, and returns a verified ReflectionMatch.
func ReflectAndVerify(targetFilePath string, patch SemanticPatch) (*ReflectionMatch, error) {
	if patch.FindSnippet == "" {
		return nil, fmt.Errorf("find_snippet cannot be empty")
	}

	// Verify zero security bypasses in replacement
	if bypassRegex.MatchString(patch.ReplaceSnippet) {
		return nil, fmt.Errorf("security bypass detected in replacement: %s (TG-DIFF-001)", patch.ReplaceSnippet)
	}

	contentBytes, err := os.ReadFile(targetFilePath)
	if err != nil {
		return nil, fmt.Errorf("failed to read target file %s: %v", targetFilePath, err)
	}
	content := string(contentBytes)

	// Clean carriage returns for universal line splitting
	cleanContent := strings.ReplaceAll(content, "\r\n", "\n")
	cleanFind := strings.ReplaceAll(patch.FindSnippet, "\r\n", "\n")
	cleanReplace := strings.ReplaceAll(patch.ReplaceSnippet, "\r\n", "\n")

	// 1. Exact match attempt
	idx := strings.Index(cleanContent, cleanFind)
	if idx == -1 {
		// 2. Whitespace-trimmed line-by-line fallback
		findTrimmed := strings.TrimSpace(cleanFind)
		idx = strings.Index(cleanContent, findTrimmed)
		if idx == -1 {
			return nil, fmt.Errorf("reflection failure: find_snippet could not be located in %s", targetFilePath)
		}
		cleanFind = findTrimmed
	}

	// Calculate line numbers
	prefix := cleanContent[:idx]
	startLine := strings.Count(prefix, "\n") + 1
	findLinesCount := strings.Count(cleanFind, "\n")
	endLine := startLine + findLinesCount

	// Calculate additions and deletions
	findLines := strings.Split(cleanFind, "\n")
	replaceLines := strings.Split(cleanReplace, "\n")

	deletions := len(findLines)
	additions := len(replaceLines)

	// Verify Ponytail Protocol bounds (<= 35 additions, <= 25 deletions)
	if additions > MaxAdditions {
		return nil, fmt.Errorf("patch violates Ponytail bounds: %d additions (max %d)", additions, MaxAdditions)
	}
	if deletions > MaxDeletions {
		return nil, fmt.Errorf("patch violates Ponytail bounds: %d deletions (max %d)", deletions, MaxDeletions)
	}

	// Build new file content
	newContent := cleanContent[:idx] + cleanReplace + cleanContent[idx+len(cleanFind):]

	// Format simulated unified diff
	var diffBuilder strings.Builder
	diffBuilder.WriteString(fmt.Sprintf("--- a/%s\n", filepath.ToSlash(patch.TargetFile)))
	diffBuilder.WriteString(fmt.Sprintf("+++ b/%s\n", filepath.ToSlash(patch.TargetFile)))
	diffBuilder.WriteString(fmt.Sprintf("@@ -%d,%d +%d,%d @@\n", startLine, deletions, startLine, additions))
	for _, l := range findLines {
		diffBuilder.WriteString(fmt.Sprintf("-%s\n", l))
	}
	for _, l := range replaceLines {
		diffBuilder.WriteString(fmt.Sprintf("+%s\n", l))
	}

	return &ReflectionMatch{
		MatchedLineStart: startLine,
		MatchedLineEnd:   endLine,
		Additions:        additions,
		Deletions:        deletions,
		UnifiedDiff:      diffBuilder.String(),
		NewContent:       newContent,
	}, nil
}

// ParseSemanticPatch reads a JSON or structured file representing a SemanticPatch.
func ParseSemanticPatch(filePath string) (*SemanticPatch, error) {
	data, err := os.ReadFile(filePath)
	if err != nil {
		return nil, fmt.Errorf("failed to read patch file %s: %v", filePath, err)
	}

	var sp SemanticPatch
	if err := json.Unmarshal(data, &sp); err != nil {
		return nil, fmt.Errorf("file is not valid semantic patch JSON: %v", err)
	}

	return &sp, nil
}
