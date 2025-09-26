"""MCP tools for parsing files loading file_structure, only need to read json file"""

import json
import os
import sys

sys.path.append(os.getcwd())

# ! 因为 MCP 环境运行在沙盒中，因此原来文件的地址信息需要变化为 Docker 容器内部的挂载卷的映射地址
DOCKER_FILE_PATH = "/mnt/tool_backends/MCP/server/ProbeCode"
ENVIRONMENT_FILE_PATH = os.path.join(DOCKER_FILE_PATH, ".environment")

# mcp settings
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("code-parser")


# several utility functions
def _get_file_data(file_path: str):
    file_path = str(os.path.abspath(file_path)).replace(os.sep, "@").replace(".py", ".json")
    file_path = f"environ_{file_path}"
    with open(f"./.environment/{file_path}", "r", encoding="utf-8") as file:
        json_data = json.load(file)
    return json_data


# for file
# todo add rule-based methods and restrictions for this function
@mcp.tool()
def read_all_file_content():
    pass


if __name__ == "__main__":
    data = _get_file_data("./CodingAgent/main.py")
    print(json.dumps(data, ensure_ascii=False, indent=2))
