from fastapi import FastAPI, HTTPException
import httpx
import requests
import models


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
    future_value = initial_investment * (1 + (0.07 * years))  # 7% annual growth rate for Bitcoin
    return {"future_value": future_value}


@app.get("/crypto-price")
async def get_crypto_assets():
    try:
        response = requests.get("api.coincap.io/v2/assets")
        response.raise_for_status()  # Raise an exception for any HTTP error status
        data = response.json()["data"]
        # Extract relevant information from the response data if needed
        return data
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch data from CoinCap API: {str(e)}")


@app.get("/btc-price")
async def get_btc_price():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{COINGECKO_API_URL}/simple/price?ids=bitcoin&vs_currencies=usd")
            data = response.json()
            btc_price = data["bitcoin"]["usd"]
            return {"btc_price": btc_price}
    except Exception as e:
        pass