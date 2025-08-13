#!/usr/bin/env python3
"""
Python File Structure Parser
Extracts class and function information from Python files
Supports both programmatic access and console output
"""

import ast
import sys
from typing import List, Dict, Any, Optional


class PythonStructureParser:
    """Parses Python files and extracts class and function information"""
    
    def __init__(self, file_path: str):
        """
        Initialize the parser with a file path
        
        Args:
            file_path (str): Path to the Python file to parse
        """
        self.file_path = file_path
        self.tree = None
        self.classes = []
        self.functions = []
        
    def parse_file(self) -> bool:
        """
        Read and parse the Python file
        
        Returns:
            bool: True if parsing was successful, False otherwise
        """
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                source_code = file.read()
                self.tree = ast.parse(source_code)
            return True
        except FileNotFoundError:
            print(f"Error: File '{self.file_path}' not found")
            return False
        except SyntaxError as e:
            print(f"Error: Syntax error in file '{self.file_path}': {e}")
            return False
            
    def extract_classes_and_functions(self) -> None:
        """
        Extract class and function information from the parsed AST
        """
        if not self.tree:
            print("Error: File must be parsed first")
            return
            
        for node in ast.walk(self.tree):
            if isinstance(node, ast.ClassDef):
                class_info = self._extract_class_info(node)
                self.classes.append(class_info)
            elif isinstance(node, ast.FunctionDef):
                func_info = self._extract_function_info(node)
                # Only add functions that are not methods (module-level functions)
                if not self._is_method(node):
                    self.functions.append(func_info)
                    
    def _extract_class_info(self, node: ast.ClassDef) -> Dict[str, Any]:
        """
        Extract information about a class
        
        Args:
            node (ast.ClassDef): AST node representing a class
            
        Returns:
            Dict[str, Any]: Dictionary containing class information
        """
        methods = []
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                methods.append(self._extract_function_info(item))
                
        # Extract docstring if available
        docstring = ast.get_docstring(node)
                
        return {
            'name': node.name,
            'line_start': node.lineno,
            'line_end': node.end_lineno,
            'methods': methods,
            'bases': [ast.dump(base) for base in node.bases],
            'docstring': docstring
        }
        
    def _extract_function_info(self, node: ast.FunctionDef) -> Dict[str, Any]:
        """
        Extract information about a function
        
        Args:
            node (ast.FunctionDef): AST node representing a function
            
        Returns:
            Dict[str, Any]: Dictionary containing function information
        """
        args = []
        defaults = node.args.defaults
        num_defaults = len(defaults)
        args_count = len(node.args.args)
        
        # Process arguments (including default values)
        for i, arg in enumerate(node.args.args):
            arg_info = {
                'name': arg.arg,
                'annotation': ast.dump(arg.annotation) if arg.annotation else None
            }
            
            # Add default value information
            if i >= args_count - num_defaults:
                default_index = i - (args_count - num_defaults)
                arg_info['default'] = ast.dump(defaults[default_index])
            else:
                arg_info['default'] = None
                
            args.append(arg_info)
            
        # Extract docstring if available
        docstring = ast.get_docstring(node)
            
        return {
            'name': node.name,
            'line_start': node.lineno,
            'line_end': node.end_lineno,
            'args': args,
            'returns': ast.dump(node.returns) if node.returns else None,
            'docstring': docstring
        }
        
    def _is_method(self, node: ast.FunctionDef) -> bool:
        """
        Check if a function is a method of a class
        
        Args:
            node (ast.FunctionDef): AST node representing a function
            
        Returns:
            bool: True if the function is a method, False otherwise
        """
        # Walk through the AST to find the function's context
        for parent in ast.walk(self.tree):
            if isinstance(parent, ast.ClassDef):
                for item in parent.body:
                    if item == node:
                        return True
        return False
        
    def get_results(self) -> Dict[str, Any]:
        """
        Get the parsed results as a structured dictionary without printing
        
        Returns:
            Dict[str, Any]: Dictionary containing parsed classes and functions
        """
        return {
            'file_path': self.file_path,
            'classes': self.classes,
            'functions': self.functions
        }
        
    def print_results(self) -> None:
        """
        Print parsed results to console
        """
        results = self.get_results()
        
        print(f"File: {results['file_path']}\n")
        
        if results['classes']:
            print("Classes:")
            for cls in results['classes']:
                print(f"  Class: {cls['name']}")
                print(f"    Start line: {cls['line_start']}")
                print(f"    End line: {cls['line_end']}")
                print(f"    Base classes: {cls['bases']}")
                if cls['docstring']:
                    print(f"    Docstring: {cls['docstring']}")
                if cls['methods']:
                    print("    Methods:")
                    for method in cls['methods']:
                        self._print_function_info(method, indent=6)
                print()
                
        if results['functions']:
            print("Functions:")
            for func in results['functions']:
                self._print_function_info(func, indent=2)
                print()
                
    def _print_function_info(self, func_info: Dict[str, Any], indent: int = 0) -> None:
        """
        Print function information with specified indentation
        
        Args:
            func_info (Dict[str, Any]): Dictionary containing function information
            indent (int): Number of spaces to indent the output
        """
        spaces = " " * indent
        print(f"{spaces}Function: {func_info['name']}")
        print(f"{spaces}  Start line: {func_info['line_start']}")
        print(f"{spaces}  End line: {func_info['line_end']}")
        if func_info['docstring']:
            print(f"{spaces}  Docstring: {func_info['docstring']}")
        if func_info['args']:
            print(f"{spaces}  Arguments:")
            for arg in func_info['args']:
                default_str = f" = {arg['default']}" if arg['default'] else ""
                annotation_str = f": {arg['annotation']}" if arg['annotation'] else ""
                print(f"{spaces}    {arg['name']}{annotation_str}{default_str}")
        if func_info['returns']:
            print(f"{spaces}  Return type: {func_info['returns']}")


def parse_python_file(file_path: str) -> Optional[Dict[str, Any]]:
    """
    Parse a Python file and return structured information about its classes and functions
    
    Args:
        file_path (str): Path to the Python file to parse
        
    Returns:
        Optional[Dict[str, Any]]: Dictionary with parsed information or None if parsing failed
    """
    parser = PythonStructureParser(file_path)
    if parser.parse_file():
        parser.extract_classes_and_functions()
        return parser.get_results()
    return None


def main():
    """Main function for command-line usage"""
    if len(sys.argv) != 2:
        print("Usage: python unified_parser.py <input_file.py>")
        sys.exit(1)
        
    file_path = sys.argv[1]
    parser = PythonStructureParser(file_path)
    if parser.parse_file():
        parser.extract_classes_and_functions()
        parser.print_results()


if __name__ == "__main__":
    main()