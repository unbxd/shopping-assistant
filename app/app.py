import time
import random
import copy
import uvicorn
from clients import MimirClient
from chat import chat
from fastapi import FastAPI, Request

app = FastAPI()
mimir_client = MimirClient()

SCRIPTS = {
    "hosting a party": [
        {
            "response": "What kind of party is it, and is there any specific theme to it?",
            "products": [],
            "options": []
        },
        {
            "response": "What dietary preferences or restrictions do you have in mind for your party?",
            "products": [],
            "options": ["nutfree", "peanutfree", "eggfree", "vegetarian", "lowsugar", "dairyfree", "vegan", "soyafree",
                        "fairtrade", "glutenfree", "low", "fat"]
        },
        {
            "response": "That sounds like a fantastic idea! Hosting a vegetarian party can be a lot of fun with so many delicious options to choose from. I’ve got some great suggestions for you that will wow your guests and keep the party vibe going. Let's check them out!",
            "products": ["party supplies", {"diet_uFilter": "vegetarian"}],
            "options": []
        },
        {
            "response": "Dumplings are a fantastic choice for a party! They’re sure to be a hit with your guests. I have some delicious dumpling options that you can serve up. Check them out below and let me know which ones you'd like to include in your menu!",
            "products": ["dumplings", {"diet_uFilter": "vegetarian"}],
            "options": []
        }
    ]
}


class Script:
    def __init__(self):
        self.uids = {}

    @staticmethod
    def find_script(text):
        found = None
        for key in SCRIPTS.keys():
            if key in text:
                found = key

        if not found:
            raise NameError("Invalid text")

        return SCRIPTS[found]

    def chat(self, uid, text):
        if uid not in self.uids:
            script = self.find_script(text)
            self.uids[uid] = copy.deepcopy(script)

        if len(self.uids[uid]) > 0:
            first_response = self.uids[uid].pop(0)
        else:
            del self.uids[uid]
            return self.chat(uid, text)

        response_message = first_response["response"]
        product_query = first_response["products"]
        products = []
        if len(product_query) == 2:
            query, filters = product_query
            products = mimir_client.fetch("eu-west-2", "ss-unbxd-prod-waitrose37331668673646",
                                          query, filters)["products"]
        options = first_response["options"]

        response = {
            "as_resp": "",
            "context": "",
            "assistant_resp": response_message,
            "products": products,
            "facets": {},
            "follow_up_question": {
                "options": options,
                "question": response_message
            },
            "msTaken": 1,
            "product_summary_resp": response_message,
            "suggested_filters": options,
            "suggested_queries": ""
        }

        time.sleep(random.randint(1000, 2500) / 1000)

        return response


script_client = Script()


@app.post("/v1.0/verticals/{vertical}/recommend/chat")
async def chat_endpoint(vertical, req: Request):
    uid = req.query_params.get('uid')
    request_data = await req.json()
    text = request_data.get('text', '')

    try:
        response = script_client.chat(uid, text)

    except (NameError, KeyError):
        response = chat(vertical, uid, text)

    return response


if __name__ == "__main__":
    uvicorn.run("app:app", port=8000, reload=True)
