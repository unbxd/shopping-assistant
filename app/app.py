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
            "response": "That sounds fantastic! Let’s make sure your party is a hit. What kind of celebration are you planning?",
            "products": [],
            "options": ["Casual Get-Together", "Dinner Party", "Kids’ Birthday Party", "Cocktail Party", "Outdoor BBQ", "Themed Party", "Other"]
        },
        {
            "response": "Love it! Think delicious cake, easy-to-eat bites, refreshing drinks, and some decoration. Let’s start with snacks—what sounds good?",
            "products": [],
            "options": ["Finger Foods", "Casual Bites", "A Mix of Both"]
        },
        {
            "response": "Great choice! Quick, tasty, and mess-free. Do you have any dietary preferences for your guests?",
            "products": [],
            "options": ["Nut-Free", "Peanut-Free", "Egg-Free", "Vegetarian", "Low-Sugar", "Dairy-Free", "Vegan", "Soy-Free", "Fair Trade", "Gluten-Free", "Low-Fat", "No preference"]
        },
        {
            "response": "Perfect! Here are some amazing vegetarian snack options to keep everyone happy.",
            "products": ["party snacks", {"diet_uFilter": "vegetarian"}],
            "options": []
        },
        {
            "response": "Excellent pick! Dumplings are always a crowd-pleaser. Here are some tasty vegetarian options:",
            "products": ["dumpling", {"diet_uFilter": "vegetarian"}],
            "options": []
        },
        {
            "response": "Dipping sauce makes everything better! Here are dumpling options that come with a flavorful dip:",
            "products": ["dumpling with dip", {"diet_uFilter": "vegetarian"}],
            "options": []
        },
        {
            "response": "Of course! Here are more vegetarian-friendly snack ideas to keep your guests munching happily:",
            "products": ["party snacks", {"diet_uFilter": "vegetarian"}],
            "options": []
        },
        {
            "response": "Great idea! Vegetarian nuggets are a guaranteed hit. Here are some options to choose from:",
            "products": ["nuggets", {"diet_uFilter": "vegetarian"}],
            "options": []
        },
        {
            "response": "Would you like a dipping sauce with those?",
            "products": [],
            "options": ["Yes", "No"]
        },
        {
            "response": "Here are a few fun dipping sauce options",
            "products": ["sauce with dip", {"diet_uFilter": "vegetarian"}],
            "options": []
        },
        {
            "response": "Classic choice! Your snack table is shaping up nicely. Would you like to move on, or check out more snack options?",
            "products": [],
            "options": ["Move on to the next item", "Look at more snack options"]
        },
        {
            "response": "We haven’t covered desserts yet! Would you like to add something sweet, like cookies or brownies?",
            "products": [],
            "options": ["Yes", "No"]
        },
        {
            "response": "Brownies? Great pick! Here are some delicious options your guests will love:",
            "products": ["brownies", {"diet_uFilter": "vegetarian"}],
            "options": []
        },
        {
            "response": "Fantastic choice. Now, shall we move on to drinks?",
            "products": [],
            "options": ["Yes", "No, I want to see more dessert options"]
        },
        {
            "response": "Are you planning to serve alcohol at your party?",
            "products": [],
            "options": ["Yes", "No"]
        },
        {
            "response": "What kind of drinks are you looking for?",
            "products": [],
            "options": ["Beer", "Whiskey and Scotch", "Wine", "Cocktail mix", "Other"]
        },
        {
            "response": "Sure! Any particular brewery you’d like to go for?",
            "products": [],
            "options": ["BrewDog", "Beavertown", "Fuller’s", "Adnams", "Birra Moretti"]
        },
        {
            "response": "Great choice! Here are some Birra Moretti beers that pair well with your vegetarian menu:",
            "products": ["beer", {"diet_uFilter": "vegetarian", "brandName_uFilter": "Birra Moretti"}],
            "options": []
        },
        {
            "response": "Absolutely! What’s your decor style for the party?",
            "products": [],
            "options": ["Minimalist & Elegant", "Colorful & Fun", "Rustic & Cozy", "Themed Party Décor", "Other"]
        },
        {
            "response": "Love it! A lively setup will set the mood. Here are some decoration options that’ll add fun and energy to your space:",
            "products": ["party decor", {}],
            "options": []
        },
        {
            "response": "Great! Now, let’s talk about the cake. Which flavor of cake do you have in mind?",
            "products": [],
            "options": ["Chocolate", "Vanilla", "Cheesecake", "Fruit Cake", "No Preference"]
        },
        {
            "response": "Sure. Here are a few cake options.",
            "products": ["cake", {}],
            "options": []
        },
        {
            "response": "That sounds fun! Here are some undecorated cake options:",
            "products": ["undecorated cake", {}],
            "options": []
        },
        {
            "response": "Classic and always a hit! Would you like to add cake decorating supplies like icing, sprinkles, or candles?",
            "products": [],
            "options": ["Yes", "No, I already have those"]
        },
        {
            "response": "Sounds like you’re all set! Anything else you'd like to add?",
            "products": [],
            "options": ["Yes", "No"]
        },
        {
            "response": "Perfect! Your party is going to be amazing. Let me know if you need anything else. Have a fantastic celebration!",
            "products": [],
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

        sleep_duration = 0
        sleep_duration += random.randint(1000, 1500) / 1000
        if options:
            sleep_duration += random.randint(100, 300) / 1000 + len(options) * random.randint(40, 60) / 1000
        if products:
            sleep_duration += random.randint(100, 300) / 1000
        time.sleep(sleep_duration)

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
