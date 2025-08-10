"""LLM agent for coding tasks."""
import os
import sys
sys.path.append(os.getcwd())

from camel.agents import ChatAgent
from camel.models import ModelFactory
from camel.types import ModelPlatformType, ModelType
from CodingAgent.utils.logging_info import setup_logging_config
from CodingAgent.llm.client_utils import load_apikey_config


logger = setup_logging_config()


class CodingAgent(ChatAgent):
    """Coding agent that extends the base ChatAgent with specific configurations for coding tasks."""
    
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
        model_platform: ModelPlatformType = ModelPlatformType.ZHIPU,
        model_type: ModelType = ModelType.GLM_4,
    ):
        """Initialize the CodingAgent.
        
        Args:
            system_message: System message for the agent.
            model: Model to use for the agent.
            memory: Memory module for the agent.
            message_window_size: Size of the message window.
            token_limit: Token limit for the agent.
            output_language: Language for the agent's output.
            tools: Tools available to the agent.
            external_tools: External tools available to the agent.
            response_terminators: Response terminators for the agent.
            scheduling_strategy: Strategy for scheduling messages.
            single_iteration: Whether to run only a single iteration.
            model_platform: Platform for the model.
            model_type: Type of model to use.
        """
        # Load API configuration
        self.load_api_config()

        # Default settings for config of self.effective model
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
        """Load API configuration from environment variables."""
        self.api_key = load_apikey_config()[0]
        self.base_url = load_apikey_config()[1]


if __name__ == "__main__":
    # A simple test
    test = CodingAgent()
    response = test.step("Hello")
    print(response.msgs[0].content)
