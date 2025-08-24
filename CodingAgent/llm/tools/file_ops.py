import os
import shutil

def create_folder(path: str) -> str:
    """Creates a new folder at the specified path.

    This function serves as a tool for creating directories. It should only be used
    when explicitly instructed to perform a file system operation.

    Args:
        path (str): The path where the folder should be created.

    Returns:
        str: A message indicating the outcome of the operation (success or failure).

    Examples:
        **Positive Examples:**
        1. **User Request:** "Please create a new directory named 'project_data' in the current working directory to store all my files for the upcoming project."
           **Explanation:** This request is very clear and specific. It provides a direct command ("create a new directory"), specifies the exact name of the folder ('project_data'), and indicates the location ("in the current working directory"). The instruction is unambiguous and provides all the necessary information to call the tool.
           **Tool Call:** `create_folder(path='project_data')`
        2. **User Request:** "I need to set up a place for my temporary log files. Can you make a folder called 'temp_logs' for this purpose?"
           **Explanation:** The user's intent is explicit. They are asking to "make a folder" and have provided the exact name 'temp_logs'. This is a clear, actionable instruction that allows for the tool to be invoked safely and effectively.
           **Tool Call:** `create_folder(path='temp_logs')`

        **Negative Examples:**
        1. **User Request:** "I need to organize my files."
           **Explanation:** This request is vague and lacks a specific target. The user's intention to organize files doesn't provide enough detail for a file system operation. Calling the `create_folder` tool would be a guess, potentially creating a folder the user didn't want. The correct action is to ask for clarification.
           **Correct Response:** "Please specify the name and location for the new folder you would like to create for your files."
        2. **User Request:** "My project needs a home."
           **Explanation:** The user is speaking metaphorically. While they may want a folder, the language "a home" is not a direct command to create one. Using the tool in this situation would be a guess. The system should not assume a file system action is required without a more direct request.
           **Correct Response:** "If you would like to create a new folder for your project, please tell me what to name it."
    """
    try:
        os.makedirs(path, exist_ok=True)
        return f"Created folder: {path}"
    except Exception as e:
        return f"Error: {e}"

def list_directory(path: str) -> list:
    """Lists all files and subdirectories in the specified directory.

    This function serves as a tool for listing directory contents. It should only be used
    when explicitly instructed to perform a file system operation.

    Args:
        path (str): The path of the directory to list.

    Returns:
        list: A list of file and directory names. Returns a list containing an error message on failure.

    Examples:
        **Positive Examples:**
        1. **User Request:** "I need to see what's inside the 'reports' folder to find the latest version. Can you list all the files and folders there?"
           **Explanation:** The user clearly states their goal is to "see what's inside" and provides a specific directory name ('reports'). The command "list all the files and folders" is an unambiguous instruction that directly maps to this tool's functionality.
           **Tool Call:** `list_directory(path='reports')`
        2. **User Request:** "What's in the current directory? I'm trying to find the 'data_processing.py' script."
           **Explanation:** The request "What's in the current directory?" is a direct query about the contents of the user's current location. This is a clear and simple command that the tool can fulfill immediately. The user's secondary goal of finding a specific file reinforces their intent to view the directory contents.
           **Tool Call:** `list_directory(path=os.getcwd())`

        **Negative Examples:**
        1. **User Request:** "Where are my files?"
           **Explanation:** This is a general question about file location and does not specify a directory to search. Calling `list_directory` on a default path (like the current directory) would be an assumption. The system must ask the user for a specific directory to avoid providing unhelpful information.
           **Correct Response:** "Please specify which folder you would like to list the contents of."
        2. **User Request:** "I can't find the 'image_assets' folder."
           **Explanation:** This is a statement of a problem, not a command to list a directory. The user may be looking for the folder in a specific location, or they may want to search the entire system (which this tool cannot do safely). The system should not blindly call `list_directory` but instead prompt the user for more information.
           **Correct Response:** "Would you like me to list the contents of a specific folder to help you find it? If so, please tell me the folder's name or path."
    """
    try:
        return os.listdir(path)
    except Exception as e:
        return [f"Error: {e}"]

