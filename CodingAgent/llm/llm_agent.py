import sys
import os

sys.path.append(os.getcwd())

from camel.agents import ChatAgent
from camel.models import ModelFactory
from camel.types import ModelPlatformType, ModelType
from CodingAgent.utils.logging_info import setup_logging_config
from CodingAgent.llm.client_utils import load_apikey_config


# ----basic global loading----- #
logger = setup_logging_config()


class CodingAgent(ChatAgent):
    def __init__(
        self,
        system_message=None,
        model=None,
        memory=None,
        message_window_size=None,
        token_limit=None,
        output_language=None,
        tools=None,
        external_tools=None,
        response_terminators=None,
        scheduling_strategy="round_robin",
        single_iteration=False,
        # all the parameters are for the father class: ChatAgent
        model_platform: ModelPlatformType = ModelPlatformType.OPENAI,
        model_type: ModelType = ModelType.GPT_4O_MINI,
    ):
        # for basic config
        self.load_api_config()

        # default settings for config of self.effective model
        self.effective_model = ModelFactory.create(
            api_key=self.api_key,
            url=self.base_url,
            model_platform=model_platform,
            model_type=model_type,
        )

        super().__init__(
            system_message,
            self.effective_model,
            memory,
            message_window_size,
            token_limit,
            output_language,
            tools,
            external_tools,
            response_terminators,
            scheduling_strategy,
            single_iteration,
        )

    def load_api_config(self):
        self.api_key = load_apikey_config()[0]
        self.base_url = load_apikey_config()[1]


if __name__ == "__main__":
    # a simple test
    test = CodingAgent()
    response = test.step("Hello")
    print(response.msgs[0].content)
