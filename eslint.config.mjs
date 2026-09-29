export default [
  {
    ignores: ["**/*.py", "**/*.go", ".torusguard/**", "node_modules/**"]
  },
  {
    files: ["**/*.js", "**/*.mjs"],
    rules: {
      "no-unused-vars": "off"
    }
  }
];
