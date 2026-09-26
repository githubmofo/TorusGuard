package harden

import (
	"bufio"
	"fmt"
	"os"
	"path/filepath"
	"strings"
)

const (
	MaxAdditions = 35
	MaxDeletions = 25
)

// ProcessPatch processes either a unified diff file (.diff, .patch) or a semantic
// patch JSON file (.json), enforcing Ponytail bounds and zero security bypasses.
func ProcessPatch(patchFilePath string) error {
	// 1. Check if input is a semantic JSON patch
	if strings.HasSuffix(strings.ToLower(patchFilePath), ".json") {
		sp, err := ParseSemanticPatch(patchFilePath)
		if err == nil && sp.TargetFile != "" && sp.FindSnippet != "" {
			targetAbs := sp.TargetFile
			if !filepath.IsAbs(targetAbs) {
				targetAbs = filepath.Join(".", sp.TargetFile)
			}
			match, reflectErr := ReflectAndVerify(targetAbs, *sp)
			if reflectErr != nil {
				return fmt.Errorf("semantic reflection failed: %v", reflectErr)
			}
			fmt.Printf("Line-Level Reflection Analysis (Alibaba OpenCodeReview Hybrid Engine):\n")
			fmt.Printf("  Target File:   %s\n", sp.TargetFile)
			fmt.Printf("  Matched Lines: %d to %d\n", match.MatchedLineStart, match.MatchedLineEnd)
			fmt.Printf("  Additions:     %d / %d\n", match.Additions, MaxAdditions)
			fmt.Printf("  Deletions:     %d / %d\n", match.Deletions, MaxDeletions)
			fmt.Println("✅ Semantic patch validated against Ponytail bounds and zero bypasses.")
			return nil
		}
	}

	// 2. Standard unified diff processing
	file, err := os.Open(patchFilePath)
	if err != nil {
		return fmt.Errorf("failed to open patch file: %v", err)
	}
	defer file.Close()

	additions := 0
	deletions := 0

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		if strings.HasPrefix(line, "+++") || strings.HasPrefix(line, "---") {
			continue
		}
		if strings.HasPrefix(line, "+") {
			additions++
			if bypassRegex.MatchString(line) {
				return fmt.Errorf("security bypass detected in patch line: %s (TG-DIFF-001)", line)
			}
		} else if strings.HasPrefix(line, "-") {
			deletions++
		}
	}

	if err := scanner.Err(); err != nil {
		return fmt.Errorf("error reading patch file: %v", err)
	}

	fmt.Printf("Patch Analysis:\n")
	fmt.Printf("  Additions: %d / %d\n", additions, MaxAdditions)
	fmt.Printf("  Deletions: %d / %d\n", deletions, MaxDeletions)

	if additions > MaxAdditions || deletions > MaxDeletions {
		return fmt.Errorf("patch violates Ponytail bounds (<= %d additions, <= %d deletions)", MaxAdditions, MaxDeletions)
	}

	fmt.Println("✅ Patch conforms to Ponytail bounds. Ready to apply.")
	return nil
}
