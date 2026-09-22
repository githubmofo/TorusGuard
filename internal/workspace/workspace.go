package workspace

import (
	"fmt"
	"os"
	"path/filepath"
)

// InitWorkspace creates the .torusguard directory and standard files
func InitWorkspace(target string) error {
	tgDir := filepath.Join(target, ".torusguard")
	
	if _, err := os.Stat(tgDir); os.IsNotExist(err) {
		err := os.MkdirAll(filepath.Join(tgDir, "rules"), 0755)
		if err != nil {
			return err
		}
		err = os.MkdirAll(filepath.Join(tgDir, "snapshots"), 0755)
		if err != nil {
			return err
		}
		
		fmt.Printf("Initialized empty TorusGuard workspace in %s\n", tgDir)
	} else {
		fmt.Printf("TorusGuard workspace already exists in %s\n", tgDir)
	}
	
	return nil
}

// DetectStack determines the primary languages/frameworks in the target
func DetectStack(target string) ([]string, error) {
	var stack []string
	
	if _, err := os.Stat(filepath.Join(target, "package.json")); err == nil {
		stack = append(stack, "Node.js")
	}
	if _, err := os.Stat(filepath.Join(target, "go.mod")); err == nil {
		stack = append(stack, "Go")
	}
	if _, err := os.Stat(filepath.Join(target, "requirements.txt")); err == nil {
		stack = append(stack, "Python")
	}
	
	return stack, nil
}
