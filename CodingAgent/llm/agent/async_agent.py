import asyncio
import os
import sys

sys.path.append(os.getcwd())
from openai import AsyncOpenAI
from CodingAgent.llm.agent.context import BaseContextManager
from CodingAgent.llm.agent.base_agent import BaseAgent
from CodingAgent.llm.tools.tool_manager import AsyncToolManager


class AsyncAgent(BaseAgent):
    def __init__(self, llm_config, stream_callback=None):
        super().__init__(llm_config)
        self.stream_callback = stream_callback
        self.async_client = AsyncOpenAI(
            base_url=self.llm_config.base_url, api_key=self.llm_config.api_key
        )

    def check_condition(self, input_str):
        return super().check_condition(input_str)

    async def stream_api_iterator(self, prompt: str):
        try:
            stream = await self.async_client.completions.create(
                model=self.llm_config.model,
                prompt=prompt,
                stream=True,
                **self.llm_config.generation_config,
            )
            async for chunk in stream:
                text = chunk.choices[0].text

                yield text

        except Exception as e:
            print(f"Error while calling API: {e}")
            yield f"Error while calling API: {e}"

    async def __stream_api_iterator(self, prompt: str, should_stop_func=None):
        try:
            stream = await self.async_client.completions.create(
                model=self.llm_config.model,
                prompt=prompt,
                stream=True,
                **self.llm_config.generation_config,
            )
            async for chunk in stream:
                if should_stop_func and should_stop_func():
                    break

                chunk_content = ""

                # 处理DeepSeek-R1的双流输出，ds有reasoning_content，利用这两个字段的互斥关系来给 token 打个标
                if (
                    hasattr(chunk.choices[0], "delta")
                    and hasattr(chunk.choices[0].delta, "reasoning_content")
                    and chunk.choices[0].delta.reasoning_content
                ):
                    chunk_content = chunk.choices[0].delta.reasoning_content
                    yield chunk_content, True  # (content, in_reasoning)
                elif not hasattr(chunk.choices[0], "delta"):
                    chunk_content = chunk.choices[0].text
                    yield chunk_content, True  # (content, in_reasoning)
                elif chunk.choices[0].delta.content:
                    chunk_content = chunk.choices[0].delta.content
                    yield chunk_content, False  # (content, in_reasoning)

        except Exception as e:
            print(f"Error while calling API: {e}")
            yield None, False

    async def async_call_api_with_callback(self, prompt: str, should_stop_func=None):
        """支持实时回调的异步API调用"""
        full_response = ""
        in_reasoning = False
        previous_in_reasoning = False

        async for chunk_result in self.__stream_api_iterator(
            prompt=prompt, should_stop_func=should_stop_func
        ):
            if chunk_result[0] is None:
                continue

            chunk_content, current_in_reasoning = chunk_result

            if previous_in_reasoning and not current_in_reasoning:
                # adding </think>
                if "</think>" not in chunk_content and "</think>" not in full_response:
                    chunk_content = "</think>\n" + chunk_content
                in_reasoning = False
            else:
                in_reasoning = current_in_reasoning

            clean_chunk = chunk_content.replace("<think>", "")
            full_response += clean_chunk

            # 实时异步回调
            if self.stream_callback:
                await self.stream_callback(clean_chunk, full_response, in_reasoning)
            else:
                print(clean_chunk, end="", flush=True)

            # 检查停止条件
            if self.check_condition(full_response):
                break

            previous_in_reasoning = current_in_reasoning

        return full_response.strip()

    async def async_call_api(self, prompt: str):
        full_response = ""
        async for result in self.stream_api_iterator(prompt=prompt):
            print(result, end="", flush=True)
            full_response += result

            stop_flag = self.check_condition(full_response)

            if stop_flag:
                break
        return full_response.strip()

    async def async_step(self, input_prompt: str):
        step_response = await self.async_call_api(input_prompt)
        agent_response, tool_call_content = self.extract_tool_content(step_response)
        return {"step_response": agent_response, "tool_call_content": tool_call_content}

    async def async_step_with_callback(self, input_prompt: str, should_stop_func=None):
        """执行单步推理并支持异步回调"""
        try:
            step_response = await self.async_call_api_with_callback(
                input_prompt, should_stop_func
            )
            agent_response, tool_call_content = self.extract_tool_content(step_response)

            return {
                "step_response": agent_response.strip(),
                "tool_call_content": tool_call_content.strip(),
            }
        except Exception as e:
            print(f"[ERROR] async_step_with_callback failed: {e}")
            return {"step_response": f"Error: {str(e)}", "tool_call_content": ""}

    async def async_step_callback(self, input_prompt: str):
        """保持向后兼容的异步步骤方法"""
        return await self.async_step_with_callback(input_prompt)


async def demo_usage():
    # basic llm config
    llm_config = {
        "model": "deepseek-r1",
        "base_url": "http://127.0.0.1:8888/v1/",
        "generation_config": {"max_tokens": 16384, "temperature": 0.5},
        # control stop condition
        "stop_condition": r"<code[^>]*>((?:(?!<code).)*?)</code>",
        # control tool condition
        "tool_condition": r"<code[^>]*>((?:(?!<code).)*?)</code>",
    }
    async_agent = AsyncAgent(llm_config=llm_config)

    # loading chat template from jinja template
    with open(
        "/data/xiyuanyang/Agent/tool_backends/MCP/server/ProbeCode/template/r1_tool.jinja",
        "r",
        encoding="utf-8",
    ) as f:
        chat_template = f.read()

    # loading context manager and tool manager
    context_manager = BaseContextManager(chat_template=chat_template)
    tool_manager = AsyncToolManager(url="http://127.0.0.1:30010")
    prompt_base_dir = "/data/xiyuanyang/Agent/tool_backends/MCP/server/ProbeCode/CodingAgent/llm/prompt"

    # getting user_prompt and assistant prefix
    problem_to_solve = "What happened in Shanghai Jiao Tong University?"
    prompt_path = os.path.join(prompt_base_dir, "initial_prompt.md")
    with open(prompt_path, encoding="utf-8") as file:
        user_prompt = (file.read()).format(problem=problem_to_solve)
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
        result = await async_agent.async_step_callback(prompt)
        context_manager.log_agent(result["step_response"])

        if not result["tool_call_content"]:
            break
        context_manager.log_tool_call(result["tool_call_content"])
        tool_result = await tool_manager.execute_tool_async(result["tool_call_content"])
        context_manager.log_tool_call_result(tool_result)
        print(tool_result)


if __name__ == "__main__":
    asyncio.run(demo_usage())
