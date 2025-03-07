import requests
import base64
import time
import json

# eBay API Credentials (Replace with your actual credentials)
CLIENT_ID = "your client ID"
CLIENT_SECRET = "your client secret"

# eBay OAuth URLs
TOKEN_URL = "https://api.sandbox.ebay.com/identity/v1/oauth2/token"
SEARCH_API_URL = "https://api.sandbox.ebay.com/buy/browse/v1/item_summary/search"


# ===================== 1️⃣ Generate eBay Access Token =====================
def get_ebay_access_token():
    """
    Function to generate an eBay OAuth access token.
    """
    credentials = f"{CLIENT_ID}:{CLIENT_SECRET}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    headers = {
        "Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type": "client_credentials",
        "scope": "https://api.ebay.com/oauth/api_scope"
    }

    response = requests.post(TOKEN_URL, headers=headers, data=data)

    if response.status_code == 200:
        token_info = response.json()
        return token_info["access_token"], token_info["expires_in"]
    else:
        print(f"❌ ERROR: {response.status_code}")
        print(f"🔴 Response: {response.text}")
        raise Exception("Failed to authenticate with eBay API.")

# ===================== 2️⃣ Fetch eBay Product Prices =====================
def fetch_ebay_prices(query, limit=5, sort_by="reviews", min_price=None, max_price=None):
    """
    Function to fetch product prices from eBay using the Browse API with sorting and filtering options.
    """
    access_token, _ = get_ebay_access_token()

    headers = {
        "Authorization": f"Bearer {access_token}",
        "X-EBAY-C-MARKETPLACE-ID": "EBAY_US",
        "Content-Type": "application/json",
    }

    params = {
        "q": query,
        "limit": limit
    }

    # Add price filter if specified
    if min_price is not None or max_price is not None:
        if min_price is None:
            min_price = ""
        if max_price is None:
            max_price = ""
        params["filter"] = f"price:[{min_price}..{max_price}]"

    response = requests.get(SEARCH_API_URL, headers=headers, params=params)

    if response.status_code == 200:
        items = response.json().get("itemSummaries", [])
        product_prices = []

        for item in items:
            title = item.get("title", "N/A")
            price = item.get("price", {}).get("value", "N/A")
            currency = item.get("price", {}).get("currency", "N/A")
            seller_reviews = item.get("seller", {}).get("reviews", 0)
            positive_feedback = item.get("seller", {}).get("positiveFeedbackPercentage", "N/A")
            url = f"https://cgi.sandbox.ebay.com/ws/eBayISAPI.dll?ViewItem&item={item.get('itemId', 'N/A')}"

            product_prices.append({
                "title": title,
                "price": float(price),
                "currency": currency,
                "reviews": seller_reviews,
                "positive_feedback": positive_feedback,
                "url": url
            })

        # Sort dynamically based on sort_by parameter
        if sort_by == "reviews":
            product_prices.sort(key=lambda x: x["reviews"], reverse=True)
        elif sort_by == "price":
            product_prices.sort(key=lambda x: x["price"])
        elif sort_by == "feedback":
            product_prices.sort(key=lambda x: x["positive_feedback"], reverse=True)

        return product_prices
    else:
        raise Exception(f"Error fetching eBay prices: {response.status_code}, {response.text}")

# ===================== 3️⃣ Dynamic Pricing Algorithm =====================
from urllib.parse import unquote  # Import for decoding URL-encoded strings

def dynamic_pricing(product_name):
    """
    Function to analyze market price and adjust pricing strategy with sorting and filtering options.
    """
    print("\n=== Sorting Options ===")
    print("1. Sort by Reviews (default)")
    print("2. Sort by Price")
    print("3. Sort by Positive Feedback")

    sort_choice = input("\nEnter your sorting choice (1/2/3): ")
    sort_by = "reviews"
    if sort_choice == "2":
        sort_by = "price"
    elif sort_choice == "3":
        sort_by = "feedback"

    print("\n=== Filtering Options ===")
    min_price = input("Enter minimum price (or press Enter to skip): ")
    max_price = input("Enter maximum price (or press Enter to skip): ")

    # Convert inputs to floats or None
    min_price = float(min_price) if min_price else None
    max_price = float(max_price) if max_price else None

    print(f"\nFetching prices for: {product_name} (Sorted by {sort_by}, Price Range: {min_price}-{max_price})")

    prices = fetch_ebay_prices(product_name, sort_by=sort_by, min_price=min_price, max_price=max_price)

    if not prices:
        print("No products found.")
        return

    # Extract all prices
    price_values = [p["price"] for p in prices]

    # Calculate pricing insights
    avg_price = sum(price_values) / len(price_values)
    min_price_found = min(price_values)
    max_price_found = max(price_values)

    # Set a dynamic selling price (Example Strategy)
    recommended_price = round((min_price_found + avg_price) / 2, 2)

    # Display results
    print("\n=== eBay Pricing Analysis ===")
    print(f"🔹 Average Price: ${avg_price:.2f}")
    print(f"🔹 Minimum Price: ${min_price_found:.2f}")
    print(f"🔹 Maximum Price: ${max_price_found:.2f}")
    print(f"✅ Recommended Selling Price: ${recommended_price:.2f}")

    print("\n=== Top Competitor Listings ===")

    for item in prices:
        # Decode URL-encoded title
        title = unquote(item['title']) if item['title'] != "N/A" else "Title Not Available"
        reviews = f"{item['reviews']} Reviews" if item['reviews'] > 0 else "No Reviews"
        feedback = f"{item['positive_feedback']}%" if item['positive_feedback'] != "N/A" else "Feedback Not Available"
        price = f"{item['price']} {item['currency']}" if item['price'] != "N/A" else "Price Not Available"
        url = item['url']

        # Shorten overly long titles for better display
        if len(title) > 50:
            title = title[:47] + "..."

        print(f"📌 {title}")
        print(f"💰 Price: {price}")
        print(f"⭐ Reviews: {reviews} | Positive Feedback: {feedback}")
        print(f"🔗 URL: {url}\n")


# =====================  Run the Dynamic Pricing =====================
if __name__ == "__main__":
    product_name = input("Enter the product name to analyze pricing: ")
    dynamic_pricing(product_name)
