# Heligrafics Odoo pre-commit hooks

A collection of pre-commit hooks for Odoo projects, developed by Heligrafics S.L.

## Available Hooks

- **odoo-method-order**: Validates that methods and attributes in Odoo models follow a logical and predefined order to improve code readability and maintainability.

## Quick Installation and Usage

1. **Install dependencies:**
   ```bash
   pip install .[test]
   ```

2. **Install pre-commit in your repository:**
   ```bash
   pre-commit install
   ```

3. **Run hooks manually (optional):**
   ```bash
   pre-commit run --all-files
   ```

## Usage notes

- The `odoo-method-order` hook/script accepts an optional `--exit-zero` argument.
  If provided, the script will always return exit code 0, even if errors are found.
  This can be useful for CI or exploratory runs where you want to see warnings but not fail the pipeline.

- The script now reports **all ordering errors** found in a file, not just the first one. This helps to quickly identify and fix all method ordering issues in your Odoo models.

### Example usage

```bash
python src/hg_odoo_pre_commit_hooks/check_method_order.py --exit-zero path/to/your/model.py
```

## Development

- Hooks are located in the `src/` directory.
- Automated tests are in the `tests/` directory.
- Example modules for testing are in `test_repo/`.

## Running Tests

You can run the tests with:

```bash
pytest
```

Or using tox (to test in different environments):

```bash
tox
```

## Repository Structure

- `src/`: Source code for the hooks.
- `tests/`: Automated tests validating hook behavior.
- `test_repo/`: Example Odoo modules (both correct and intentionally incorrect) used in tests.
  - `method_ordered_module/`: Example Odoo module with correctly ordered methods.
  - `method_not_ordered_module/`: Example Odoo module with unordered methods to trigger errors.
- `.pre-commit-config.yaml`: Pre-commit hook configuration.
- `.pre-commit-hooks.yaml`: Local hook definitions.
- Other configuration files: `.editorconfig`, `.ruff.toml`, `.pylintrc`, etc.

## Example `.pre-commit-config.yaml` Configuration

```yaml
- repo: https://github.com/heligrafics/odoo-pre-commit-hooks
   rev: main
   hooks:
   - id: odoo-method-order
```

## Contributing

1. Create a branch for your feature or fix.
2. Ensure all tests pass.
3. Submit a pull request with a clear description of your contribution.

---

Heligrafics S.L.
