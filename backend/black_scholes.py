import math
from scipy.stats import norm

def calculate_d1_d2(S, K, T, r, sigma):
    """
    d1:
    ln(S/K) will output a positive value if the stock price is
    greater than the strike price. this positive z score, after
    being plugged into the normal distribution, will indicate a
    high probability. this is because if the stock price is higher
    than the strike price we are already in the money, and the price
    of the call option should be higher. the second numerator term accounts for the upward drift of
    the stock. Given enough time and volatility of the stock,
    it might get into money eventually. N(d2) is the probability
    the stock ends up above K

    d2:
    N(d2) needs to capture the probability weighted by how much
    the stock tends to the upside, so it needs to follow the log
    normal distribution so need to account for the skew
    """
    d1 = (math.log(S/K) + (r + 0.5* sigma ** 2) * T) / (sigma * math.sqrt(T))

    d2 = d1 - sigma * math.sqrt(T)

    return d1, d2

def black_scholes_price(S,K,T,r,sigma,option_type="call"):
    """
    The black scholes price for a call/put option.
    Essentially the expected value of owning the stock given that
    it expired in money, minus the expected cost of paying the
    strike price discounted to present day. Vice versa for a put
    """
    d1, d2 = calculate_d1_d2(S, K, T, r, sigma)

    if option_type == "call":
        price = S * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)

    elif option_type == "put":
        price = K * math.exp(-r * T) *  norm.cdf(-d2) - S * norm.cdf(-d1)

    return round(price, 4)


def calculate_greeks(S, K, T, r, sigma, option_type="call"):
    d1, d2 = calculate_d1_d2(S, K, T, r, sigma)

    gamma = norm.pdf(d1) / (S * sigma * math.sqrt(T))
    vega = S * norm.pdf(d1) * math.sqrt(T) / 100

    if option_type == "call":
        delta = norm.cdf(d1)
        theta = (-(S * norm.pdf(d1) * sigma) / (2 * math.sqrt(T))
                 - r * K * math.exp(-r * T) * norm.cdf(d2)) / 365
        rho = K * T * math.exp(-r * T) * norm.cdf(d2) / 100

    elif option_type == "put":
        delta = norm.cdf(d1) - 1
        theta = (-(S * norm.pdf(d1) * sigma) / (2 * math.sqrt(T))
                 + r * K * math.exp(-r * T) * norm.cdf(-d2)) / 365
        rho = -K * T * math.exp(-r * T) * norm.cdf(-d2) / 100

    # delta is a number 0-1 indicating how much the price of
    # the option will change given a 1$ increase in the stock price

    # gamma is the rate of change of delta

    # vega is an indication of how much the option
    # gains or loses given an increase in 1% of volatility

    #rho is how much the discounted cost changes
    # given an increase of interest rates by 1%
    return {
        "delta": round(delta, 4),
        "gamma": round(gamma, 4),
        "theta": round(theta, 4),
        "vega":  round(vega, 4),
        "rho":   round(rho, 4),
    }

def calculate_payoff_curve(S, K, T, r, sigma, premium, option_type="call", num_points=200):
    low  = S * 0.5
    high = S * 1.5
    step = (high - low) / num_points

    curve = []
    price = low
    while price <= high:
        if option_type == "call":
            expiration_pnl = max(price - K, 0) - premium
        else:
            expiration_pnl = max(K - price, 0) - premium

        current_value = black_scholes_price(price, K, T, r, sigma, option_type)

        curve.append({
            "stock_price": round(price, 2),
            "pnl": round(expiration_pnl, 4),
            "current_value": round(current_value, 4)
        })
        price += step

    return curve


if __name__ == "__main__":
    S     = 100
    K     = 105
    T     = 30 / 365
    r     = 0.05
    sigma = 0.20

    price  = black_scholes_price(S, K, T, r, sigma, "call")
    greeks = calculate_greeks(S, K, T, r, sigma, "call")
    payoff = calculate_payoff_curve(S, K, price)

    print(f"Price  : ${price}")
    print(f"Greeks : {greeks}")
    print(f"Payoff points: {len(payoff)}, first: {payoff[0]}, last: {payoff[-1]}")
