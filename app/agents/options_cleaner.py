from pydantic import BaseModel
from openai import OpenAI
from typing import List
import json
from config.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


def generate_valid_options(solr_query: str, filters: dict, follow_up_query: str, options: List[str]) -> List[str]:
    response = client.chat.completions.create(
        model="gpt-4o",  # Using 4o-mini model
        messages=[
            {
                "role": "system",
                "content": (
                    # "You will be given a query asked by the user (for grocery vertical) along with any existing filters. Next, you'll receive a follow-up question that includes several filter options. "
                    # "Your task is to analyze the query and the options, and provide high scores to options which are useful for the user to further narrow their search. "
                    # "Provide scores (from 0 to 1) that will help user to filter down the products "
                    "You are a smart scoring agent. Your task is to analyse the options and check which options are suitable to show to the users which can help in filtering the products in result set."
                    "If the query pertains to a product category where every product inherently satisfies a particular filter (i.e., 100% of the products meet that filter), give low score to that option (< 0.4). "
                    "Return your answer as JSON in the following format: {\"filtered_options\": {\"option 1\": 0.9xx, \"option 2\": 0.8xx, ...}}."
                )
            },
            {
                "role": "user",
                "content": f"{solr_query}"
            },
            {
                "role": "assistant",
                "content": f"{follow_up_query}"
            },
            {
                "role": "system",
                "content": f"Options to be cleaned: {options}"
            },
        ],
        response_format={"type": "json_object"},
    )

    try:
        data = json.loads(response.choices[0].message.content)
        scores = data.get("filtered_options", [])
        print(scores)
        new_options = [i for i, score in scores.items() if score >= 0.5]
        # if len(new_options) == 0:
        #     new_options = [i for i, score in scores.items() if score >= 0.1]
        if len(new_options) == 0:
            new_options = [i for i, score in scores.items()]

    except:
        print(response.choices[0].message.content)
        new_options = []

    print(f"Generated options: {new_options}")
    return new_options


if __name__ == "__main__":
    # Example 1: Single message query
    query1 = generate_valid_options("apples", {}, "What specific dietary needs or preferences do you have in mind?", [
        "vegetarian",
        "eggfree",
        "peanutfree",
        "soyafree",
        "nutfree",
        "glutenfree",
        "vegan",
        "dairyfree",
        "lowfat",
        "ownlabel",
        "organic",
        "lowsugar",
        "essentialrange",
        "fairtrade"
    ])
    print("Example 1 Query:", query1)

    # Example 2: Multi-turn conversation with specific grocery request
    query2 = generate_valid_options("apples", {"diet_uFilter": "vegetarian"}, "Which brand are you interested in?", [
        "Waitrose Ltd",
        "Ella's Kitchen",
        "Innocent",
        "Aspall",
        "innocent"
    ])
    print("Example 2 Query:", query2)
