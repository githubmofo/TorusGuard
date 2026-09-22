package harden

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

const (
	MaxAdditions = 35
	MaxDeletions = 25
)

// ProcessPatch reads a unified diff patch file, counts additions and deletions,
// and enforces the Ponytail protocol.
func ProcessPatch(patchFilePath string) error {
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
