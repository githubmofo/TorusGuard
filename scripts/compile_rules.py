import os
import json
import re

RULES_DIR = ".torusguard/rules"
OUTPUT_FILE = ".torusguard/rules_catalog.json"

def get_default_patterns(rule_id):
    if "SEC" in rule_id:
        return [r"(?i)(password|secret|api[_-]?key|token)\s*=\s*['\"][a-zA-Z0-9_\-]{8,}['\"]"]
    elif "DB" in rule_id:
        return [r"(?i)(select\s+\*|exec\s+|execute\s+|raw\s*\(|query\s*\()"]
    elif "INPUT" in rule_id:
        return [r"(?i)(eval\s*\(|exec\s*\(|system\s*\(|child_process|innerHTML)"]
    elif "AUTH" in rule_id:
        return [r"(?i)(jwt\.sign|md5|sha1|verify.*false)"]
    elif "PLATFORM" in rule_id:
        return [r"(?i)(cors.*\*|app\.disable\('x-powered-by'\))"]
    return [r"(?i)(vulnerable_function\(\))"]

def compile_rules():
    catalog = {"rules": []}
    
    if not os.path.exists(RULES_DIR):
        print(f"Rules directory {RULES_DIR} not found.")
        return
        
    for filename in os.listdir(RULES_DIR):
        if not filename.endswith(".md") or filename.upper() == "README.md":
            continue
            
        filepath = os.path.join(RULES_DIR, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Parse ID from # TG-XXX-000: Title
        id_match = re.search(r'#\s*(TG-[A-Z]+-\d+)', content)
        rule_id = id_match.group(1) if id_match else filename.replace(".md", "")
        
        # Description
        desc_match = re.search(r'#\s*TG-[A-Z]+-\d+:\s*(.*)', content)
        description = desc_match.group(1).strip() if desc_match else "Security Rule"
        
        # Severity
        sev_match = re.search(r'## Severity\s*\n\s*(Critical|High|Medium|Low)', content, re.IGNORECASE)
        severity = sev_match.group(1).capitalize() if sev_match else "High"
        
        catalog["rules"].append({
            "id": rule_id,
            "description": description,
            "severity": severity,
            "patterns": get_default_patterns(rule_id)
        })

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(catalog, f, indent=2)
        
    print(f"Compiled {len(catalog['rules'])} rules into {OUTPUT_FILE}")

if __name__ == "__main__":
    compile_rules()
