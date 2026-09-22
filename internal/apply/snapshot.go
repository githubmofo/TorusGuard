package apply

import (
	"fmt"
	"io"
	"os"
	"path/filepath"
	"strings"
	"time"
)

func CreateSnapshot(targetDir string, filePath string) (string, error) {
	relPath, err := filepath.Rel(targetDir, filePath)
	if err != nil {
		return "", err
	}
	
	cleanRelPath := filepath.Clean(relPath)
	if strings.HasPrefix(cleanRelPath, "..") || filepath.IsAbs(cleanRelPath) {
		return "", fmt.Errorf("path traversal attempt detected: %s", filePath)
	}
	
	runID := time.Now().Format("20060102-150405")
	snapshotDir := filepath.Join(targetDir, ".torusguard", "snapshots", runID)
	
	err = os.MkdirAll(snapshotDir, 0755)
	if err != nil {
		return "", err
	}
	
	snapshotPath := filepath.Join(snapshotDir, filepath.Base(filePath)+".bak")
	
	sourceFile, err := os.Open(filePath)
	if err != nil {
		return "", err
	}
	defer sourceFile.Close()
	
	destFile, err := os.Create(snapshotPath)
	if err != nil {
		return "", err
	}
	defer destFile.Close()
	
	_, err = io.Copy(destFile, sourceFile)
	if err != nil {
		return "", err
	}
	
	fmt.Printf("Captured pre-apply snapshot for %s at %s\n", relPath, snapshotPath)
	return runID, nil
}
