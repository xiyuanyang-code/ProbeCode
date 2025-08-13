# PYPARSER: Python Code Structure Parser

This tool can parse Python files and extract information about classes and functions defined in them.

## Features
- Parse Python files using AST (Abstract Syntax Tree)
- Extract all class definitions and their information
- Extract all function definitions and their information
- Extract docstrings for classes and functions
- Support for command-line interface
- Module interface for programmatic usage
- Unified class with both programmatic access and console output capabilities

## Usage

### Command-line usage

```bash
python unified_parser.py <input_file.py>
```

### Module usage

```python
from unified_parser import PythonStructureParser

# Create parser instance
parser = PythonStructureParser("example.py")

# Parse the file
if parser.parse_file():
    parser.extract_classes_and_functions()
    
    # Get results without printing to console
    results = parser.get_results()
    
    # Access the results
    print(f"File: {results['file_path']}")
    print(f"Classes found: {len(results['classes'])}")
    print(f"Functions found: {len(results['functions'])}")
    
    # Access class information
    for cls in results['classes']:
        print(f"Class: {cls['name']}")
        print(f"  Docstring: {cls['docstring']}")
        print(f"  Methods: {len(cls['methods'])}")
        
    # Access function information
    for func in results['functions']:
        print(f"Function: {func['name']}")
        print(f"  Docstring: {func['docstring']}")

# Or print results directly to console
parser.print_results()
```

## Return Structure
The `get_results()` method returns a dictionary with the following structure:
```python
{
    'file_path': str,           # Path to the parsed file
    'classes': [                # List of class information
        {
            'name': str,        # Class name
            'line_start': int,  # Starting line number
            'line_end': int,    # Ending line number
            'methods': [...],   # List of method information (same structure as functions)
            'bases': [...],     # List of base classes
            'docstring': str    # Class docstring (if any)
        }
    ],
    'functions': [              # List of function information
        {
            'name': str,        # Function name
            'line_start': int,  # Starting line number
            'line_end': int,    # Ending line number
            'args': [...],      # List of argument information
            'returns': str,     # Return type information
            'docstring': str    # Function docstring (if any)
        }
    ]
}
```