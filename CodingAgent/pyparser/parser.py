#!/usr/bin/env python3
"""
Python File Structure Parser
Extracts class and function information from Python files, including source code,
docstrings, and detailed parameter information. It also extracts all top-level
statements not contained within classes or functions.
Supports both programmatic access and console output.
"""

import ast
import os
import sys
from typing import List, Dict, Any, Optional


class PythonStructureParser:
    """
    Parses Python files and extracts class and function information,
    along with top-level statements.
    """
    
    def __init__(self, file_path: str):
        """
        Initializes the parser with a file path.
        
        Args:
            file_path (str): Path to the Python file to parse.
        """
        self.file_path = os.path.abspath(file_path) if not os.path.isabs(file_path) else file_path
        self.tree = None
        self.source_lines = []
        self.classes = []
        self.functions = []
        self.top_level_code = []
        
    def parse_file(self) -> bool:
        """
        Reads and parses the Python file.
        
        Returns:
            bool: True if parsing was successful, False otherwise.
        """
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                source_code = file.read()
                self.source_lines = source_code.splitlines()
                # Use ast to parse the file
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
        Extracts class, function, and top-level code information from the parsed AST.
        """
        if not self.tree:
            print("Error: File must be parsed first.")
            return
            
        for node in self.tree.body:
            if isinstance(node, ast.ClassDef):
                class_info = self._extract_class_info(node)
                self.classes.append(class_info)
            elif isinstance(node, ast.FunctionDef):
                func_info = self._extract_function_info(node)
                self.functions.append(func_info)
            else:
                # This is a top-level statement (not a class or function)
                code_info = {
                    'type': type(node).__name__,
                    'line_start': node.lineno,
                    'line_end': node.end_lineno,
                    'source_code': self._extract_source_code(node, check_docstring=False)
                }
                self.top_level_code.append(code_info)
                    
    def _extract_source_code(self, node: ast.AST, check_docstring: bool = True) -> str:
        """
        Extracts the source code snippet for a given AST node.
        
        Args:
            node (ast.AST): The AST node to extract code for.
            check_docstring (bool): If True, removes the docstring from the
                                     extracted code.
        
        Returns:
            str: The source code snippet.
        """
        if not hasattr(node, 'lineno') or not hasattr(node, 'end_lineno'):
            return ""

        start_line = node.lineno - 1
        end_line = node.end_lineno
        lines = self.source_lines[start_line:end_line]
        
        # Remove the docstring from the source code to avoid duplication
        if check_docstring:
            docstring_node = next((n for n in node.body if isinstance(n, ast.Expr) and isinstance(n.value, ast.Constant) and isinstance(n.value.value, str)), None)
            if docstring_node:
                doc_start_line = docstring_node.lineno - 1
                doc_end_line = docstring_node.end_lineno
                # Create a new list of lines without the docstring
                lines_without_doc = lines[:doc_start_line - start_line] + lines[doc_end_line - start_line:]
                return '\n'.join(lines_without_doc)
            
        return '\n'.join(lines)
            
    def _extract_class_info(self, node: ast.ClassDef) -> Dict[str, Any]:
        """
        Extracts information about a class.
        
        Args:
            node (ast.ClassDef): AST node representing a class.
            
        Returns:
            Dict[str, Any]: Dictionary containing class information.
        """
        methods = []
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                methods.append(self._extract_function_info(item))
                
        docstring = ast.get_docstring(node)
                
        return {
            'name': node.name,
            'line_start': node.lineno,
            'line_end': node.end_lineno,
            'methods': methods,
            'bases': [ast.unparse(base) for base in node.bases],
            'docstring': docstring,
            'source_code': self._extract_source_code(node)
        }
        
    def _extract_function_info(self, node: ast.FunctionDef) -> Dict[str, Any]:
        """
        Extracts information about a function.
        
        Args:
            node (ast.FunctionDef): AST node representing a function.
            
        Returns:
            Dict[str, Any]: Dictionary containing function information.
        """
        args = []
        defaults = node.args.defaults
        num_defaults = len(defaults)
        args_count = len(node.args.args)
        
        # Process arguments (including default values)
        for i, arg in enumerate(node.args.args):
            arg_info = {
                'name': arg.arg,
                'annotation': ast.unparse(arg.annotation) if arg.annotation else None
            }
            
            # Add default value information
            if i >= args_count - num_defaults:
                default_index = i - (args_count - num_defaults)
                arg_info['default'] = ast.unparse(defaults[default_index])
            else:
                arg_info['default'] = None
                
            args.append(arg_info)
            
        docstring = ast.get_docstring(node)
            
        return {
            'name': node.name,
            'line_start': node.lineno,
            'line_end': node.end_lineno,
            'args': args,
            'returns': ast.unparse(node.returns) if node.returns else None,
            'docstring': docstring,
            'source_code': self._extract_source_code(node)
        }
        
    def get_results(self) -> Dict[str, Any]:
        """
        Gets the parsed results as a structured dictionary without printing.
        
        Returns:
            Dict[str, Any]: Dictionary containing parsed classes, functions,
                            and top-level code.
        """
        return {
            'file_path': self.file_path,
            'classes': self.classes,
            'functions': self.functions,
            'top_level_code': self.top_level_code
        }
        
    def print_results(self) -> None:
        """
        Prints parsed results to the console.
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
        
        if results['top_level_code']:
            print("Top-Level Code:")
            for code_block in results['top_level_code']:
                self._print_top_level_code_info(code_block, indent=2)
                print()
                
    def _print_function_info(self, func_info: Dict[str, Any], indent: int = 0) -> None:
        """
        Prints function information with specified indentation.
        
        Args:
            func_info (Dict[str, Any]): Dictionary containing function information.
            indent (int): Number of spaces to indent the output.
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
        
        # Print the source code
        print(f"{spaces}  Source Code:\n{spaces}---")
        for line in func_info['source_code'].splitlines():
            print(f"{spaces}  {line}")
        print(f"{spaces}---")

    def _print_top_level_code_info(self, code_info: Dict[str, Any], indent: int = 0) -> None:
        """
        Prints top-level code information with specified indentation.

        Args:
            code_info (Dict[str, Any]): Dictionary containing top-level code information.
            indent (int): Number of spaces to indent the output.
        """
        spaces = " " * indent
        print(f"{spaces}Statement Type: {code_info['type']}")
        print(f"{spaces}  Start line: {code_info['line_start']}")
        print(f"{spaces}  End line: {code_info['line_end']}")
        print(f"{spaces}  Source Code:\n{spaces}---")
        for line in code_info['source_code'].splitlines():
            print(f"{spaces}  {line}")
        print(f"{spaces}---")


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


def CLI():
    """Main function for command-line usage."""
    if len(sys.argv) != 2:
        print("Usage: python parser.py <input_file.py>")
        sys.exit(1)
        
    file_path = sys.argv[1]

    parser = PythonStructureParser(file_path)
    if parser.parse_file():
        parser.extract_classes_and_functions()
        parser.print_results()


if __name__ == "__main__":
    CLI()