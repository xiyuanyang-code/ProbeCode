#!/usr/bin/env python3
"""
Test the programmatic interface of the unified parser
"""

import sys
import os
import json
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from CodingAgent.pyparser.parser import PythonStructureParser

def test_programmatic_usage():
    """Test programmatic usage of the parser"""
    # Create parser instance
    parser = PythonStructureParser("./example/example.py")
    
    # Parse the file
    if parser.parse_file():
        parser.extract_classes_and_functions()
        
        # Get results without printing
        results = parser.get_results()
        print(results)
        with open("./result/test.json", "w") as file:
            json.dump(results, file)
        
        print("Programmatic access test:")
        print(f"File: {results['file_path']}")
        print(f"Number of classes: {len(results['classes'])}")
        print(f"Number of functions: {len(results['functions'])}")
        
        # Access class information
        for cls in results['classes']:
            print(f"Class: {cls['name']}")
            if cls['docstring']:
                print(f"  Docstring: {cls['docstring']}")
            print(f"  Methods: {len(cls['methods'])}")
            
        # Access function information
        for func in results['functions']:
            print(f"Function: {func['name']}")
            if func['docstring']:
                print(f"  Docstring: {func['docstring']}")

if __name__ == "__main__":
    test_programmatic_usage()