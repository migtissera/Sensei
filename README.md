# Sensei (先生)
A simple, powerful, minimal codebase to generate synthetic data using OpenAI, MistralAI or AnthropicAI

![alt text](Sensei.png)

# How to run

- `pip install openai mistralai numpy`

## Choose your provider: OpenAI or MistralAI
- Change `PROVIDER` under `params.py`
- `openai`, `mistral` or `anthropic`

### For OpenAI
- Change `GPT_MODEL`, `OPENAI_API_KEY` and `OUTPUT_FILE_PATH` under `params.py`

### For MistralAI
- Change `MISTRALAI_MODEL`, `MISTRALAI_API_KEY` and `OUTPUT_FILE_PATH` under `params.py`

### For AnthropicAI
- Change `ANTHROPICAI_MODEL`, `ANTHROPICAI_API_KEY` and `OUTPUT_FILE_PATH` under `params.py`

## Run Sensei
- Run with `python main.py`

# Optional

- Change the topics in `topics.py`
- Change the system contexts in `system_messages.py`
- Change the number of workers in `params.py`