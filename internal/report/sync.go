package report

import (
	"fmt"
	"os"
	"path/filepath"
	"time"
)

func SyncReport(targetDir string, findings []string) error {
	reportPath := filepath.Join(targetDir, "security_report.md")
	
	content := fmt.Sprintf("# TorusGuard Security Report\n\nGenerated at: %s\n\n", time.Now().Format(time.RFC3339))
	
	if len(findings) == 0 {
		content += "## Findings\n\nNo vulnerabilities found.\n"
	} else {
		content += "## Findings\n\n"
		for _, f := range findings {
			content += fmt.Sprintf("- %s\n", f)
		}
	}
	
	return os.WriteFile(reportPath, []byte(content), 0644)
}
