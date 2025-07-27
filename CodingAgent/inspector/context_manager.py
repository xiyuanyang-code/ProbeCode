import os
import sys

sys.path.append(os.getcwd())

from abc import ABC, abstractmethod
from typing import Optional, List, Tuple
from CodingAgent.inspector.code_loader import filter_files, read_single_file


class AbstractContentProvider(ABC):
    @abstractmethod
    def get_content(self) -> List[Tuple[str, str]]:
        pass


class FileContentContextManager(AbstractContentProvider):
    """
    A simple file content context manager.
    Loads file contents under the specified path when entering the context, and supports file filtering.
    """

    def __init__(
        self,
        file_path: str = None,
        include_list: Optional[List[str]] = None,
        exclude_list: Optional[List[str]] = None,
    ):
        file_path = os.getcwd() if file_path is None else file_path
        if not os.path.isdir(file_path):
            raise ValueError(f"'{file_path}' is not a valid directory.")
        self.total_file_path = file_path
        self.include_list = include_list if include_list is not None else []
        self.exclude_list = exclude_list if exclude_list is not None else []
        self._contents: Optional[List[Tuple[str, str]]] = None
        self.files_filtered: List[str] = None


        # initialize
        self.filter_files()

    def filter_files(self) -> List[str]:
        self.files_filtered = filter_files(
            file_path=self.total_file_path,
            include=self.include_list,
            exclude=self.exclude_list,
        )
        return self.files_filtered

    def get_content(self) -> List[Tuple[str, str]]:
        """
        Implements the abstract method: get and return file contents.
        """
        if self._contents is None:
            self._contents = [
                read_single_file(content_path) for content_path in self.files_filtered
            ]
        return self._contents

    def __enter__(self) -> "FileContentContextManager":
        """
        Enter the runtime context.
        Loads file contents and returns itself.
        """
        self.get_content()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit the runtime context.
        Any cleanup can be done here, such as releasing resources.
        For file reading, explicit cleanup is usually not needed because files are already closed.
        """
        self._contents = None
        if exc_type:
            print(f"An exception occurred: {exc_val}")
        return False


# a simple test
if __name__ == "__main__":
    with FileContentContextManager(
        include_list=["*.py"],
        exclude_list=["/test"],
        # for this demo, it will include all the files with *.py pattern, but exclude all the files matched in the directory /test
    ) as file_manager:
        print(file_manager.files_filtered)
        results = file_manager.get_content()

    print(len(results))
    for result in results:
        print(result[0])
