import os
import fnmatch
from typing import Tuple


def read_single_file(file_path: str) -> Tuple[str, str]:
    """Read a single file and return its content and extension."""
    _, ext = os.path.splitext(file_path)
    with open(file_path, "r", encoding="utf-8") as file:
        file_string = file.read().strip()
    return (file_string, ext)


def filter_files(
    file_path: str = None, include: list[str] = None, exclude: list[str] = None
) -> list[str]:
    """
    Recursively filter files based on include and exclude patterns.
    Include rules take precedence over exclude rules.

    Args:
        file_path (str): Root directory path to search for files. Defaults to current working directory.
        include (list[str]): List of fnmatch patterns for files to include. Supports directory patterns (e.g., "**/build/").
        exclude (list[str]): List of fnmatch patterns for files to exclude. Supports directory patterns (e.g., "**/node_modules/").

    Returns:
        list[str]: List of relative file paths that match the filter criteria.
    """
    file_path = os.getcwd() if file_path is None else file_path
    include = [] if include is None else include
    exclude = [] if exclude is None else exclude

    collected_files = set()

    for root, dirs, files in os.walk(file_path):
        relative_root = os.path.relpath(root, file_path).replace(os.sep, "/")
        if relative_root == ".":
            relative_root = ""
        elif not relative_root.endswith("/"):
            relative_root += "/"

        # --- Step 1: Check if the directory should be excluded (e.g., node_modules/) ---
        dir_should_be_excluded = False
        for pattern in exclude:
            # Check for explicit directory exclusion patterns (ending with '/')
            if pattern.endswith("/") and fnmatch.fnmatch(relative_root, pattern):
                dir_should_be_excluded = True
                break

        if dir_should_be_excluded:
            # Skip all files in this directory as the entire directory is excluded
            continue

        # --- Step 2: Process files in the current directory ---
        for file_name in files:
            full_file_path = os.path.join(root, file_name)
            relative_file_path = os.path.relpath(full_file_path, file_path).replace(
                os.sep, "/"
            )

            is_included_by_rule = False
            is_excluded_by_rule = False

            # Prioritize include rules
            if include:
                for pattern in include:
                    # Handle "negation include" rules (e.g., "!temp*.txt")
                    if pattern.startswith("!"):
                        if fnmatch.fnmatch(relative_file_path, pattern[1:]):
                            is_excluded_by_rule = True
                            break
                    elif fnmatch.fnmatch(relative_file_path, pattern):
                        is_included_by_rule = True
                        break
                # If include list is not empty, and file wasn't positively included or was explicitly excluded by an include rule, skip it.
                if not is_included_by_rule or is_excluded_by_rule:
                    continue
            else:
                # If include list is empty, all files are initially considered for inclusion
                is_included_by_rule = True

            # Only check exclude rules if the file was initially included
            if is_included_by_rule:
                is_excluded_by_secondary_rule = False
                for pattern in exclude:
                    # Check if file matches any exclude pattern, including directory-level exclusions
                    if pattern.endswith("/"):
                        # Check if the file is within an excluded directory
                        if relative_file_path.startswith(pattern):
                            is_excluded_by_secondary_rule = True
                            break
                    elif fnmatch.fnmatch(relative_file_path, pattern):
                        is_excluded_by_secondary_rule = True
                        break

                if not is_excluded_by_secondary_rule:
                    collected_files.add(relative_file_path)

    return sorted(list(collected_files))
