from openai import OpenAI
import json
from config.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


def generate_filter_question(filter_options) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Using 4o-mini model
        messages=[
            {"role": "system",
             "content": f"Your task is to ask follow up question on the top facet in a friendly way. Give me only the query that should be asked to the user, so based on their response, I can apply filter and show the products. **Do not give options in your query**, I will be showing options to the user directly in the UI. **Make sure to ask in super friendly way like a human, do not just give me a straight up blunt question. Don't use any greetings, as those are already sent at the start of the chat.**"},
            {"role": "system", "content": json.dumps(filter_options, indent=4)},
        ],
    )

    query = response.choices[0].message.content

    print(f"Generated Filter Question: {query}")
    return query


if __name__ == "__main__":
    query1 = generate_filter_question(
        {"brandName_uFilter": ['Waitrose Ltd', "Ella's Kitchen", 'Innocent', 'Aspall', 'innocent']})
    print("Example 1 Query:", query1)

    query2 = generate_filter_question({'diet_uFilter':
                                    ['vegetarian', 'eggfree', 'peanutfree', 'soyafree', 'nutfree', 'glutenfree',
                                     'vegan', 'dairyfree', 'lowfat', 'ownlabel', 'organic', 'lowsugar',
                                     'essentialrange', 'fairtrade']})
    print("Example 2 Query:", query2)
