import os
import sys
import json
import warnings

from CodingAgent.llm.agent.context import BaseContextManager
from CodingAgent.llm.agent.base_agent import BaseAgent
from CodingAgent.llm.tools.tool_manager import AsyncToolManager, StreamToolManager
from CodingAgent.llm.agent.base_chat import BaseChat
from CodingAgent.llm.agent.async_agent import AsyncAgent
from contextlib import redirect_stderr, contextmanager

DEV_NULL = "nul" if sys.platform.startswith("win") else "/dev/null"


class DevNull:
    def write(self, msg):
        pass

    def flush(self):
        pass


@contextmanager
def suppress_stderr():
    """临时将 sys.stderr 重定向到 /dev/null（或一个空对象）。"""

    original_stderr = sys.stderr
    sys.stderr = DevNull()

    try:
        yield
    finally:
        sys.stderr = original_stderr


class ProbeCodeAgent(BaseChat):
    """
    一个集成了 LLM (AsyncAgent), 上下文管理 (BaseContextManager)
    和异步工具执行 (AsyncToolManager) 的异步对话 Agent。
    """

    def __init__(self, config_file: str = "config.json"):
        super().__init__(config_file)
        llm_config = self.config.get("llm_config", {})
        tool_server_url = self.config.get("tool_server_url")
        chat_template_path = self.config.get("chat_template_path")
        prompt_base_dir = self.config.get("prompt_base_dir")

        if not all([llm_config, tool_server_url, chat_template_path, prompt_base_dir]):
            self.logger.error(
                "Configuration missing critical keys (llm_config, tool_server_url, chat_template_path, prompt_base_dir)."
            )
            return

        self.llm_config = llm_config
        self.prompt_base_dir = prompt_base_dir
        self.agent = AsyncAgent(
            llm_config=self.llm_config, stream_callback=self._llm_stream_callback
        )

        with open(chat_template_path, "r", encoding="utf-8") as file:
            chat_template = file.read()

        self.context_manager = BaseContextManager(chat_template=chat_template)
        self.tool_manager = AsyncToolManager(url=tool_server_url)
        self.assistant_prefix = self._get_assistant_prefix()

    def _get_assistant_prefix(self):
        """
        生成或加载 Agent 的初始回复前缀和工具调用指南。
        """
        # todo remove hard coding
        return """<think>
Okay, to answer the user's question, I will answer user's problem by deep reasoning together with writing python code. For example
1.If I want to use the tool of web_search(keywords), will say <code>\nkeywords=...\nresults=web_search(keywords)\nprint(results)\n</code> to call the tool.
2.If I want to do computation, I will write code for accurate result: <code>\na = 123\nb = 456\nprint(a+b)\n</code>.

Now, let me analyze the user's question.</think>"""

    async def _llm_stream_callback(
        self, content: str, full_response: str, in_reasoning: bool
    ):
        """
        AsyncAgent 的实时流式输出回调函数。
        """
        print(content, end="", flush=True)

    def _initialize_context(self, user_query: str):
        """
        为每次新的用户查询初始化上下文和 Agent 日志。
        """
        prompt_path = os.path.join(self.prompt_base_dir, "initial_prompt.md")
        with open(prompt_path, encoding="utf-8") as file:
            user_prompt = (file.read()).format(problem=user_query)

        self.context_manager.agent_logs = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_prompt},
            {"role": "assistant", "content": self.assistant_prefix},
        ]

    async def _process_query(self, query: str):
        """
        实现 BaseChat 的核心逻辑，处理用户输入并运行多步 Agent 循环。
        """
        self.user_chat.display_system_message("Agent Running...")
        self._initialize_context(query)

        while True:
            prompt = self.context_manager.build_input_prompt()

            print("\n[AGENT]: ", end="")
            result = await self.agent.async_step_with_callback(prompt)
            print("\n")

            step_response = result.get("step_response", "")
            tool_call_content = result.get("tool_call_content", "")
            self.context_manager.log_agent(step_response)

            if not tool_call_content.strip():
                self.user_chat.display_system_message("Agent Stop")
                break

            self.context_manager.log_tool_call(tool_call_content)
            tool_result = await self.tool_manager.execute_tool_async(tool_call_content)
            self.context_manager.log_tool_call_result(tool_result)
            self.user_chat.display_system_message(
                f"工具执行结果:\n{tool_result.get('output')}"
            )


# =========================================================
# Demo
# =========================================================

# =========================================================
# for user mode: use 2>/dev/null to redirect stderr
# for debug mode: do not use it~
# todo write an argparse to implement this
# =========================================================
if __name__ == "__main__":
    with open(DEV_NULL, "w") as f_null:
        with redirect_stderr(f_null):
            try:
                agent = ProbeCodeAgent()
                agent.chat_loop()
            except Exception as e:
                print(f"Error in Running Agent: {e}")
