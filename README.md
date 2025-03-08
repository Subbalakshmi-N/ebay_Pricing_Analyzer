# ebay_Pricing_Analyzer

This project fetches product prices from eBay's API and applies a dynamic pricing strategy based on market trends, seller reviews, and feedback ratings.

## Features
- Fetches real-time product prices from eBay using the Browse API
- Allows sorting by **reviews, price, or positive feedback**
- Supports **price filtering (min/max price range)**
- Calculates **average, minimum, and maximum prices**
- Suggests an **optimal selling price**

---

## Installation
### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/your-username/ebay-dynamic-pricing.git
cd ebay-dynamic-pricing
```

### **2️⃣ Set Up a Virtual Environment (Optional but Recommended)**
```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate  # On Windows
```

### **3️⃣ Install Dependencies**
```bash
pip install -r requirements.txt
```

---

## Configuration
### **1️⃣ Get eBay API Credentials**
- Go to [eBay Developer Program](https://developer.ebay.com/)
- Create an application and get your **Client ID** and **Client Secret**

### **2️⃣ Set Up Your Credentials**
Replace the placeholders in the script:
```python
CLIENT_ID = "your client ID"
CLIENT_SECRET = "your client secret"
```

---

## Usage
Run the script and enter the product name when prompted:
```bash
python ebay_pricing.py
```

### **Example Workflow**
1. Enter a product name (e.g., `Laptop`)
2. Choose sorting preference (reviews, price, feedback)
3. Optionally, enter a price range (or leave blank to skip)
4. View the **market analysis and recommended selling price**

---

## Example Output
```
Enter the product name to analyze pricing: iPhone 13

=== Sorting Options ===
1. Sort by Reviews (default)
2. Sort by Price
3. Sort by Positive Feedback

Enter your sorting choice (1/2/3): 1

=== Filtering Options ===
Enter minimum price (or press Enter to skip): 500
Enter maximum price (or press Enter to skip): 1000

Fetching prices for: iPhone 13 (Sorted by reviews, Price Range: 500-1000)

=== eBay Pricing Analysis ===
🔹 Average Price: $750.00
🔹 Minimum Price: $699.00
🔹 Maximum Price: $999.00
✅ Recommended Selling Price: $724.50

=== Top Competitor Listings ===
📌 Apple iPhone 13 (Unlocked) 128GB - Midnight
💰 Price: 750 USD
⭐ Reviews: 120 Reviews | Positive Feedback: 98%
🔗 URL: https://cgi.sandbox.ebay.com/ws/eBayISAPI.dll?ViewItem&item=123456789
```

---

## License
This project is open-source and available under the [MIT License](LICENSE).

---

## Contributions
Feel free to submit a pull request or open an issue if you find a bug or have suggestions!

---

## Author
Developed by **Subbalakshmi N**

📧 Contact: subbalakshminarayanprasad@gmail.com

