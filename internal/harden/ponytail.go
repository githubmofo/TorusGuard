package harden

import (
	"fmt"
)

type Patch struct {
	FilePath    string
	Additions   int
	Deletions   int
	Content     string
}

// VerifyPonytailBounds ensures that patches comply with the Ponytail Protocol
func VerifyPonytailBounds(p Patch) error {
	if p.Additions > 35 {
		return fmt.Errorf("patch exceeds Ponytail bounds: %d additions (max 35)", p.Additions)
	}
	if p.Deletions > 25 {
		return fmt.Errorf("patch exceeds Ponytail bounds: %d deletions (max 25)", p.Deletions)
	}
	return nil
}
