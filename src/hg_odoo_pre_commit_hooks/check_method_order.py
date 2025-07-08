"""check_method_order.py

Verifica que los métodos y atributos dentro de las clases sigan un orden predefinido.
Está diseñado principalmente para asegurar la consistencia en la organización
del código, especialmente en módulos de Heligrafics.

Funciones principales:
- Analiza la definición de clases en un archivo Python.
- Clasifica los métodos y atributos según categorías predefinidas.
- Verifica que el orden de aparición de estas categorías sea el esperado.
- Reporta errores si se detectan métodos o atributos fuera de orden o con
categorías desconocidas.

Uso:
    python check_method_order.py archivo1.py archivo2.py ...

Categorías esperadas:
    - private_attributes
    - default_methods
    - field_declarations
    - sql_constraints
    - selection_computed_methods
    - compute_inverse_search
    - constraints_methods
    - onchange_methods
    - crud_methods
    - action_methods
    - other_methods

Salida:
    Imprime advertencias en la consola si se detectan métodos fuera de orden o
    categorías desconocidas.
    Devuelve un código de salida 1 si hay errores, 0 si todo está correcto.
"""

import argparse
import ast
import sys

EXPECTED_ORDER = [
    "private_attributes",
    "field_declarations",
    "sql_constraints",
    "default_methods",
    "selection_computed_methods",
    "compute_inverse_search",
    "constraints_methods",
    "onchange_methods",
    "crud_methods",
    "action_methods",
    "other_methods",
]

CRUD_METHODS = [
    "create",
    "write",
    "unlink",
    "copy",
    "read",
    "search",
    "search_count",
    "name_get",
    "name_search",
    "toggle_active",
]

MODELS_BASES = ("Model", "AbstractModel", "TransientModel")


def is_field_assignment(node):
    """Determina si un nodo AST representa una asignación a un campo.

    Args:
        node (ast.AST): Nodo del árbol de sintaxis abstracta a analizar.
    Returns:
        bool: True si el nodo es una asignación a un campo, False en caso contrario.
    """

    if not isinstance(node, ast.Assign):
        return False
    value = node.value
    if isinstance(value, ast.Call):
        if isinstance(value.func, ast.Attribute):
            return value.func.value.id == "fields"
    return False


def get_decorator_name(d):
    """Extracts the name of a decorator from an AST node."""
    if isinstance(d, ast.Name):
        return d.id
    if isinstance(d, ast.Attribute):
        return d.attr
    if isinstance(d, ast.Call):
        if isinstance(d.func, ast.Name):
            return d.func.id
        if isinstance(d.func, ast.Attribute):
            return d.func.attr
        return ""
    return getattr(d, "attr", "")


def get_method_category(node):
    """Clasifica un nodo AST que representa un método o asignación en una
    categoría específica.

    Args:
        node (ast.AST): Nodo del árbol de sintaxis abstracta (AST) que representa
        un método o una asignación en una clase.

    Returns:
        str: Categoría del método o asignación. Puede ser uno de los siguientes
        valores: EXPECTED_ORDER
    """

    name = getattr(node, "name", "")
    decorators = [get_decorator_name(d) for d in getattr(node, "decorator_list", [])]

    if isinstance(node, ast.Assign):
        targets = [t.id for t in node.targets if isinstance(t, ast.Name)]
        if any(t == "_sql_constraints" for t in targets):
            return "sql_constraints"
        if any(t.startswith("_") for t in targets):
            return "private_attributes"
        if is_field_assignment(node):
            return "field_declarations"
        return "other_methods"

    if name in ("default_get", "default") or name.startswith("_default_"):
        return "default_methods"
    if name.startswith("_domain_") or name.startswith("_selection_"):
        return "selection_computed_methods"
    if (
        name.startswith("_compute_")
        or name.startswith("_inverse_")
        or name.startswith("_search_")
    ):
        return "compute_inverse_search"
    if "constraints" in decorators:
        return "constraints_methods"
    if "onchange" in decorators or name.startswith("_onchange_"):
        return "onchange_methods"
    if name in CRUD_METHODS:
        return "crud_methods"
    if name.startswith("action_"):
        return "action_methods"
    return "other_methods"


def check_order(method_order, filepath):
    """Verifica que el orden de los métodos en una lista siga el orden esperado de
    categorías.

    Args:
        method_order (list): Lista de tuplas que representan los métodos, donde
            cada tupla contiene
            (categoría, número de línea, nombre del método).
        filepath (str): Ruta al archivo que contiene los métodos.
    Returns:
        bool: True si el orden de los métodos es correcto según las categorías
              esperadas, False en caso contrario.

    Imprime mensajes de advertencia si encuentra una categoría desconocida o si
    un método está fuera de orden.
    """

    current_max_index = -1
    errors_found = False
    for index_method, method_data in enumerate(method_order):
        cat, lineno, name = method_data
        try:
            idx = EXPECTED_ORDER.index(cat)
        except ValueError:
            print(f"{filepath}:{lineno}: Unknown category '{cat}' in '{name}'")
            errors_found = True
            continue
        if idx < current_max_index:
            expected_before = EXPECTED_ORDER[current_max_index]
            prev_method = method_order[index_method - 1]
            print(
                f"{filepath}:{lineno}: '{name}' (category '{cat}') appears out "
                f"of order. Should be before '{expected_before}' (before "
                f"'{prev_method[0]}->{prev_method[2]}:{prev_method[1]}')"
            )
            errors_found = True
        else:
            current_max_index = idx
    return not errors_found


def analyze_file(filepath):
    """Analiza un archivo Python para determinar el orden de los métodos dentro
    de las clases.

    Si hay más de un modelo Odoo en el archivo, reporta un error y verifica el
    orden de métodos por clase, no globalmente.

    Args:
        filepath (str): Ruta al archivo Python que se va a analizar.

    Returns:
        bool: True si el orden es correcto y no hay múltiples modelos, False
            en caso contrario.
    """

    with open(filepath, encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=filepath)

    model_classes = []
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and any(
            (
                (
                    isinstance(base, ast.Attribute)
                    and base.attr in MODELS_BASES
                    and getattr(base.value, "id", "") == "models"
                )
                or (isinstance(base, ast.Name) and base.id in MODELS_BASES)
            )
            for base in node.bases
        ):
            model_classes.append(node)

    errors_found = False
    if len(model_classes) > 1:
        print(
            f"{filepath}: ERROR: Multiple Odoo models found in the same file "
            f"({len(model_classes)} classes)."
        )
        errors_found = True

    for node in model_classes:
        method_order = []
        for subnode in node.body:
            # Ignora docstrings o expresiones solitarias
            if isinstance(subnode, ast.Expr) and isinstance(
                subnode.value,
                ast.Str | ast.Constant,
            ):
                continue
            cat = get_method_category(subnode)
            name = getattr(subnode, "name", None)
            if not name and isinstance(subnode, ast.Assign):
                name = subnode.targets[0].id
            method_order.append((cat, subnode.lineno, name or "<unnamed>"))
        if not check_order(method_order, filepath):
            errors_found = True

    return not errors_found


def main():
    parser = argparse.ArgumentParser(description="Check Odoo method order.")
    parser.add_argument(
        "--exit-zero",
        action="store_true",
        help="Always return exit code 0 (even if errors are found).",
    )
    parser.add_argument("files", nargs="+", help="Python files to check.")
    args = parser.parse_args()

    success = True
    for filepath in args.files:
        if not analyze_file(filepath):
            success = False
    if not success and not args.exit_zero:
        sys.exit(1)


if __name__ == "__main__":
    main()
