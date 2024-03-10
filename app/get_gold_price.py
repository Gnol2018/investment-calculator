import requests
from lxml import html

# Send a GET request to the website
url = "https://sjc.com.vn/giavang/textContent.php"
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
# Parse the HTML content
    tree = html.fromstring(response.content)

    # Extract the price of gold using XPath
    price_1l_10l_1kg_buy = tree.xpath('//td[contains(text(), "SJC 1L, 10L, 1KG")]/following-sibling::td[1]/span/text()')[0]
    print("SJC 1L, 10L, 1KG - Buy Price:", price_1l_10l_1kg_buy.strip())

    price_1l_10l_1kg_sell = tree.xpath('//td[contains(text(), "SJC 1L, 10L, 1KG")]/following-sibling::td[2]/span/text()')[0]
    print("SJC 1L, 10L, 1KG - Sell Price:", price_1l_10l_1kg_sell.strip())

else:
    print("Failed to retrieve the webpage.")
