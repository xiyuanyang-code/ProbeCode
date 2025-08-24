"""File content reader for the coding agent."""

import os
import sys
import json

sys.path.append(os.getcwd())
import fnmatch
from typing import Optional, List, Tuple
from abc import ABC, abstractmethod

# add analyze tools
from CodingAgent.config import load_config
from CodingAgent.pyparser.parser import PythonStructureParser, parse_python_file


class AbstractContentProvider(ABC):
    """Abstract base class for content providers."""

    @abstractmethod
    def get_content(self) -> List[Tuple[str, str]]:
        """Get the content from the provider.

        Returns:
            List of tuples containing (file_path, file_content).
        """
        pass


class FileContentReader(AbstractContentProvider):
    """A simple file content context manager.

    Loads file contents under the specified path when entering the context,
    and supports include/exclude file filtering with a two-step process.
    Automatically skips binary files.
    """

    def __init__(
        self,
        file_path: str = None,
        include_list: Optional[List[str]] = None,
        exclude_list: Optional[List[str]] = None,
    ):
        """Initialize the FileContentReader.

        Args:
            file_path: Path to the directory to read files from. Defaults to current working directory.
            include_list: List of file patterns to include.
            exclude_list: List of file patterns to exclude.

        Raises:
            ValueError: If file_path is not a valid directory.
        """
        file_path = os.getcwd() if file_path is None else file_path
        if not os.path.isdir(file_path):
            raise ValueError(f"'{file_path}' is not a valid directory.")
        self.total_file_path = file_path
        self.include_list = include_list if include_list is not None else []
        self.exclude_list = exclude_list if exclude_list is not None else []
        self._contents: Optional[List[Tuple[str, str]]] = None
        self.files_filtered: Optional[List[str]] = None
        self.config = load_config()

        # feat: loading for environments
        # self.environment is where the stores the code, in the current working directory
        self.environ_path = os.path.join(os.getcwd(), ".environment")
        # todo add judgement if the environment path exists and has contents
        os.makedirs(self.environ_path, exist_ok=True)

        # Initialize
        self.filter_files()

    def _all_files(self) -> List[str]:
        """Get absolute paths of all files in the directory.

        Returns:
            List of absolute file paths.
        """
        matches = []
        for root, _, files in os.walk(self.total_file_path):
            for f in files:
                matches.append(os.path.join(root, f))
        return matches

    def _match_patterns(self, files: List[str], patterns: List[str]) -> List[str]:
        """Return files that match any of the patterns.

        Args:
            files: List of file paths to check.
            patterns: List of patterns to match against.

        Returns:
            List of matching file paths.
        """
        matched = set()
        for pat in patterns:
            for f in files:
                rel_path = os.path.relpath(f, self.total_file_path)
                if fnmatch.fnmatch(rel_path, pat):
                    matched.add(f)
        return list(matched)

    def _is_binary_file(self, path: str) -> bool:
        """Check if a file is a binary file.

        Args:
            path: Path to the file to check.

        Returns:
            True if the file is binary, False otherwise.
        """
        try:
            with open(path, "rb") as f:
                chunk = f.read(1024)
            # Check for null byte
            if b"\0" in chunk:
                return True
            # Try to decode as utf-8
            chunk.decode("utf-8")
            return False
        except (UnicodeDecodeError, OSError):
            return True

    def filter_files(self) -> List[str]:
        """Filter files with include then exclude patterns.

        Returns:
            List of filtered file paths.
        """
        all_files = self._all_files()

        # Step 1: include
        if self.include_list:
            included = self._match_patterns(all_files, self.include_list)
        else:
            included = all_files  # Default to all files

        # Step 2: exclude
        if self.exclude_list:
            excluded = set(self._match_patterns(all_files, self.exclude_list))
            final_files = [f for f in included if f not in excluded]
        else:
            final_files = included

        # Step 3: Skip binary files
        final_files = [f for f in final_files if not self._is_binary_file(f)]

        self.files_filtered = sorted(final_files)
        return self.files_filtered

    def get_content(self) -> List[Tuple[str, str]]:
        """Read file contents (skipping binary files).

        Returns:
            List of tuples containing (file_path, file_content).
        """
        if self._contents is None:
            self._contents = []
            self.json_file = []
            for path in self.files_filtered:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    file_content: str = f.read()
                    self._contents.append((path, file_content))
                    new_path = path[:-3].replace(os.sep, "_")

                    environ_file_path = os.path.join(
                        self.environ_path, f"environ_{new_path}.json"
                    )
                    self.json_file.append(environ_file_path)
                    with open(environ_file_path, "w", encoding="utf-8") as environ_file:
                        result = parse_python_file(file_path=path)
                        json.dump(
                            result,
                            environ_file,
                            indent=2,
                            ensure_ascii=False,
                            sort_keys=True,
                        )
            with open(os.path.join(self.environ_path, "config.json"), "w") as file:
                json.dump(
                    self.json_file, file, indent=2, ensure_ascii=False, sort_keys=True
                )

        return self._contents

    def __enter__(self) -> "FileContentReader":
        """Enter the context manager.

        Returns:
            The FileContentReader instance.
        """
        self.get_content()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit the context manager.

        Args:
            exc_type: Exception type if an exception occurred.
            exc_val: Exception value if an exception occurred.
            exc_tb: Exception traceback if an exception occurred.

        Returns:
            False to propagate exceptions.
        """
        self._contents = None
        if exc_type:
            print(f"An exception occurred: {exc_val}")
        return False


# A simple test
if __name__ == "__main__":
    with FileContentReader(
        include_list=["*.py"],
        exclude_list=["log/*", "build/*", "dist/*", "test/*"],
    ) as file_manager:
        results = file_manager.get_content()
    for path, content in results:
        print(path)
        print(content)
