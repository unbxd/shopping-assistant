import requests
import json
import urllib.parse

from config.config import PROXY_USER, PROXY_PASSWORD, PROXY_IP, PROXY_PORT, REGION_MIMIR_MAPPING



class MimirClient:

    if PROXY_USER and PROXY_PASSWORD and PROXY_IP and PROXY_PORT:
        proxies = {"http": f"http://{PROXY_USER}:{PROXY_PASSWORD}@{PROXY_IP}:{PROXY_PORT}"}
    else:
        proxies = {}

    @classmethod
    def fetch(cls, region, site_key, query, filters=None):
        mimir_endpoint = REGION_MIMIR_MAPPING[region]
        fields = "fields=name,imageUrl,price"
        rows = "rows=10"

        if not filters:
            url = f"{mimir_endpoint}/unbxd-search/{site_key}/search?q={query}&{fields}&{rows}"
        else:
            filter_query = " AND ".join([f"{key}:{urllib.parse.quote(value)}" for key, value in filters.items()])
            url = f"{mimir_endpoint}/unbxd-search/{site_key}/search?q={query}&{fields}&{rows}&filter={filter_query}"

        try:
            print(f"SOLR URL: {url}")
            resp = requests.request("GET", url, headers={"content-type": "application/json"}, proxies=cls.proxies)
            resp.raise_for_status()
            content = json.loads(resp.content)

        except Exception as e:
            print("Error %s occurred while getting api key" % (str(e)))
            content = {}

        facets = content.get("facets", {}).get("text", {}).get("list", [])
        updated_facets = []
        for facet in facets:
            name = facet["filterField"]
            options = [f for i, f in enumerate(facet["values"]) if i%2 != 1]

            if (filters is not None) and (name in filters.keys()):
                continue

            if name not in {"diet_uFilter","brandName_uFilter","allCategoryNames_uFilter","price"}:
                continue

            if len(options) > 2:
                updated_facets.append({"filter_field": name, "filter_options": options})

        products = []
        for product in content.get("response", {}).get("products", []):
            products.append({
                "productId": product["uniqueId"],
                "title": product["name"],
                "imageUrl": product["imageUrl"][0] if isinstance(product["imageUrl"], list) else product["imageUrl"],
                "productUrl": product["imageUrl"][0] if isinstance(product["imageUrl"], list) else product["imageUrl"],
                "price": product["price"]
            })

        return {
            "num_products": content.get("response", {}).get("numberOfProducts", 0),
            "products": products,
            "facets": updated_facets
        }

if __name__ == "__main__":
    all_sites = {}
    client = MimirClient()
    _response = client.fetch("eu-west-2", "ss-unbxd-prod-waitrose37331668673646", "apples",
                             {})
    print(json.dumps(_response, indent=4))
    print("\n\n")


    _response = client.fetch("eu-west-2", "ss-unbxd-prod-waitrose37331668673646", "apples",
                             {"diet_uFilter": "eggfree", "brandName_uFilter": "Ella's Kitchen"})
    print(json.dumps(_response, indent=4))
    # print([site for site in all_sites if (site is not None) and ("lulu" in site)])
    print("\n\n")


    _response = client.fetch("eu-west-2", "ss-unbxd-prod-waitrose37331668673646", "apples",
                             {"diet_uFilter": "eggfree", "brandName_uFilter": "Robinsons"})
    print(json.dumps(_response, indent=4))
    # print([site for site in all_sites if (site is not None) and ("lulu" in site)])
