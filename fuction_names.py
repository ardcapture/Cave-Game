import ast
from typing import List


def extract_functions(filename: str) -> List[str]:
    with open(filename, "r") as file:
        code = file.read()

    tree = ast.parse(code)

    function_names: List[str] = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            function_names.append(node.name)

    return function_names


if __name__ == "__main__":
    filename = "src\\level.py"  # Replace with the name of your Python file
    function_names = extract_functions(filename)

    print("List of functions in the file:")
    for name in function_names:
        print(name)
