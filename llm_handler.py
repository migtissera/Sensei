import openai
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

from params import OPENAI_MODEL, OPENAI_API_KEY, MISTRALAI_MODEL, MISTRALAI_API_KEY

openai.api_key = OPENAI_API_KEY


def send_to_chatgpt(msg_list):
    completion = openai.ChatCompletion.create(
        model=OPENAI_MODEL, temperature=0.5, messages=msg_list
    )
    chatgpt_response = completion.choices[0].message["content"]
    chatgpt_usage = completion.usage
    return chatgpt_response, chatgpt_usage


def send_to_mistral(msg_list):
    client = MistralClient(api_key=MISTRALAI_API_KEY)

    messages = []
    for message in msg_list:
        messages.append(ChatMessage(role=message["role"], content=message["content"]))

    chat_response = client.chat(
        model=MISTRALAI_MODEL,
        messages=messages,
    )

    mistral_response = chat_response.choices[0].message.content
    mistral_usage = chat_response.usage
    return mistral_response, mistral_usage


def send_to_llm(provider, msg_list):
    if provider == "openai":
        response, usage = send_to_chatgpt(msg_list)
    elif provider == "mistral":
        response, usage = send_to_mistral(msg_list)
    return response, usage
