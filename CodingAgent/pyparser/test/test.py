"""
Test the backward compatibility of the unified parser
"""

import sys
import os
import json

sys.path.append(os.getcwd())

from CodingAgent.pyparser.parser import parse_python_file

def simple_test():
    results = parse_python_file("./CodingAgent/pyparser/example/simple.py")
    with open("./CodingAgent/pyparser/example/simple_result.json", "w") as file:
        json.dump(results, file, indent=2, ensure_ascii=False, sort_keys=True)

def empty_test():
    results = parse_python_file("./CodingAgent/pyparser/example/empty.py")
    with open("./CodingAgent/pyparser/example/empty_result.json", "w") as file:
        json.dump(results, file, indent=2, ensure_ascii=False, sort_keys=True)
    

def example_test():
    # Parse a Python file and get structured information
    results = parse_python_file("./CodingAgent/pyparser/example/example.py")

    with open("./CodingAgent/pyparser/example/example_result.json", "w") as file:
        json.dump(results, file, indent=2, ensure_ascii=False, sort_keys=True)

    # Access the results
    # the print part is for debugging only, for MCP usage, it will read result (serialized text) or load a slice from a json file each time
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


def another_test():
    file_path = "/home/xiyuanyang/anaconda3/lib/python3.12/site-packages/camel/agents/chat_agent.py"
    # switch to yours for testing
    result = parse_python_file(file_path)

    with open("./CodingAgent/pyparser/example/another_result.json", "w") as file:
        json.dump(result, file, indent=2, ensure_ascii=False, sort_keys=True)


if __name__ == "__main__":
    simple_test()
    empty_test()
    example_test()
    another_test()
