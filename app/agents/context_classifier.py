from pydantic import BaseModel
from openai import OpenAI
from typing import List
import json
from config.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


def classify_chat(messages: List) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Using 4o-mini model
        messages=[
            {"role": "system",
             "content": "Classify if the latest user message starts a new topic or continues the old conversation. If the latest message references a subject from a previous message (e.g., follow-up questions like 'And what about...?' referring to an earlier topic), classify it as 'old_conversation'. Since I am generating SOLR query as well as filters, so if user wants to see different product now, then tag as 'new_conversation', also if it is first user message. Give me the response in JSON format - {\"classification\": \"old_conversation\"} or {\"classification\": \"new_conversation\"}"},
            *[{"role": msg[0], "content": msg[1]} for msg in messages],
        ],
        response_format={"type": "json_object"},
    )

    try:
        data = json.loads(response.choices[0].message.content)
        convo_type = data.get("classification", "old_conversation")
    except:
        print(response.choices[0].message.content)
        convo_type = "old_conversation"

    print(f"Convo Type: {convo_type}")
    return convo_type


if __name__ == "__main__":
    # Example 1: Short conversation (3 messages, ending with user)
    history1 = [
        ["user", "What is the capital of France?"],
        ["assistant", "The capital of France is Paris."],
        ["user", "And what about Germany?"],
    ]
    classification1 = classify_chat(history1)
    print("Example 1:", classification1)
    assert classification1 == "old_conversation"

    # Example 2: Long conversation with old context (5 messages)
    history2 = [
        ["user", "Tell me about black holes."],
        ["assistant",
                "Black holes are regions of spacetime where gravity is so strong that nothing can escape."],
        ["user", "What about wormholes?"],
        ["assistant",
                "Wormholes are theoretical passages through space-time that could create shortcuts for long journeys."],
        ["user", "Are they related to black holes?"],
    ]
    classification2 = classify_chat(history2)
    print("Example 2:", classification2)
    assert classification2 == "old_conversation"

    # Example 3: Long conversation with a new context (5 messages)
    history3 = [
        ["user", "Tell me about photosynthesis."],
        ["assistant",
                "Photosynthesis is the process by which green plants convert light into energy."],
        ["user", "What is the role of chlorophyll?"],
        ["assistant",
                "Chlorophyll is a pigment that helps in absorbing light energy for photosynthesis."],
        ["user", "What is the capital of Japan?"],
    ]
    classification3 = classify_chat(history3)
    print("Example 3:", classification3)
    assert classification3 == "new_conversation"