def delete_item(path: str) -> str:
    """Deletes the specified file or folder.

    This function serves as a tool for deleting file system items. It should only be used
    when explicitly instructed to perform a file system operation. Exercise caution, as
    this action is irreversible.

    Args:
        path (str): The path of the item to delete.

    Returns:
        str: A message indicating the outcome of the operation (success or failure).

    Examples:
        **Positive Examples:**
        1. **User Request:** "I no longer need the 'archive_temp' folder and all its contents. Please permanently remove it."
           **Explanation:** This is a highly specific and direct command. The user identifies the exact folder name ('archive_temp'), confirms they want to remove "all its contents," and uses the phrase "permanently remove it." This clear and final instruction justifies a tool call.
           **Tool Call:** `delete_item(path='archive_temp')`
        2. **User Request:** "The file 'draft_old.txt' is just taking up space. Get rid of it for me."
           **Explanation:** The user provides the exact file name ('draft_old.txt') and a clear command to "get rid of it." The intent to delete is explicit and leaves no room for ambiguity, making it safe to invoke the tool.
           **Tool Call:** `delete_item(path='draft_old.txt')`

        **Negative Examples:**
        1. **User Request:** "This file is useless."
           **Explanation:** The user's statement expresses an opinion about a file but does not provide a command to delete it. Deleting the file based on this statement would be a dangerous assumption. The system must not act on such an ambiguous and non-commanding statement.
           **Correct Response:** "Which file are you referring to? Please provide a clear command if you would like me to delete it."
        2. **User Request:** "My project directory is getting too cluttered. I need to clean it up."
           **Explanation:** "Clean it up" is a broad and undefined instruction. It could mean deleting files, moving them, or just renaming them. This ambiguity means the system cannot safely call the `delete_item` tool. It must first ask for clarification on what specific actions to take.
           **Correct Response:** "What specific files or folders would you like to delete to clean up your project directory? Please provide a list."
    """
    try:
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)
        return f"Deleted: {path}"
    except Exception as e:
        return f"Error: {e}"

def rename_item(src: str, dest: str) -> str:
    """Renames a file or folder.

    This function serves as a tool for renaming file system items. It should only be used
    when explicitly instructed to perform a file system operation.

    Args:
        src (str): The current path of the item.
        dest (str): The new path for the item.

    Returns:
        str: A message indicating the outcome of the operation (success or failure).

    Examples:
        **Positive Examples:**
        1. **User Request:** "I want to change the name of the 'draft_final.docx' file to 'final_report.docx' for submission."
           **Explanation:** The user clearly states they want to "change the name" and provides both the original file path ('draft_final.docx') and the desired new name ('final_report.docx'). This level of detail makes the instruction unambiguous and ready for tool execution.
           **Tool Call:** `rename_item(src='draft_final.docx', dest='final_report.docx')`
        2. **User Request:** "The folder 'images' should really be called 'assets'. Please rename it for me."
           **Explanation:** This is a direct command to "rename" a specific folder ('images') to a new name ('assets'). The command is explicit and provides all the necessary arguments for the function, making it a perfect candidate for a tool call.
           **Tool Call:** `rename_item(src='images', dest='assets')`

        **Negative Examples:**
        1. **User Request:** "The name of this file is terrible."
           **Explanation:** This is a subjective comment, not a command. The user is expressing an opinion but has not specified which file to rename or what the new name should be. Acting on this would be a guess and could lead to errors or unwanted changes.
           **Correct Response:** "Which file would you like to rename, and what would you like the new name to be?"
        2. **User Request:** "I've decided to restructure my files. The filenames need to be updated."
           **Explanation:** The command "filenames need to be updated" is a general statement of intent without providing the crucial source and destination paths. It is not an explicit instruction to perform a rename operation on a specific file. The system must prompt for more details.
           **Correct Response:** "Please specify which file you would like to rename, and what its new name should be."
    """
    try:
        os.rename(src, dest)
        return f"Renamed {src} to {dest}"
    except Exception as e:
        return f"Error: {e}"

def move_file(src: str, dest: str) -> str:
    """Moves a file to a new location.

    This function serves as a tool for moving files. It should only be used
    when explicitly instructed to perform a file system operation.

    Args:
        src (str): The current path of the file.
        dest (str): The destination path for the file.

    Returns:
        str: A message indicating the outcome of the operation (success or failure).

    Examples:
        **Positive Examples:**
        1. **User Request:** "Please move the 'meeting_notes.txt' file from the 'current' directory into the 'archive/2024' folder."
           **Explanation:** The user provides a clear command ("move the... file"), the specific source file path ('current/meeting_notes.txt'), and the precise destination folder ('archive/2024'). All required parameters are available, so a tool call is appropriate.
           **Tool Call:** `move_file(src='current/meeting_notes.txt', dest='archive/2024/meeting_notes.txt')`
        2. **User Request:** "I need to put my 'final_report.pdf' into the 'submitted' folder now that I'm done with it."
           **Explanation:** The user explicitly states their intention to "put" (move) a specific file ('final_report.pdf') into a designated destination ('submitted' folder). This command is clear and contains all the information needed to perform the operation.
           **Tool Call:** `move_file(src='final_report.pdf', dest='submitted/final_report.pdf')`

        **Negative Examples:**
        1. **User Request:** "This file should be somewhere else."
           **Explanation:** The user's statement expresses a desire for a change in location but does not provide the specific file to move or the destination path. This is an incomplete instruction that cannot be acted upon.
           **Correct Response:** "Which file would you like to move, and where should I move it to? Please provide both the source and destination paths."
        2. **User Request:** "My 'reports' directory is getting full."
           **Explanation:** The user is describing a problem (a full directory) but has not requested a specific action. Moving files is one possible solution, but so is deleting or archiving. The system must not assume which action to take without a direct command.
           **Correct Response:** "Would you like me to move some files out of the 'reports' directory? If so, please specify which files and where they should go."
    """
    try:
        shutil.move(src, dest)
        return f"Moved {src} to {dest}"
    except Exception as e:
        return f"Error: {e}"

