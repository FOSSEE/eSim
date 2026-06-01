### Related Issues

<!-- Link to the issues that are solved with this PR (e.g. Closes #123) -->

### Purpose

<!--- Describe the problem or feature. -->

### Approach

<!--- How does this address the problem? -->

### 🛡️ Pre-Merge Contributor Checklist

Please verify that your PR fulfills all the following mandatory requirements before requesting review:

- [ ] **Changelog**: I have documented my changes under the `[Unreleased]` section in `CHANGELOG.md`. *(Mandatory for all code modifications)*
- [ ] **Tests**: I have added unit or integration tests verifying my changes.
- [ ] **Lints & Style**: I have run `ruff check .` locally and resolved all formatting or style violations.
- [ ] **Type Check**: I have verified my type annotations pass local type checking hooks.
- [ ] **Conventional Commits**: My commits follow the standard semantic guidelines (e.g. `feat:`, `fix:`, `docs:`, `test:`).
- [ ] **Security Scan**: I have confirmed that no insecure functions (`eval`, unescaped `subprocess.call` with `shell=True`) were introduced.
