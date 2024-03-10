from fastapi import FastAPI, HTTPException
import httpx
import requests
from lxml import html

app = FastAPI()

COINGECKO_API_URL = "https://api.coingecko.com/api/v3"


@app.get("/")
def read_root():
    return {"message": "Welcome to Bitcoin HODL calculator API! Test"}


@app.get("/calculate/")
async def calculate_hodl(initial_investment: float, current_price: float, years: int):
    """
    Calculate the future value of a Bitcoin HODL investment.
    """
    # Assuming simple annual compounding
    future_value = initial_investment * (
        1 + (0.07 * years)
    )  # 7% annual growth rate for Bitcoin
    return {"future_value": future_value}


@app.get("/sjc-gold-price")
async def get_sjc_gold_price():
    try:
        url = "https://sjc.com.vn/giavang/textContent.php"
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content
            tree = html.fromstring(response.content)

            # Extract the price of gold using XPath
            price_1l_10l_1kg_buy = tree.xpath(
                '//td[contains(text(), "SJC 1L, 10L, 1KG")]/following-sibling::td[1]/span/text()'
            )[0]
            price_1l_10l_1kg_sell = tree.xpath(
                '//td[contains(text(), "SJC 1L, 10L, 1KG")]/following-sibling::td[2]/span/text()'
            )[0]

            # Create a dictionary to hold the data
            data = {
                "buy_price": price_1l_10l_1kg_buy.strip(),
                "sell_price": price_1l_10l_1kg_sell.strip(),
            }

            # Return the gold prices as JSON response
            return data
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve the webpage: {str(e)}")


@app.get("/btc-price")
async def get_btc_price():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{COINGECKO_API_URL}/simple/price?ids=bitcoin&vs_currencies=usd"
            )
            data = response.json()
            btc_price = data["bitcoin"]["usd"]
            return {"btc_price": btc_price}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to fetch BTC price from CoinCap API: {str(e)}"
        )
