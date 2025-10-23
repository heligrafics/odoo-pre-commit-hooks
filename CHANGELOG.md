## v0.4.0 (2025-10-23)

### Feat

- **method-order**: Add support for 'init' method category and include init_method in validation
- **field_declarations**: Add regex support for field assignment validation and update tests for new model

### Fix

- Correct spelling of 'constraints' to 'constrains' in method categories
- **get_method_category**: Remove redundant check for 'constraints' in decorators

## v0.3.0 (2025-07-09)

### Feat

- **odoo-method-order**: Enhance method order analysis to handle multiple Odoo models in a single file

### Fix

- **odoo-method-order**: 'Name' object has no attribute 'attr'

## v0.2.0 (2025-06-20)

### Feat

- **odoo-method-order**: Enhance method order checker to report all errors and add tests
- **odoo-method-order**: Add --exit-zero option to method order checker and corresponding tests

## v0.1.0 (2025-06-18)

### Feat

- **odoo-method-order**:  Add pre-commit hooks and method order validation for Odoo modules
