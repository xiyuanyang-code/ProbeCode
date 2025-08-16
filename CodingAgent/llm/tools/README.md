# MCP Tools

## Default Tools

This directory contains the default tools available for use with the MCP (Multi-Client Protocol) in the CodingAgent project. These tools extend the capabilities of the LLM by providing access to external functionalities.

### Web Search Tools

1. `web_search_english`: 
   - Searches the internet for English content using the DuckDuckGo API
   - Takes a query string and optional max_results parameter
   - Returns formatted search results with titles, snippets, and URLs

2. `web_search_chinese`:
   - Searches the internet for Chinese content using Zhipu AI's web search tool
   - Requires ZHIPU_API_KEY environment variable to be set
   - Returns search results in Chinese

### File Operations Tools

1. `create_folder`:
   - Creates a new folder at the specified path
   - Takes a path string as parameter
   - Returns a success or error message

2. `list_directory`:
   - Lists all files and subdirectories in the specified directory
   - Takes a path string as parameter
   - Returns a list of file/directory names or an error message

3. `delete_item`:
   - Deletes the specified file or folder
   - Takes a path string as parameter
   - Returns a success or error message

4. `rename_item`:
   - Renames a file or folder
   - Takes source and destination path strings as parameters
   - Returns a success or error message

5. `move_file`:
   - Moves a file to a new location
   - Takes source and destination path strings as parameters
   - Returns a success or error message

6. `read_file`:
   - Reads the contents of a file
   - Takes a path string as parameter
   - Returns the file contents or an error message

7. `write_file`:
   - Writes content to a file
   - Takes a path string and content string as parameters
   - Returns a success or error message

8. `get_file_info`:
   - Gets information about a file or directory
   - Takes a path string as parameter
   - Returns a dictionary with file information or an error message

9. `get_current_directory`:
   - Gets the current working directory
   - Returns the current directory path or an error message

10. `create_file`:
    - Creates a new empty file at the specified path
    - Takes a path string as parameter
    - Returns a success or error message