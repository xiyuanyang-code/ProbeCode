#!/usr/bin/env python3
"""
Test the backward compatibility of the unified parser
"""

import sys
import os
import json

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from CodingAgent.pyparser.parser import parse_python_file


def test_backward_compatibility():
    """Test that the old parse_python_file function still works"""
    # Parse a Python file and get structured information
    results = parse_python_file("./CodingAgent/pyparser/example/example.py")

    with open("./CodingAgent/pyparser/result/result_test1.json", "w") as file:
        json.dump(results, file, indent=2, ensure_ascii=False, sort_keys=True)

    # Access the results
    if results:
        print(f"File: {results['file_path']}")
        print(f"Classes found: {len(results['classes'])}")
        print(f"Functions found: {len(results['functions'])}")

        # Access class information
        for cls in results["classes"]:
            print(f"Class: {cls['name']}")
            print(f"  Docstring: {cls['docstring']}")
            print(f"  Methods: {len(cls['methods'])}")

        # Access function information
        for func in results["functions"]:
            print(f"Function: {func['name']}")
            print(f"  Docstring: {func['docstring']}")


if __name__ == "__main__":
    test_backward_compatibility()
