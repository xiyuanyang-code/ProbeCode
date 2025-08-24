import json
import os
import sys

from typing import List, Optional, Dict, Any

# This toolkit maintains several level of code inspecting
# * project level: get all the information about the repo
# * file level: get information for a specific file
# * structure level: get detailed information for a specific class and function
# * element level: search for a certain element in specific function or classes
# todo add some searching functions

sys.path.append(os.getcwd())


def list_all_files() -> List[str]:
    """
    Lists all files in the project.

    Returns:
        A list of all file paths.
    """
    pass


def list_tree_structure() -> str:
    """
    Returns a string representing the file tree structure of the project.
    """
    pass


def search_file_by_name(search_pattern: str) -> List[str]:
    """
    Searches for files by a given name pattern.

    Args:
        search_pattern: The pattern to search for (e.g., 'test.py').

    Returns:
        A list of file paths that match the pattern.
    """
    pass


def search_file_by_code(search_pattern: str) -> List:
    """
    Searches for specific code snippets within the project files.

    Args:
        search_pattern: The code snippet to search for.

    Returns:
        A list of file paths containing the code snippet.
    """
    pass


def get_file_summary(file_path: str) -> Dict[str, Any]:
    """
    Provides a high-level summary of a file, including its classes and functions.

    Args:
        file_path: The path to the file.

    Returns:
        A dictionary with a summary of the file's contents.
    """
    pass


def get_file_all(file_path: str) -> Dict[str, Any]:
    """
    Retrieves all parsed content from a file, including all classes, functions, and top-level code.

    Args:
        file_path: The path to the file.

    Returns:
        A dictionary containing all parsed code structures.
    """
    pass


def get_file_classes_summary(file_path: str) -> List:
    """
    Provides a summary of all classes in a file.

    Args:
        file_path: The path to the file.

    Returns:
        A list of dictionaries, each providing a summary of a class.
    """
    pass


def get_file_functions_summary(file_path: str) -> List:
    """
    Provides a summary of all functions in a file.

    Args:
        file_path: The path to the file.

    Returns:
        A list of dictionaries, each providing a summary of a function.
    """
    pass


def get_file_classes_all(file_path: str) -> List:
    """
    Retrieves the full definitions for all classes in a file.

    Args:
        file_path: The path to the file.

    Returns:
        A list of dictionaries, each containing the complete definition of a class.
    """
    pass


def get_file_functions_all(file_path: str) -> List:
    """
    Retrieves the full definitions for all functions in a file.

    Args:
        file_path: The path to the file.

    Returns:
        A list of dictionaries, each containing the complete definition of a function.
    """
    pass


def get_file_toplevel_code(file_path: str) -> List:
    """
    Retrieves all top-level code statements (e.g., imports, assignments) from a file.

    Args:
        file_path: The path to the file.

    Returns:
        A list of dictionaries, each representing a top-level code statement.
    """
    pass


def get_class_definition(file_path: str, class_name: str) -> Optional[Dict[str, Any]]:
    """
    Retrieves the complete definition of a specific class from a file.

    Args:
        file_path: The path to the file.
        class_name: The name of the class.

    Returns:
        A dictionary with the class's full definition, or None if not found.
    """
    pass


def get_class_all(file_path: str, class_name: str) -> str:
    """
    Retrieves the complete source code of a specific class.

    Args:
        file_path: The path to the file containing the class.
        class_name: The name of the class.

    Returns:
        A string containing the complete source code for the class, or an error message if not found.
    """
    pass


def get_function_all(file_path: str, function_name: str) -> str:
    """
    Retrieves the complete source code of a specific function.

    Args:
        file_path: The path to the file containing the function.
        function_name: The name of the function.

    Returns:
        A string containing the complete source code for the function, or an error message if not found.
    """
    pass


def get_function_definition(
    file_path: str, function_name: str
) -> Optional[Dict[str, Any]]:
    """
    Retrieves the complete definition of a specific function from a file.

    Args:
        file_path: The path to the file.
        function_name: The name of the function.

    Returns:
        A dictionary with the function's full definition, or None if not found.
    """
    pass


def get_method_definition(
    file_path: str, class_name: str, method_name: str
) -> Optional[Dict[str, Any]]:
    """
    Retrieves the complete definition of a specific method from a class.

    Args:
        file_path: The path to the file.
        class_name: The name of the class containing the method.
        method_name: The name of the method.

    Returns:
        A dictionary with the method's full definition, or None if not found.
    """
    pass


def get_docstring(file_path: str, item_name: str, item_type: str) -> Optional[str]:
    """
    Retrieves the docstring for a specific class, function, or method.

    Args:
        file_path: The path to the file.
        item_name: The name of the item (class, function, or method).
        item_type: The type of the item ('class', 'function', or 'method').

    Returns:
        The docstring as a string, or None if not found.
    """
    pass


def get_function_arguments(
    file_path: str, function_name: str
) -> Optional[List[Dict[str, Any]]]:
    """
    Retrieves the arguments for a specific function.

    Args:
        file_path: The path to the file.
        function_name: The name of the function.

    Returns:
        A list of dictionaries, each describing an argument, or None if not found.
    """
    pass
