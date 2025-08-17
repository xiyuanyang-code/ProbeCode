# PYPARSER: Python Code Structure Parser

This tool can parse Python files and extract information about classes and functions defined in them, it will be used as an MCP tool for Agents to read and understand long-context Python files.

Source Code: [`parser.py`](./parser.py)

## Features
- Parse Python files using AST (Abstract Syntax Tree).
- Extract all class definitions, all function definitions and top-level code, as well as some concrete information.
- Support both for command-line interface and module interface for MCP tool usage.

## Usage


- Command-line usage

    ```bash
    python parser.py <input_file.py>
    ```

- Module usage

    ```python
    # for interface functions
    from CodingAgent.pyparser.parser import parse_python_file

    def simple_test():
        results = parse_python_file("./CodingAgent/pyparser/example/simple.py")
        with open("./CodingAgent/pyparser/example/simple_result.json", "w") as file:
            json.dump(results, file, indent=2, ensure_ascii=False, sort_keys=True)
    ```

    ```python
    # parse_python_file is written based on class PythonStructureParser

    def parse_python_file(file_path: str) -> Optional[Dict[str, Any]]:
        """
        Parses a Python file and returns structured information about its classes,
        functions, and top-level statements.
        
        Args:
            file_path (str): Path to the Python file to parse.
            
        Returns:
            Optional[Dict[str, Any]]: Dictionary with parsed information or None
                                    if parsing failed.
        """
        parser = PythonStructureParser(file_path)
        if parser.parse_file():
            parser.extract_classes_and_functions()
            return parser.get_results()
        return None
    ```

## Return Structure

Just like the syntactic analysis parser does, this parser will use AST (abstract syntax tree) for splitting. It will be categorized into:

- Function Definition

- Class Definition

- Top Level Code: will be executed immediately in scripts

Thus the json structure is like:

```json
{
  "classes": [],
  "file_path": "/home/xiyuanyang/Agents/Coding_Agent/CodingAgent/pyparser/example/empty.py",
  "functions": [],
  "top_level_code": []
}
```

- classes: for each class is a dict, stores some detailed messages:
    - Base Class
    - Line start, Line End
        - Maintain all the source code
    - Methods: Treat functions
    - Class Name
    - Docstring

- functions: for each function is a dict, stores some detailed messages:
    - function name
    - docstring
    - args
    - return
    - line start, line end
        - Maintain all the source code

> [!WARNING]
> The storage for top level code is being refactored.

- Top Level Code
    - Stored Line by Line
    - type: `Import`, `Assign`, `If`, etc.
    - line start, line end
        - Source Code


### Example

Take [`simple.py`](./example/simple.py) as an example:

<details>

<summary> Example for simple.py </summary>

```python
import os
import sys

HELLO = "123456"

def hello():
    print("Hello world")
    i = 300

class TestClass():
    def __init__(self):
        self.time = "20250505"
    
    def run(self):
        print("This class is running!")

if __name__ == "__main__":
    test = TestClass()
    hello()
    test.run()
```

The json file after parsing looks like:

```json
{
  "classes": [
    {
      "bases": [],
      "docstring": null,
      "line_end": 15,
      "line_start": 10,
      "methods": [
        {
          "args": [
            {
              "annotation": null,
              "default": null,
              "name": "self"
            }
          ],
          "docstring": null,
          "line_end": 12,
          "line_start": 11,
          "name": "__init__",
          "returns": null,
          "source_code": "    def __init__(self):\n        self.time = \"20250505\""
        },
        {
          "args": [
            {
              "annotation": null,
              "default": null,
              "name": "self"
            }
          ],
          "docstring": null,
          "line_end": 15,
          "line_start": 14,
          "name": "run",
          "returns": null,
          "source_code": "    def run(self):\n        print(\"This class is running!\")"
        }
      ],
      "name": "TestClass",
      "source_code": "class TestClass():\n    def __init__(self):\n        self.time = \"20250505\"\n    \n    def run(self):\n        print(\"This class is running!\")"
    }
  ],
  "file_path": "./CodingAgent/pyparser/example/simple.py",
  "functions": [
    {
      "args": [],
      "docstring": null,
      "line_end": 8,
      "line_start": 6,
      "name": "hello",
      "returns": null,
      "source_code": "def hello():\n    print(\"Hello world\")\n    i = 300"
    }
  ],
  "top_level_code": [
    {
      "line_end": 1,
      "line_start": 1,
      "source_code": "import os",
      "type": "Import"
    },
    {
      "line_end": 2,
      "line_start": 2,
      "source_code": "import sys",
      "type": "Import"
    },
    {
      "line_end": 4,
      "line_start": 4,
      "source_code": "HELLO = \"123456\"",
      "type": "Assign"
    },
    {
      "line_end": 20,
      "line_start": 17,
      "source_code": "if __name__ == \"__main__\":\n    test = TestClass()\n    hello()\n    test.run()",
      "type": "If"
    }
  ]
}
```

</details>