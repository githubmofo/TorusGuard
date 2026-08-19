import os

validation_file = r"c:\Users\Admin\Desktop\New folder\docs\validation\nodegoat-v0.3.0-validation.md"

text_to_append = """
## NodeGoat Dependency Experiment
`npm audit fix --force` was tested separately on the NodeGoat workspace. It resolved some dependency findings but introduced or exposed major version migrations involving core packages such as Express and MongoDB. These changes are not included in the TorusGuard v0.3.0 release and are not treated as a validated NodeGoat remediation. They require a separate compatibility and refactoring project.
"""

with open(validation_file, "a", encoding="utf-8") as f:
    f.write(text_to_append)

print("Validation file updated.")
