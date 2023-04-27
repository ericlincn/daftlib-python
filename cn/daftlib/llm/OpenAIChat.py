from cn.daftlib.utils.OpenAIUtil import OpenAIUtil
from cn.daftlib.utils.VarUtil import VarUtil
import openai
import json
import tiktoken

class OpenAIChat:

    model_name: str = "gpt-3.5-turbo"
    """Model name to use."""
    temperature: float = 0.7
    """What sampling temperature to use."""
    max_tokens: int = None
    """Maximum number of tokens to generate."""
    streaming: bool = False
    """Whether to stream the results or not."""
    n: int = 1
    """Number of chat completions to generate for each prompt."""

    def __init__(self, openai_api_key:str = None, openai_organization:str = None) -> None:

        if not openai_api_key:
            openai_api_key = VarUtil.getVarByEnv("OPENAI_API_KEY")

        if not openai_organization:
            openai_organization = VarUtil.getVarByEnv("OPENAI_ORGANIZATION", "")
        
        if openai_api_key:
            openai.api_key = openai_api_key
        
        if openai_organization:
            openai.organization = openai_organization
    
    def completion(self, messages:list) -> str:
        payload = {
            "model": self.model_name,
            "messages": messages
        }
        return OpenAIUtil.sendRequest("/chat/completions", payload)
    
    def completion2(self, messages:list) -> str:

        try:
            response = openai.ChatCompletion.create(
                model = self.model_name,
                messages = messages
            )
            return json.dumps(response)
        except openai.OpenAIError as e:
            print("OpenAIError:", e)

    def getNumTokens(self, messages:list) -> int:

        model = self.model_name
        if model == "gpt-3.5-turbo":
            # gpt-3.5-turbo may change over time.
            # Returning num tokens assuming gpt-3.5-turbo-0301.
            model = "gpt-3.5-turbo-0301"
        elif model == "gpt-4":
            # gpt-4 may change over time.
            # Returning num tokens assuming gpt-4-0314.
            model = "gpt-4-0314"

        # Returns the number of tokens used by a list of messages.
        try:
            encoding = tiktoken.encoding_for_model(model)
        except KeyError:
            print("Warning: model not found. Using cl100k_base encoding.")
            encoding = tiktoken.get_encoding("cl100k_base")

        if model == "gpt-3.5-turbo-0301":
            # every message follows <im_start>{role/name}\n{content}<im_end>\n
            tokens_per_message = 4
            # if there's a name, the role is omitted
            tokens_per_name = -1
        elif model == "gpt-4-0314":
            tokens_per_message = 3
            tokens_per_name = 1
        else:
            raise NotImplementedError(
                f"get_num_tokens_from_messages() is not presently implemented "
                f"for model {model}."
                "See https://github.com/openai/openai-python/blob/main/chatml.md for "
                "information on how messages are converted to tokens."
            )
        num_tokens = 0
        for message in messages:
            num_tokens += tokens_per_message
            for key, value in message.items():
                num_tokens += len(encoding.encode(value))
                if key == "name":
                    num_tokens += tokens_per_name
        # every reply is primed with <im_start>assistant
        num_tokens += 3
        return num_tokens