from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from black_scholes import black_scholes_price, calculate_greeks, calculate_payoff_curve

app = FastAPI(title = "Options Pricing API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class OptionRequest(BaseModel):
    stock_price: float = Field(..., gt = 0)
    strike_price: float = Field(..., gt = 0)
    time_to_expiry_days: int = Field(..., ge =1, le=1095)
    volatility: float = Field(..., gt=0, le=5)
    risk_free_rate: float = Field(..., ge = 0, le = 1)
    option_type: str

@app.post("/price")
def price_option(req: OptionRequest):
    T = req.time_to_expiry_days / 365

    if T <=0:
        raise HTTPException(status_code=400, detail="Time to expiry must be at least 1 day")

    price = black_scholes_price(req.stock_price, req.strike_price, T, req.risk_free_rate, req.volatility, req.option_type)

    greeks = calculate_greeks(req.stock_price, req.strike_price, T, req.risk_free_rate, req.volatility, req.option_type)

    payoff = calculate_payoff_curve(req.stock_price, req.strike_price, T, req.risk_free_rate, req.volatility, price, req.option_type)

    return {
        "price": price,
        "greeks": greeks,
        "payoff": payoff,
    }

@app.get("/health")
def health():
    return {
        "status": "ok"
    }
