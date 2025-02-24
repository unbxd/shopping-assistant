from pydantic import BaseModel
from openai import OpenAI
from typing import List
import json
from config.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


def generate_chat_response(vertical: str, messages: List, products: List) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Using 4o-mini model
        messages=[
            {"role": "system",
             "content": f"You are a chatbot for '{vertical}' vertical. Read the old chat messages, and also we have some products that we will be showing to the user. Generate a friendly response to show to the user alongside the products. **Do not give me the products information in the response**, as those will be shown, just give me a chat response."},
            *[{"role": msg[0], "content": msg[1]} for msg in messages],
            {"role": "system",
              "content": f"Here are the products that will be shown to the user: {json.dumps(products, indent=4)}"}
        ],
    )

    query = response.choices[0].message.content

    print(f"Generated Chat Response: {query}")
    return query


if __name__ == "__main__":
    # Example 1: Single message query
    history1 = [
        ["user", "I need some apples."],
    ]
    query1 = generate_chat_response("grocery", history1, [])
    print("Example 1 Query:", query1)

    # Example 2: Multi-turn conversation with specific grocery request
    history2 = [
        ["user", "aplles"],
        ["assistant", "Do you prefer any particular brand?"],
        ["user", "Waitrose"],
    ]
    query2 = generate_chat_response("grocery", history2, [
        {
            "productId": "088663",
            "title": "Waitrose Pink Lady Apples",
            "imageUrl": "https://ecom-su-static-prod.wtrecom.com/images/products/11/LN_088663_BP_11.jpg",
            "productUrl": "https://ecom-su-static-prod.wtrecom.com/images/products/11/LN_088663_BP_11.jpg",
            "price": 2.75
        },
        {
            "productId": "088643",
            "title": "Waitrose Braeburn Apples min 5",
            "imageUrl": "https://ecom-su-static-prod.wtrecom.com/images/products/11/LN_088643_BP_11.jpg",
            "productUrl": "https://ecom-su-static-prod.wtrecom.com/images/products/11/LN_088643_BP_11.jpg",
            "price": 1.8
        },
        {
            "productId": "088628",
            "title": "Waitrose Royal Gala Apples",
            "imageUrl": "https://ecom-su-static-prod.wtrecom.com/images/products/11/LN_088628_BP_11.jpg",
            "productUrl": "https://ecom-su-static-prod.wtrecom.com/images/products/11/LN_088628_BP_11.jpg",
            "price": 1.8
        },
        {
            "productId": "027969",
            "title": "Waitrose Pink Lady Apples",
            "imageUrl": "https://ecom-su-static-prod.wtrecom.com/images/products/11/LN_027969_BP_11.jpg",
            "productUrl": "https://ecom-su-static-prod.wtrecom.com/images/products/11/LN_027969_BP_11.jpg",
            "price": 3
        },
        {
            "productId": "029108",
            "title": "Essential Mini Apples",
            "imageUrl": "https://ecom-su-static-prod.wtrecom.com/images/products/11/LN_029108_BP_11.jpg",
            "productUrl": "https://ecom-su-static-prod.wtrecom.com/images/products/11/LN_029108_BP_11.jpg",
            "price": 1.2
        },
        {
            "productId": "008825",
            "title": "Waitrose Jazz Apples",
            "imageUrl": "https://ecom-su-static-prod.wtrecom.com/images/products/11/LN_008825_BP_11.jpg",
            "productUrl": "https://ecom-su-static-prod.wtrecom.com/images/products/11/LN_008825_BP_11.jpg",
            "price": 2.45
        },
        {
            "productId": "511572",
            "title": "Waitrose Smitten Apples",
            "imageUrl": "https://ecom-su-static-prod.wtrecom.com/images/products/11/LN_511572_BP_11.jpg",
            "productUrl": "https://ecom-su-static-prod.wtrecom.com/images/products/11/LN_511572_BP_11.jpg",
            "price": 2.1
        },
        {
            "productId": "088637",
            "title": "Waitrose Granny Smith Apples",
            "imageUrl": "https://ecom-su-static-prod.wtrecom.com/images/products/11/LN_088637_BP_11.jpg",
            "productUrl": "https://ecom-su-static-prod.wtrecom.com/images/products/11/LN_088637_BP_11.jpg",
            "price": 1.95
        },
        {
            "productId": "076788",
            "title": "Waitrose Jazz Apples",
            "imageUrl": "https://ecom-su-static-prod.wtrecom.com/images/products/11/LN_076788_BP_11.jpg",
            "productUrl": "https://ecom-su-static-prod.wtrecom.com/images/products/11/LN_076788_BP_11.jpg",
            "price": 2.6
        },
        {
            "productId": "098595",
            "title": "Waitrose Braeburn Apples",
            "imageUrl": "https://ecom-su-static-prod.wtrecom.com/images/products/11/LN_098595_BP_11.jpg",
            "productUrl": "https://ecom-su-static-prod.wtrecom.com/images/products/11/LN_098595_BP_11.jpg",
            "price": 1.9
        }
    ])
    print("Example 2 Query:", query2)
