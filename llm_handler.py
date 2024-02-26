import openai
from params import GPT_MODEL, OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY


def send_to_chatgpt(msg_list):
    completion = openai.ChatCompletion.create(
        model=GPT_MODEL, temperature=0.5, messages=msg_list
    )
    chatgpt_response = completion.choices[0].message
    return chatgpt_response, completion.usage
