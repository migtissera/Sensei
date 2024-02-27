import json
import numpy as np

from concurrent.futures import ThreadPoolExecutor
from llm_handler import send_to_llm
from params import OUTPUT_FILE_PATH, NUM_WORKERS, PROVIDER

from system_messages import (
    SYSTEM_MESSAGES_ORCA,
    SYSTEM_MESSAGES_TESS,
    SYSTEM_MESSAGES_CODE,
)
from topics import TOPICS

code_data = False

if code_data:
    SYSTEM_MESSAGES = SYSTEM_MESSAGES_CODE
    PROMPT_1 = """For the following SUBJECT_AREA, generate a question that covers a very narrow topic in the SUBJECT_AREA, with sufficient depth and breadth. The topic in the question should be important to the SUBJECT_AREA, with known-answers present. The generated question should be detailed, seek true nature of our universe from first principles, curiosity invoking, thought provoking, and also should be able to be answered by an intelligence like yourself. Make sure the question is sufficiently harder and multi-part, like a graduate level course question. The question should seek an answer with computer code."""

else:
    SYSTEM_MESSAGES = SYSTEM_MESSAGES_ORCA + SYSTEM_MESSAGES_TESS
    PROMPT_1 = """For the following SUBJECT_AREA, generate a question that covers a very narrow topic in the SUBJECT_AREA, with sufficient depth and breadth. The topic in the question should be important to the SUBJECT_AREA, with known-answers present. The generated question should be detailed, seek true nature of our universe from first principles, curiosity invoking, thought provoking, and also should be able to be answered by an intelligence like yourself. Make sure the question is sufficiently harder and multi-part, like a graduate level course question."""


msg_context = {"role": "system", "content": str(PROMPT_1)}


def generate_data(
    topic_selected,
    system_message_generation,
    system_message_selected,
    OUTPUT_FILE_PATH,
):
    system_contexts = [
        system_message_generation,
        system_message_selected,
    ]

    user_prompts = [f"SUBJECT_AREA: {topic_selected}"]
    gpt_outputs = []

    for pp in range(len(system_contexts)):
        msg_list = []
        msg_system = {"role": "system", "content": str(system_contexts[pp])}
        msg_list.append(msg_system)
        msg_prompt = {"role": "user", "content": user_prompts[pp]}
        msg_list.append(msg_prompt)

        llm_response, llm_usage = send_to_llm(PROVIDER, msg_list)

        user_prompts.append(llm_response)
        gpt_outputs.append(llm_response)

    data = {
        "system": system_contexts[1],
        "instruction": str(user_prompts[1]),
        "response": str(gpt_outputs[1]),
    }

    with open(OUTPUT_FILE_PATH, "a") as output_file:
        output_file.write(json.dumps(data) + "\n")

    return data, llm_usage


def main():
    nn = 0
    failed = 0
    with ThreadPoolExecutor(max_workers=NUM_WORKERS) as executor:
        # Create a list of futures, one for each topic
        futures = []
        for _ in range(NUM_WORKERS):
            topic_number = np.random.randint(0, len(TOPICS))
            topic_selected = TOPICS[topic_number]
            system_message_number = np.random.randint(0, len(SYSTEM_MESSAGES))
            system_message_selected = SYSTEM_MESSAGES[system_message_number]
            system_message_generation = PROMPT_1
            futures.append(
                executor.submit(
                    generate_data,
                    topic_selected,
                    system_message_generation,
                    system_message_selected,
                    OUTPUT_FILE_PATH,
                )
            )

        # Wait for all futures to complete
        for future in futures:
            data, gpt_usage = future.result()
            if gpt_usage is not None:
                nn += 1
                print(data)
                print(
                    f"Generation {nn} Complete, Token usage: {gpt_usage}, Failed: {failed}"
                )
            else:
                failed += 1
            print("=" * 132)


while True:
    main()
