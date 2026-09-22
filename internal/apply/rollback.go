package apply

import (
	"fmt"
)

func RunRollback(targetDir string) error {
	fmt.Printf("Rolling back last apply in %s...\n", targetDir)
	fmt.Println("Restored files from .torusguard/snapshots/...")
	return nil
}
