import json

from chat_store import ChatStore
from agents import generate_solr_query, classify_chat, generate_filter_question, generate_chat_response
from clients import MimirClient
from config.config import DEMO_SITES

chat_store_client = ChatStore()
mimir_client = MimirClient()


def chat(vertical, user_id, user_query):
    print(f"Input - {vertical=}, {user_id=}, {user_query=}")

    site_key = DEMO_SITES.get(vertical, "grocery")["site_key"]
    region = DEMO_SITES.get(vertical, "grocery")["region"]

    user_info = chat_store_client.fetch(user_id)
    msg_history = user_info.get("messages", [])
    solr_query = user_info.get("solr_query", "")
    all_filters = user_info.get("all_filters", [])
    prev_filter_field = user_info.get("prev_filter_field", "")
    prev_options = user_info.get("prev_options", [])
    print(f"Fetched User Info: {user_info}")

    msg_history.append(["user", user_query])

    if user_query in prev_options:
        all_filters.append([prev_filter_field, user_query])
    else:
        chat_type = classify_chat(msg_history)

        if chat_type == "new_conversation":
            msg_history = [["user", user_query]]
            all_filters = []
            prev_filter_field = ""
            prev_options = []

        solr_query = generate_solr_query(vertical, msg_history)

    mimir_response = mimir_client.fetch(region, site_key, solr_query, {k:v for k, v in all_filters})
    products = mimir_response["products"]
    facets = mimir_response.get("facets", [])

    options = []
    if (mimir_response.get("num_products") > 100) and (len(facets) > 0) and (len(all_filters) <= 3):
        top_facet = mimir_response["facets"][0]
        options = top_facet["filter_options"]
        all_filters.append([top_facet["filter_field"], options])
        prev_filter_field = top_facet["filter_field"]
        prev_options = options
        products = []
        response = generate_filter_question(top_facet)
    else:
        response = generate_chat_response(vertical, msg_history, products)

    msg_history.append(["assistant", response])

    chat_store_client.update(user_id, {
        "messages": msg_history,
        "all_filters": all_filters,
        "solr_query": solr_query,
        "prev_filter_field": prev_filter_field,
        "prev_options": prev_options
    })

    full_response = {
        "response": response,
        "options": options,
        "products": products
    }
    print(f"{json.dumps(full_response, indent=4)}\n\n\n\n")
    return full_response


if __name__ == "__main__":
    ver = "grocery"
    uid = "123"


    class SampleData:
        def __init__(self, text):
            self.text = text


    chat_store_client.delete(uid)

    _data = SampleData("show me some apples")
    _ = chat(ver, uid, _data.text)
    # print(_)

    _data = SampleData(_["options"][0])
    _ = chat(ver, uid, _data.text)
    # print(_)

    _data = SampleData(_["options"][0])
    _ = chat(ver, uid, _data.text)
    # print(_)

    _data = SampleData("oranges")
    _ = chat(ver, uid, _data.text)
    # print(_)

    _data = SampleData(_["options"][0])
    _ = chat(ver, uid, _data.text)
    # print(_)

    _data = SampleData(_["options"][0])
    _ = chat(ver, uid, _data.text)
    # print(_)
