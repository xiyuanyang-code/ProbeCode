import re
import sys
import os

sys.path.append(os.getcwd())

from typing import Dict, List, Any
from openai import OpenAI
from CodingAgent.llm.agent.utils import LLMConfig
from CodingAgent.llm.agent.context import BaseContextManager
from CodingAgent.llm.tools.tool_manager import BaseToolManager


class BaseAgent:
    def __init__(self, llm_config: Dict[str, Any]):

        self.llm_config: LLMConfig = LLMConfig(llm_config)
        self.client = OpenAI(
            base_url=self.llm_config.base_url, api_key=self.llm_config.api_key
        )

    def check_condition(self, input_str: str):
        if not self.llm_config.stop_condition:
            return False
        matches = list(
            re.finditer(self.llm_config.stop_condition, input_str, re.DOTALL)
        )
        return len(matches) > 0

    def extract_tool_content(self, input_str: str):
        if not self.llm_config.tool_condition:
            return input_str, ""
        matches = list(
            re.finditer(self.llm_config.tool_condition, input_str, re.DOTALL)
        )
        detected_num = len(matches)

        if detected_num > 0:
            match = matches[0]
            code_content = match.group(1)
            match_start_index = match.start()
            cut_text = input_str[:match_start_index]

            return cut_text, code_content

        return input_str, ""

    def call_api(self, prompt: str):
        try:
            with self.client.completions.create(
                model=self.llm_config.model,
                prompt=prompt,
                stream=True,
                **self.llm_config.generation_config,
            ) as stream:
                full_response = ""

                # stream output
                for chunk in stream:
                    if "delta" in chunk.choices[0]:
                        if chunk.choices[0].delta.content is not None:
                            content = chunk.choices[0].delta.content
                            if self.llm_config.is_debug:
                                print(content, end="", flush=True)
                            full_response += content
                    else:
                        content = chunk.choices[0].text
                        if self.llm_config.is_debug:
                            print(content, end="", flush=True)
                        full_response += content

                    stop_flag = self.check_condition(full_response)

                    if stop_flag:
                        return full_response.strip()

        except KeyboardInterrupt:
            print("Error, the response is key borad interrupted!")
            # 在这里可以添加任何额外的清理操作，例如关闭连接池或日志记录
        except Exception as e:
            print(f"发生错误: {e}")
            # ! more release can be added here

        return full_response.strip()

    def step(self, input_prompt: str):
        step_response = self.call_api(input_prompt)
        agent_response, tool_call_content = self.extract_tool_content(step_response)
        return {"step_response": agent_response, "tool_call_content": tool_call_content}


def demo_usage():
    # basic llm config
    llm_config = {
        "model": "GLM-4.5",
        "base_url": "http://127.0.0.1:8889/v1/",
        "generation_config": {"max_tokens": 16384, "temperature": 0.5},
        # control stop condition
        "stop_condition": r"<code[^>]*>((?:(?!<code).)*?)</code>",
        # control tool condition
        "tool_condition": r"<code[^>]*>((?:(?!<code).)*?)</code>",
    }
    base_agent = BaseAgent(llm_config=llm_config)

    # loading chat template from jinja template
    with open(
        "/data/xiyuanyang/Agent/tool_backends/MCP/server/ProbeCode/template/r1_tool.jinja",
        "r",
        encoding="utf-8",
    ) as f:
        chat_template = f.read()

    # loading context manager and tool manager
    context_manager = BaseContextManager(chat_template=chat_template)
    tool_manager = BaseToolManager(url="http://127.0.0.1:30010")

    # getting user_prompt and assistant prefix
    user_prompt = f"""The problem is: 1+1=?
Solve the problem with the help of feedback from a code executor. Every time you write a piece of code between <code> and </code>, the code inside will be executed. For example, when encounting numerical operations, you might write a piece of code to inteprete the math problem into python code and print the final result in the code. Based on the reasoning process and the executor feedback, you could write code to help answering the question for multiple times (either for gaining new information or verifying). There are also several integrated tools that can be used to help you solve the problem. The available tools are:
1. web_search(keywords), this function takes keywords as input, which is a string, and the output is a string containing several web information. This function will call a web search engine to return the search results. This tool is especially useful when answering knowledge-based questions."""
    assistant_prefix = f"""<think>\nOkay, to answer the user's question, I will answer user's problem by deep reasoning together with writing python code. For example\n1.If I want to use the tool of web_search(keywords), will say <code>\nkeywords=...\nresults=web_search(keywords)\nprint(results)\n</code> to call the tool.\n2.If I want to do computation, I will write code for accurate result: <code>\na = 123\nb = 456\nprint(a+b)\n</code>.\n\nNow, let me analyze the user's question."""

    # initialize agent logs
    context_manager.agent_logs = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": user_prompt},
        {"role": "assistant", "content": assistant_prefix},
    ]

    # build chat loops
    while True:
        prompt = context_manager.build_input_prompt()
        print(f"The prompt is:\n{prompt} \n\n")
        result = base_agent.step(prompt)
        context_manager.log_agent(result["step_response"])

        if not result["tool_call_content"]:
            break
        context_manager.log_tool_call(result["tool_call_content"])
        tool_result = tool_manager.execute_tool(result["tool_call_content"])
        context_manager.log_tool_call_result(tool_result)
        print(tool_result)


if __name__ == "__main__":
    print("For simple demo usage!")
    demo_usage()
