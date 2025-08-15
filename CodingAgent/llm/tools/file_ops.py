import os
import shutil

def create_folder(path: str) -> str:
    """创建新文件夹"""
    try:
        os.makedirs(path, exist_ok=True)
        return f"Created folder: {path}"
    except Exception as e:
        return f"Error: {e}"

def list_directory(path: str) -> list:
    """列出指定目录下的所有文件和子目录"""
    try:
        return os.listdir(path)
    except Exception as e:
        return [f"Error: {e}"]

def delete_item(path: str) -> str:
    """删除指定的文件或文件夹"""
    try:
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)
        return f"Deleted: {path}"
    except Exception as e:
        return f"Error: {e}"

def rename_item(src: str, dest: str) -> str:
    """重命名文件或文件夹"""
    try:
        os.rename(src, dest)
        return f"Renamed {src} to {dest}"
    except Exception as e:
        return f"Error: {e}"

def move_file(src: str, dest: str) -> str:
    """移动文件到新路径"""
    try:
        shutil.move(src, dest)
        return f"Moved {src} to {dest}"
    except Exception as e:
        return f"Error: {e}"