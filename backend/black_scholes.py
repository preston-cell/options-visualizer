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
