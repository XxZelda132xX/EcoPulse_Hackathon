import math
import pandas as pd

plumes_csv = "datasets/plumes_aggregate.csv"
prior_csv  = "datasets/shedgum_prior_data.csv"

# if your prior file doesn't have sigma columns, this fallback relative sigma is used
DEFAULT_PRIOR_REL_SIGMA = 0.20  # 20%

def quad_sum(series):
    return math.sqrt((series**2).sum())

def getPlumeData():
    df = pd.read_csv(plumes_csv)
    # keep CO2 only
    df = df[df["gas"].str.upper() == "CO2"]

    # totals in t/h
    rate_tph  = df["emission_auto"].sum() / 1000.0
    sigma_tph = quad_sum(df["emission_uncertainty_auto"] / 1000.0)
    return rate_tph, sigma_tph

def getPriorData():
    df = pd.read_csv(prior_csv)

    # sum all asset rows to site total (expects 'prior_tph')
    rate_tph = df["prior_tph"].sum()

    # use sigma_prior_tph if present, else sigma_prior_rel * prior_tph row-wise
    if "sigma_prior_tph" in df.columns:
        sigma_tph = quad_sum(df["sigma_prior_tph"])
    else:
        rel = df["sigma_prior_rel"] if "sigma_prior_rel" in df.columns else DEFAULT_PRIOR_REL_SIGMA
        sigma_tph = quad_sum(df["prior_tph"] * rel)

    return rate_tph, sigma_tph

def blend(plumeData, priorData):
    E, sE = plumeData
    P, sP = priorData
    wE, wP = 1.0/(sE*sE), 1.0/(sP*sP)
    mu = (wE*E + wP*P) / (wE + wP)
    s  = math.sqrt(1.0 / (wE + wP))
    return mu, s

if __name__ == "__main__":
    plume_rate, plume_sigma = getPlumeData()
    prior_rate, prior_sigma = getPriorData()
    post_rate, post_sigma   = blend((plume_rate, plume_sigma), (prior_rate, prior_sigma))

    lo95 = post_rate - 1.96*post_sigma
    hi95 = post_rate + 1.96*post_sigma

    print(f"Plumes: {plume_rate:.2f} ± {plume_sigma:.2f} t/h")
    print(f"Prior : {prior_rate:.2f} ± {prior_sigma:.2f} t/h")
    print(f"Post  : {post_rate:.2f} ± {post_sigma:.2f} t/h  (95% [{lo95:.2f}, {hi95:.2f}])")
