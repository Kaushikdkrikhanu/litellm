from typing import Optional
from pydantic import BaseModel
# import litellm
from litellm import completion
import os


class InvestigationOutput(BaseModel):
    alert_explanation: Optional[str] = None
    investigation: Optional[str] = None
    conclusions_and_possible_root_causes: Optional[str] = None
    next_steps: Optional[str] = None
    related_logs: Optional[str] = None
    app_or_infra: Optional[str] = None
    external_links: Optional[str] = None

os.environ["AZURE_API_KEY"] = "DT6eVnaObSlCjDQv28KrFkqEez4kB7hqIvO4v9QRdXEgP4oXwteAJQQJ99BBACHYHv6XJ3w3AAAAACOGQhJR"
os.environ["AZURE_API_BASE"] = "https://ai-kaushikd2861ai626826707682.openai.azure.com/"
os.environ["AZURE_API_VERSION"] = "2024-10-21"


tools = [
  {
    "type": "function",
    "function": {
      "name": "get_current_time",
      "description": "Returns the current date and time",
      "strict": True,
      "parameters": {
        "properties": {
          "timezone": {
            "type": "string",
            "description": "The timezone to get the current time for (e.g., 'UTC', 'America/New_York')"
          }
        },
        "required": [
            "timezone"
        ],
        "type": "object",
        "additionalProperties": False,
      }
    }
  }
]

response = completion(
    model = "azure/gpt-4",
    messages=[
        {
            "role": "system",
            "content": "You are a tool-calling AI assist provided with common devops and IT tools that you can use to troubleshoot problems or answer questions.\nWhenever possible you MUST first use tools to investigate then answer the question."
        },
        {
            "role": "user",
            "content": "What is the current date and time in NYC?"
        }
    ],
    drop_params=True,
    temperature=0.00000001,
    tools=tools,
    tool_choice='auto',
    response_format=InvestigationOutput, # commenting this line will cause the output to be correct
)


# response = litellm.completion(
#     model = "azure/gpt-4o-mini", 
#     messages = [{ "content": "Hello, how are you?","role": "user"}]
# )

print(response.to_json())