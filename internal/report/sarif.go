package report

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
)

type SarifReport struct {
	Version string `json:"version"`
	Runs    []Run  `json:"runs"`
}

type Run struct {
	Tool    Tool     `json:"tool"`
	Results []Result `json:"results"`
}

type Tool struct {
	Driver Driver `json:"driver"`
}

type Driver struct {
	Name    string `json:"name"`
	Version string `json:"version"`
}

type Result struct {
	Message Message `json:"message"`
	Level   string  `json:"level"`
}

type Message struct {
	Text string `json:"text"`
}

func GenerateSARIFReport(targetDir string, findings []string) error {
	fmt.Printf("Generating dynamic SARIF v2.1.0 report for %s...\n", targetDir)

	results := []Result{}
	for _, f := range findings {
		// Ignore the "No active findings detected" message if real findings exist,
		// but if it's the only one, we can map it as a note or omit it.
		level := "warning"
		if f == "No active findings detected. Posture is secure." {
			level = "note"
		}
		
		results = append(results, Result{
			Message: Message{Text: f},
			Level:   level,
		})
	}

	report := SarifReport{
		Version: "2.1.0",
		Runs: []Run{
			{
				Tool: Tool{
					Driver: Driver{
						Name:    "TorusGuard",
						Version: "2.0.0-alpha",
					},
				},
				Results: results,
			},
		},
	}

	sarifPath := filepath.Join(targetDir, "report.sarif")
	data, err := json.MarshalIndent(report, "", "  ")
	if err != nil {
		return err
	}

	if err := os.WriteFile(sarifPath, data, 0644); err != nil {
		return err
	}

	fmt.Printf("✔ Dynamic SARIF report generated at %s\n", sarifPath)
	return nil
}
