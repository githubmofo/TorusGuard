package harden

import (
	"fmt"
)

func RunHarden(patchFilePath string) error {
	fmt.Printf("Formulating zero-regression remediation patch from: %s\n", patchFilePath)
	return ProcessPatch(patchFilePath)
}
