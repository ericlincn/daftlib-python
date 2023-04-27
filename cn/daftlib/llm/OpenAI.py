from cn.daftlib.utils.OpenAIUtil import OpenAIUtil
from cn.daftlib.utils.VarUtil import VarUtil
import openai
import json
import tiktoken

class OpenAI:

    model_name: str = "text-davinci-003"
    """Model name to use."""
    temperature: float = 0.7
    """What sampling temperature to use."""
    max_tokens: int = 256
    """The maximum number of tokens to generate in the completion.
    -1 returns as many tokens as possible given the prompt and
    the models maximal context size."""
    top_p: float = 1
    """Total probability mass of tokens to consider at each step."""
    frequency_penalty: float = 0
    """Penalizes repeated tokens according to frequency."""
    presence_penalty: float = 0
    """Penalizes repeated tokens."""
    n: int = 1
    """How many completions to generate for each prompt."""
    best_of: int = 1
    """Generates best_of completions server-side and returns the "best"."""
    streaming: bool = False
    """Whether to stream the results or not."""

    def __init__(self, openai_api_key:str = None, openai_organization:str = None) -> None:

        if not openai_api_key:
            openai_api_key = VarUtil.getVarByEnv("OPENAI_API_KEY")

        if not openai_organization:
            openai_organization = VarUtil.getVarByEnv("OPENAI_ORGANIZATION", "")
        
        if openai_api_key:
            openai.api_key = openai_api_key
        
        if openai_organization:
            openai.organization = openai_organization

    def completion(self, prompt:str, stop:str = "\n") -> str:
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "n": self.n,
            "stream": self.streaming,
            # "logprobs": null,
            "stop": stop
        }
        return OpenAIUtil.sendRequest("/completions", payload)
    
    def completion2(self, prompt:str, stop:str = "\n") -> str:

        try:
            response = openai.Completion.create(
                model = self.model_name,
                prompt = prompt,
                max_tokens = self.max_tokens,
                temperature = self.temperature,
                top_p = self.top_p,
                n = self.n,
                stream = self.streaming,
                stop = stop
            )
            return json.dumps(response)
        except openai.OpenAIError as e:
            print("OpenAIError:", e)

    def getNumTokens(self, text:str) -> int:
        # create a GPT-3.5-Turbo encoder instance
        enc = tiktoken.encoding_for_model(self.model_name)
        # encode the text using the GPT-3.5-Turbo encoder
        tokenized_text = enc.encode(text)
        # calculate the number of tokens in the encoded text
        return len(tokenized_text)