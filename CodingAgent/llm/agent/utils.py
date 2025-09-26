from typing import Dict, Any, List
import openai


class LLMConfig:
    def __init__(self, input_dict: Dict[str, Any]):
        if "model" not in input_dict.keys():
            print("WARNING! model is not in input dict.")
        if "base_url" not in input_dict.keys():
            print("WARNING! base_url is not in input dict.")
        self.model = input_dict["model"]
        self.base_url = input_dict["base_url"]

        self.api_key = (
            input_dict["api_key"] if "api_key" in input_dict.keys() else "EMPTY"
        )
        self.generation_config = (
            input_dict["generation_config"]
            if "generation_config" in input_dict.keys()
            else {}
        )
        self.stop_condition = (
            input_dict["stop_condition"]
            if "stop_condition" in input_dict.keys()
            else None
        )
        self.tool_condition = (
            input_dict["tool_condition"]
            if "tool_condition" in input_dict.keys()
            else None
        )
        self.is_debug = (
            input_dict["is_debug"] if "is_debug" in input_dict.keys() else None
        )
