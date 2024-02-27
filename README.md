# Sensei (先生)
A simple, powerful, minimal codebase to generate synthetic data using OpenAI

![alt text](Sensei.png)

# How to run

- `pip install openai mistralai numpy`

## Choose your provider: OpenAI or MistralAI

### For OpenAI
- Change `GPT_MODEL`, `OPENAI_API_KEY` and `OUTPUT_FILE_PATH` under `params.py`

### For MistralAI
- Change `MISTRALAI_MODEL`, `MISTRALAI_API_KEY` and `OUTPUT_FILE_PATH` under `params.py`

- Run with `python main.py`

# Optional

- Change the topics in `topics.py`
- Change the system contexts in `system_messages.py`
- Change the number of workers in `params.py`