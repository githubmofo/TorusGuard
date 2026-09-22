package rules

import (
	"encoding/json"
	"os"
	"path/filepath"
)

type Rule struct {
	ID          string   `json:"id"`
	Description string   `json:"description"`
	Severity    string   `json:"severity"`
	Patterns    []string `json:"patterns"`
}

type Catalog struct {
	Rules []Rule `json:"rules"`
}

func LoadRules(workspaceDir string) (*Catalog, error) {
	catalogPath := filepath.Join(workspaceDir, "rules_catalog.json")
	
	if _, err := os.Stat(catalogPath); os.IsNotExist(err) {
		// return empty catalog if not found
		return &Catalog{}, nil
	}
	
	data, err := os.ReadFile(catalogPath)
	if err != nil {
		return nil, err
	}
	
	var catalog Catalog
	if err := json.Unmarshal(data, &catalog); err != nil {
		return nil, err
	}
	
	return &catalog, nil
}
