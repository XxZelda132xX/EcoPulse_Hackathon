import math
import pandas as pd

plumes_csv = "datasets/plumes_aggregate.csv"
prior_csv  = "datasets/shedgum_prior_data.csv"

DEFAULT_PRIOR_REL_SIGMA = 0.20  # 20%

def quad_sum(series):
    return math.sqrt((series**2).sum())

def getPlumeData():
    df = pd.read_csv(plumes_csv)                   # plume,flow_rate,flow_uncertainty (kg/h)
    rate_tph  = df["flow_rate"].sum() / 1000.0    # → t/h
    sigma_tph = quad_sum(df["flow_uncertainty"]) / 1000.0
    return rate_tph, sigma_tph

def getPriorData():
    df = pd.read_csv(prior_csv)

    # use provided per-row relative sigma or default
    if "sigma_prior_rel" in df.columns:
        rel = pd.to_numeric(df["sigma_prior_rel"], errors="coerce").fillna(DEFAULT_PRIOR_REL_SIGMA)
    else:
        rel = pd.Series([DEFAULT_PRIOR_REL_SIGMA] * len(df))

    df["_sigma_tph"] = pd.to_numeric(df["prior_tph"], errors="coerce") * rel

    # bin to hour and aggregate per hour across assets
    df["time_utc"] = pd.to_datetime(df["time_utc"], utc=True, errors="coerce")
    df["time_hour"] = df["time_utc"].dt.floor("H")

    agg = df.groupby("time_hour").agg(
        site_rate_tph = ("prior_tph", "sum"),
        site_sigma_tph= ("_sigma_tph", lambda s: quad_sum(pd.to_numeric(s, errors="coerce")))
    ).reset_index()

    # pick a representative hour: the one closest to the median site total
    median_rate = agg["site_rate_tph"].median()
    idx = (agg["site_rate_tph"] - median_rate).abs().idxmax()
    rate_tph  = float(agg.loc[idx, "site_rate_tph"])
    sigma_tph = float(agg.loc[idx, "site_sigma_tph"])

    return rate_tph, sigma_tph

def blend(plumeData, priorData):
    E, sE = plumeData   # plumes (t/h)
    P, sP = priorData   # prior  (t/h)
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
    print(f"Prior : {prior_rate:.2f} ± {prior_sigma:.2f} t/h (representative hour)")
    print(f"Post  : {post_rate:.2f} ± {post_sigma:.2f} t/h  (95% [{lo95:.2f}, {hi95:.2f}])")
