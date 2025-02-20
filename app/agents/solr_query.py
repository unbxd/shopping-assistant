from pydantic import BaseModel
from openai import OpenAI
from typing import List
import json
from config.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)



def generate_solr_query(vertical: str, messages: List) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Using 4o-mini model
        messages=[
            {"role": "system",
             "content": f"Extract the key {vertical}-related search term based on the latest user message. Return only the extracted search term in JSON format - {{\"query\": \"apple\"}}"},
            *[{"role": msg[0], "content": msg[1]} for msg in messages],
        ],
        response_format={"type": "json_object"},
    )

    try:
        data = json.loads(response.choices[0].message.content)
        query = data.get("query", "")
    except:
        print(response.choices[0].message.content)
        query = ""

    print(f"Generated SOLR Query: {query}")
    return query


if __name__ == "__main__":
    # Example 1: Single message query
    history1 = [
        ["user", "I need some apples."],
    ]
    query1 = generate_solr_query("grocery", history1)
    print("Example 1 Query:", query1)

    # Example 2: Multi-turn conversation with specific grocery request
    history2 = [
        ["user", "I'm looking for cooking oil."],
        ["assistant", "Do you need refined or unrefined oil?"],
        ["user", "Refined oil, please."],
    ]
    query2 = generate_solr_query("grocery", history2)
    print("Example 2 Query:", query2)

    # Example 3: Multi-turn conversation with multiple groceries mentioned
    history3 = [
        ["user", "I need some fresh fruits."],
        ["assistant", "What kind of fruits are you looking for?"],
        ["user", "Yellow ripe mangoes."],
        ["assistant", "Would you like any other fruits?"],
        ["user", "No, just mangoes."],
    ]
    query3 = generate_solr_query("grocery", history3)
    print("Example 3 Query:", query3)

    # Example 3: Multi-turn conversation with multiple groceries mentioned
    history3 = [
        ["user", "chocolates"],
        ["assistant", "Any dietary preferences?"],
        ["user", "egg-free and dark"],
        ["assistant", "Which brand"],
        ["user", "Amul"],
    ]
    query3 = generate_solr_query("grocery", history3)
    print("Example 4 Query:", query3)
