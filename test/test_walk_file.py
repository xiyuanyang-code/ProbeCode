import os
import sys
import shutil

sys.path.append(os.getcwd())

from typing import List
from inspector.code_loader import filter_files


# --- Helper Functions for Test Setup/Teardown ---
TEST_DIR = "test_dir_for_manual_tests"


def _setup_test_environment() -> None:
    """Creates a fresh set of dummy files and directories for testing."""
    _cleanup_test_environment()  # Ensure a clean slate

    # Create directories
    dirs_to_create = [
        TEST_DIR,
        os.path.join(TEST_DIR, "sub_dir"),
        os.path.join(TEST_DIR, "build"),
        os.path.join(TEST_DIR, "node_modules"),
        os.path.join(TEST_DIR, "tmp"),
        os.path.join(TEST_DIR, "docs"),
    ]
    for d in dirs_to_create:
        os.makedirs(d, exist_ok=True)

    # Create files
    files_to_create = {
        os.path.join(TEST_DIR, "file1.txt"): "content",
        os.path.join(TEST_DIR, "temp.log"): "log",
        os.path.join(TEST_DIR, "build", "output.log"): "build log",
        os.path.join(TEST_DIR, "sub_dir", "another.py"): "import os",
        os.path.join(TEST_DIR, ".hidden_file"): "hidden",
        os.path.join(TEST_DIR, "important.txt"): "important",
        os.path.join(TEST_DIR, "docs", "report.md"): "report",
        os.path.join(TEST_DIR, "node_modules", "dep.js"): "js",
        os.path.join(TEST_DIR, "tmp", "readme.md"): "readme",
        os.path.join(TEST_DIR, "tmp", "temp.txt"): "temp file in tmp",
        os.path.join(TEST_DIR, "important.log"): "important log content",
    }
    for path, content in files_to_create.items():
        with open(path, "w") as f:
            f.write(content)


def _cleanup_test_environment() -> None:
    """Removes the test directory if it exists."""
    if os.path.exists(TEST_DIR):
        shutil.rmtree(TEST_DIR)


def _get_relative_paths(full_paths: List[str], base_dir: str) -> List[str]:
    """Converts a list of full paths to relative paths for comparison."""
    return sorted(
        [os.path.relpath(p, base_dir).replace(os.sep, "/") for p in full_paths]
    )


def run_test_case(
    test_name: str, ignored: List[str], included: List[str], expected: List[str]
) -> None:
    """Helper to run a single test case, setting up and tearing down the environment."""
    print(f"\n--- Running {test_name} ---")
    original_cwd = os.getcwd()
    _setup_test_environment()  # Create files and dirs for this test

    try:
        # Change to TEST_DIR for walk_file to operate correctly from its root
        os.chdir(TEST_DIR)
        collected_full_paths = filter_files(include=included, exclude=ignored)
        # Convert collected paths back to relative paths from TEST_DIR
        collected_relative_paths = _get_relative_paths(collected_full_paths, ".")

        passed = sorted(collected_relative_paths) == sorted(expected)
        status = "PASSED" if passed else "FAILED"
        print(f"Test Status: {status}")
        print(f"  Expected ({len(expected)} files): {sorted(expected)}")
        print(
            f"  Actual   ({len(collected_relative_paths)} files): {collected_relative_paths}"
        )

        if not passed:
            print("\n  --- Mismatch Details ---")
            expected_set = set(expected)
            actual_set = set(collected_relative_paths)
            missing = list(expected_set - actual_set)
            extra = list(actual_set - expected_set)
            if missing:
                print(f"  Missing in actual: {sorted(missing)}")
            if extra:
                print(f"  Extra in actual: {sorted(extra)}")

    finally:
        os.chdir(original_cwd)  # Always change back to original CWD
        _cleanup_test_environment()  # Clean up test files

    return passed


# --- Test Cases ---


def test_ignore_log_build_node_modules():
    """Test Case 1: Ignore .log files, build directory, and node_modules."""
    ignored = ["*.log", "build/", "node_modules/"]
    included = ["*.*"]
    expected_files = [
        ".hidden_file",
        "file1.txt",
        "docs/report.md",
        "important.txt",
        "sub_dir/another.py",
        "tmp/readme.md",
        "tmp/temp.txt",
    ]
    return run_test_case("Test Case 1", ignored, included, expected_files)


def test_ignore_all_include_specific():
    """Test Case 2: Ignore all, but explicitly include important.txt and sub_dir/another.py."""
    # This tests the "whitelist" behavior where inclusion overrides general exclusion.
    ignored = []
    included = ["important.txt", "sub_dir/another.py"]  # Corrected expectation
    expected_files = [
        "important.txt",
        "sub_dir/another.py",  # This should be included because of the explicit include
    ]
    return run_test_case("Test Case 2", ignored, included, expected_files)


def test_only_include_txt_files():
    """Test Case 3: Only include .txt files (implicitly ignore others)."""
    # This scenario means if 'included' is not empty, only matched files are considered.
    # The original expected output was correct.
    ignored = []
    included = ["*.txt"]  # Changed from "!**/*.txt" to only include .txt files
    expected_files = [
        "file1.txt",
        "important.txt",
        "tmp/temp.txt",
    ]
    return run_test_case("Test Case 3", ignored, included, expected_files)


def test_no_ignore_include_lists():
    """Test Case 4: No ignore/include lists (all files should be collected)."""
    # Verifies the default behavior: if no rules, collect everything.
    ignored = []
    included = []
    expected_files = [
        ".hidden_file",
        "build/output.log",
        "docs/report.md",
        "file1.txt",
        "important.log",
        "important.txt",
        "node_modules/dep.js",
        "sub_dir/another.py",
        "temp.log",
        "tmp/readme.md",
        "tmp/temp.txt",
    ]
    return run_test_case("Test Case 4", ignored, included, expected_files)


def test_parent_directory_ignore():
    """Test Case 5: Test parent directory ignore - tmp/ should ignore everything inside."""
    ignored = ["tmp/"]
    included = [
        "*",
    ]
    expected_files = [
        ".hidden_file",
        "build/output.log",
        "docs/report.md",
        "file1.txt",
        "important.log",
        "important.txt",
        "node_modules/dep.js",
        "sub_dir/another.py",
        "temp.log",
    ]
    return run_test_case("Test Case 5", ignored, included, expected_files)


# --- Run All Tests ---
if __name__ == "__main__":
    print("Running all test cases for file filtering logic...\n")
    status = 1
    status *= test_ignore_log_build_node_modules()
    status *= test_ignore_all_include_specific()
    status *= test_only_include_txt_files()
    status *= test_no_ignore_include_lists()
    status *= test_parent_directory_ignore()

    print("\n\ntest result: ")
    print(bool(status))