def read_file(path: str) -> str:
    """Reads the contents of a text file.

    This function serves as a tool for reading file contents. It should only be used
    when explicitly instructed to perform a file system operation.

    Args:
        path (str): The path of the file to read.

    Returns:
        str: The file contents as a string. Returns an error message on failure.

    Examples:
        **Positive Examples:**
        1. **User Request:** "Please open 'project_outline.txt' and show me the content so I can remember the next steps."
           **Explanation:** The user gives a clear command to "open" and "show the content" of a specific file ('project_outline.txt'). The intent is unambiguous and the tool has all the information it needs to proceed.
           **Tool Call:** `read_file(path='project_outline.txt')`
        2. **User Request:** "What are the instructions in the 'README.md' file?"
           **Explanation:** The request "What are the instructions in...?" is a direct query about the contents of a specified file ('README.md'). This is a clear instruction to read the file's content and is safe to execute.
           **Tool Call:** `read_file(path='README.md')`

        **Negative Examples:**
        1. **User Request:** "I need to get some information from a file."
           **Explanation:** This statement is too general. It doesn't specify which file the user wants to read. The system cannot guess the file and must ask for a clear, specific path.
           **Correct Response:** "Please tell me the name of the file you would like me to read."
        2. **User Request:** "Can you help me with my notes?"
           **Explanation:** The user is asking for general help with "notes" but hasn't specified which file contains those notes or what they want done with them. This is too vague to safely call the `read_file` tool.
           **Correct Response:** "If your notes are in a file, please provide the file name so I can read it for you."
    """
    try:
        with open(path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        return f"Error: {e}"

def write_file(path: str, content: str) -> str:
    """Writes content to a text file, overwriting existing content.

    This function serves as a tool for writing to a file. It should only be used
    when explicitly instructed to perform a file system operation.

    Args:
        path (str): The path of the file to write to.
        content (str): The content to write to the file.

    Returns:
        str: A message indicating the outcome of the operation (success or failure).

    Examples:
        **Positive Examples:**
        1. **User Request:** "I need to save the message 'Task completed successfully' into a file named 'status.log'."
           **Explanation:** The user gives a specific command to "save" content. They provide the exact content to be written ('Task completed successfully') and the precise file path ('status.log'). This command is complete and unambiguous.
           **Tool Call:** `write_file(path='status.log', content='Task completed successfully')`
        2. **User Request:** "Please write the following to 'config.ini': `[settings] mode = 'debug'`."
           **Explanation:** The user explicitly instructs the system to "write" a block of content to a specified file ('config.ini'). Both the content and the destination are clearly provided, justifying the tool call.
           **Tool Call:** `write_file(path='config.ini', content='[settings] mode = 'debug'')`

        **Negative Examples:**
        1. **User Request:** "I have some new data to save."
           **Explanation:** This is a statement of intent, but it lacks two crucial pieces of information: the file name and the content to be written. The tool cannot be called without these. The system must ask for these details.
           **Correct Response:** "Please tell me the name of the file you want to write to and what content you would like to save."
        2. **User Request:** "My script needs to log its status."
           **Explanation:** This is a description of a requirement. The system knows the script needs to log status, but it doesn't know where to log it or what specific status message to write. It cannot perform a write operation without a clear directive.
           **Correct Response:** "What is the file path and content you would like to log?"
    """
    try:
        with open(path, 'w', encoding='utf-8') as file:
            file.write(content)
        return f"Successfully wrote to {path}"
    except Exception as e:
        return f"Error: {e}"

def get_file_info(path: str) -> dict:
    """Gets information about a file or directory.

    This function serves as a tool for getting file metadata. It should only be used
    when explicitly instructed to perform a file system operation.

    Args:
        path (str): The path of the file or directory.

    Returns:
        dict: A dictionary containing file information (size, type, timestamps). Returns a dictionary with an error message on failure.

    Examples:
        **Positive Examples:**
        1. **User Request:** "Can you give me the details about the file 'main.py'? I need to know its size and when it was last modified."
           **Explanation:** The user directly asks for "details" about a specific file ('main.py') and specifies the exact information they want ("size and when it was last modified"). This is a clear, actionable request.
           **Tool Call:** `get_file_info(path='main.py')`
        2. **User Request:** "What are the properties of the 'assets' directory? I need to check its size."
           **Explanation:** The user uses the term "properties," which is a synonym for file info, and specifies a clear target ('assets' directory) and a specific detail they want to check ("its size"). This is a direct command that warrants a tool call.
           **Tool Call:** `get_file_info(path='assets')`

        **Negative Examples:**
        1. **User Request:** "My program is too big."
           **Explanation:** This is a subjective statement without a direct request for file information. "Too big" could refer to file size, but it's not a command. The system should not assume the user wants file information and should ask for clarification.
           **Correct Response:** "Are you referring to a specific file or folder? If so, please provide the path so I can check its size for you."
        2. **User Request:** "I need to know when my files were created."
           **Explanation:** This is a general statement of intent but lacks a specific target. It doesn't specify *which* files the user wants information about. The system cannot act without a clear path.
           **Correct Response:** "Please tell me the name of the file or folder you would like to get information about."
    """
    try:
        stat = os.stat(path)
        return {
            "path": path,
            "size": stat.st_size,
            "is_directory": os.path.isdir(path),
            "created": stat.st_ctime,
            "modified": stat.st_mtime
        }
    except Exception as e:
        return {"error": str(e)}

def get_current_directory() -> str:
    """Gets the current working directory.

    This function serves as a tool for getting the current directory path. It should only be used
    when explicitly instructed to perform a file system operation.

    Returns:
        str: The current working directory path. Returns an error message on failure.

    Examples:
        **Positive Examples:**
        1. **User Request:** "Can you tell me which directory I am currently in?"
           **Explanation:** The user's request is a direct and unambiguous question about their current location, using the phrase "which directory I am currently in." This maps directly to the tool's functionality.
           **Tool Call:** `get_current_directory()`
        2. **User Request:** "I need to know my present working directory."
           **Explanation:** "Present working directory" is a common technical term. This request is a direct, explicit query for a specific piece of information that the tool is designed to provide.
           **Tool Call:** `get_current_directory()`

        **Negative Examples:**
        1. **User Request:** "Where am I?"
           **Explanation:** The user's question is too general and could be interpreted metaphorically. While the user might be asking for their directory, they could also be confused about their place in the conversation or the project. The system should seek clarification to ensure the user is asking about the file system.
           **Correct Response:** "Are you asking for the current directory? If so, I can provide that for you."
        2. **User Request:** "What is the path?"
           **Explanation:** The user is asking for "the path" without any context. This could refer to a file path, a network path, or the current directory. The system cannot assume the user's intent.
           **Correct Response:** "Could you please specify which path you would like to know? For example, the path to a file or the current directory."
    """
    try:
        return os.getcwd()
    except Exception as e:
        return f"Error: {e}"

def create_file(path: str) -> str:
    """Creates a new empty file at the specified path.

    This function serves as a tool for creating an empty file. It should only be used
    when explicitly instructed to perform a file system operation.

    Args:
        path (str): The path where the file should be created.

    Returns:
        str: A message indicating the outcome of the operation (success or failure).

    Examples:
        **Positive Examples:**
        1. **User Request:** "I need to create a new, empty file called 'requirements.txt' for my project."
           **Explanation:** The user clearly states their intention to "create a new, empty file" and provides the exact name ('requirements.txt'). This is a direct command with all the necessary information.
           **Tool Call:** `create_file(path='requirements.txt')`
        2. **User Request:** "Please make a file named 'todo.md' in the current folder so I can write down my tasks."
           **Explanation:** The user gives a clear command to "make a file" and specifies the filename ('todo.md') and location ("in the current folder"). This instruction is perfectly suited for the tool.
           **Tool Call:** `create_file(path='todo.md')`

        **Negative Examples:**
        1. **User Request:** "I want to start a new document."
           **Explanation:** The user's statement is too abstract. It doesn't provide a file name. Starting a "new document" could also mean launching a text editor or a word processor, not necessarily creating an empty file on the file system.
           **Correct Response:** "Please tell me the name you would like for the new document file."
        2. **User Request:** "I need a place to write."
           **Explanation:** This is a vague request that doesn't mention files or creation. The user's need to "write" could be fulfilled in many ways. The system must not assume that creating a file is the desired action.
           **Correct Response:** "If you would like me to create a file for you to write in, please provide a file name."
    """
    try:
        with open(path, 'w') as file:
            pass
        return f"Created file: {path}"
    except Exception as e:
        return f"Error: {e}"