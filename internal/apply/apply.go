package apply

import (
	"bufio"
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
)

func getTargetFileFromPatch(patchFilePath string) (string, error) {
	file, err := os.Open(patchFilePath)
	if err != nil {
		return "", err
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		if strings.HasPrefix(line, "--- a/") {
			return strings.TrimPrefix(line, "--- a/"), nil
		}
	}
	return "", fmt.Errorf("could not detect target file in patch")
}

func RunApply(patchFilePath string, targetDir string, autoYes bool) error {
	fmt.Printf("Applying remediation patch from %s...\n", patchFilePath)

	if !autoYes {
		fmt.Println("Human Gate: Requires explicit --yes to apply patches.")
		return nil
	}

	targetFile, err := getTargetFileFromPatch(patchFilePath)
	if err != nil {
		return fmt.Errorf("invalid patch file: %v", err)
	}
	
	targetFilePath := filepath.Join(targetDir, targetFile)

	if _, err := os.Stat(targetFilePath); os.IsNotExist(err) {
		return fmt.Errorf("target file %s does not exist", targetFile)
	}

	// Create snapshot
	runID, err := CreateSnapshot(targetDir, targetFilePath)
	if err != nil {
		fmt.Printf("Warning: Failed to capture snapshot: %v\n", err)
	} else {
		fmt.Printf("✔ Pre-apply snapshot captured (Run ID: %s)\n", runID)
	}

	// Apply patch using git apply
	cmd := exec.Command("git", "apply", patchFilePath)
	cmd.Dir = targetDir
	
	if output, err := cmd.CombinedOutput(); err != nil {
		fmt.Printf("❌ Failed to apply patch: %v\nOutput: %s\n", err, output)
		return fmt.Errorf("patch application failed")
	}

	fmt.Println("✔ Golden Fix successfully applied.")
	return nil
}
