package main

import (
	"fmt"
	"os"
	"os/exec"
	"path/filepath"

	"github.com/torusguard/torusguard/internal/termui"
)

// RunThreatModel executes the automated STRIDE threat modeling & DFD generation engine
func RunThreatModel(targetDir string) error {
	fmt.Println()
	fmt.Println(termui.CardHeader("🛡️  STRIDE THREAT MODEL & DFD", "Architectural Risk & Data Flow Mapping", "v"+Version, termui.Cyan))

	scriptPath := filepath.Join(targetDir, ".torusguard", "scripts", "stride_generator.py")
	if _, err := os.Stat(scriptPath); err != nil {
		// Fallback to relative script
		scriptPath = filepath.Join(".", ".torusguard", "scripts", "stride_generator.py")
	}

	cmd := exec.Command("python", scriptPath, targetDir)
	cmd.Dir = targetDir
	output, err := cmd.CombinedOutput()
	if err != nil {
		fmt.Printf("Threat model generation error: %v\nOutput: %s\n", err, string(output))
		return err
	}

	outReport := filepath.Join(targetDir, "SECURITY_THREAT_MODEL.md")
	fmt.Println(termui.CardBorderTop("Threat Model Generated", termui.Green, false))
	fmt.Println(termui.FormatBoxLine(fmt.Sprintf("%s✔ Interactive Mermaid DFD%s synthesized in Zone boundary graph", termui.Green, termui.Reset), 67, "│", termui.Green))
	fmt.Println(termui.FormatBoxLine(fmt.Sprintf("%s✔ STRIDE Risk Ledger%s (Spoofing, Tampering, Repudiation, etc.)", termui.Green, termui.Reset), 67, "│", termui.Green))
	fmt.Println(termui.FormatBoxLine(fmt.Sprintf("%s✔ Artifact:%s %s", termui.Cyan, termui.Reset, outReport), 67, "│", termui.Green))
	fmt.Println(termui.CardBorderBottom(termui.Green, false))
	fmt.Println()

	return nil
}
