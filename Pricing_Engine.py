import streamlit as st
import numpy as np
import pandas as pd
from scipy.fft import fft
from scipy.stats import norm

# ==========================================================================
# Variance Gamma Option Pricing using FFT
# ==========================================================================

# Computes the characteristic function of the Variance Gamma process
# used in Fourier-based option valuation.
def vg_characteristic_function(u, S0, r, q, T, sigma, nu, theta):
    omega = (1.0 / nu) * np.log(1.0 - theta * nu - 0.5 * sigma**2 * nu)
    drift = np.log(S0) + (r - q + omega) * T

    phi = np.exp(1j * u * drift) * (
        1.0 - 1j * theta * nu * u + 0.5 * sigma**2 * nu * u**2
    ) ** (-T / nu)

    return phi


# Creates the strike-price and frequency grids required for FFT evaluation.
def setup_numerical_grids(S0, N, eta):
    delta_k = (2 * np.pi) / (N * eta)

    indices = np.arange(N)
    frequencies = indices * eta

    lower_limit = np.log(S0) - (N * delta_k) / 2
    log_strikes = lower_limit + indices * delta_k

    strikes = np.exp(log_strikes)

    return strikes, frequencies, lower_limit


# Forms the Carr-Madan damped transform that guarantees convergence
# of the Fourier integral.
def build_fourier_integrand(v, S0, r, q, T, sigma, nu, theta, alpha):
    shifted_frequency = v - (alpha + 1) * 1j

    characteristic_fn = vg_characteristic_function(
        shifted_frequency, S0, r, q, T, sigma, nu, theta
    )

    denominator = (
        (alpha**2 + alpha - v**2)
        + 1j * (2 * alpha + 1) * v
    )

    psi = np.exp(-r * T) * characteristic_fn / denominator

    return psi


# Executes the Fast Fourier Transform after applying Simpson weights.
def execute_fft_transformation(psi, frequencies, lower_limit, eta, N):

    weights = np.ones(N)
    weights[0] = 1 / 3
    weights[1::2] = 4 / 3
    weights[2::2] = 2 / 3
    weights[-1] = 1 / 3

    fft_input = (
        np.exp(-1j * lower_limit * frequencies)
        * psi
        * eta
        * weights
    )

    transformed = np.real(fft(fft_input))

    return transformed


# Removes the exponential damping and converts OTM put prices
# into call prices through put-call parity.
def finalize_option_prices(
    fft_output,
    strikes,
    S0,
    r,
    q,
    T,
    alpha,
):

    option_prices = np.zeros(len(fft_output))

    log_strikes = np.log(strikes)

    raw_prices = (
        np.exp(-alpha * log_strikes)
        / np.pi
    ) * fft_output

    for i, strike in enumerate(strikes):

        if strike >= S0:
            option_prices[i] = raw_prices[i]

        else:
            put_price = raw_prices[i]

            call_price = (
                put_price
                + S0 * np.exp(-q * T)
                - strike * np.exp(-r * T)
            )

            intrinsic = (
                S0 * np.exp(-q * T)
                - strike * np.exp(-r * T)
            )

            option_prices[i] = max(call_price, intrinsic)

    return option_prices


# Complete pricing workflow from parameter input
# to FFT-generated call prices.
def complete_fft_pricing_engine(
    S0,
    r,
    q,
    T,
    sigma,
    nu,
    theta,
    alpha=1.5,
    N=4096,
    eta=0.25,
):

    strikes, frequencies, lower_limit = setup_numerical_grids(
        S0,
        N,
        eta,
    )

    psi = build_fourier_integrand(
        frequencies,
        S0,
        r,
        q,
        T,
        sigma,
        nu,
        theta,
        alpha,
    )

    fft_values = execute_fft_transformation(
        psi,
        frequencies,
        lower_limit,
        eta,
        N,
    )

    call_prices = finalize_option_prices(
        fft_values,
        strikes,
        S0,
        r,
        q,
        T,
        alpha,
    )

    return strikes, call_prices


# ==========================================================================
# Black-Scholes Benchmark Model
# ==========================================================================

# Returns the analytical European call option value
# under the Black-Scholes framework.
def black_scholes_call(
    S0,
    K,
    r,
    q,
    T,
    sigma_bs,
):

    if T <= 0 or sigma_bs <= 0:
        return np.maximum(
            S0 * np.exp(-q * T)
            - K * np.exp(-r * T),
            0,
        )

    d1 = (
        np.log(S0 / K)
        + (r - q + 0.5 * sigma_bs**2) * T
    ) / (sigma_bs * np.sqrt(T))

    d2 = d1 - sigma_bs * np.sqrt(T)

    return (
        S0 * np.exp(-q * T) * norm.cdf(d1)
        - K * np.exp(-r * T) * norm.cdf(d2)
    )


# ==========================================================================
# Streamlit User Interface
# ==========================================================================

st.set_page_config(
    page_title="VG FFT vs Black-Scholes",
    layout="wide",
)

st.title("Variance Gamma FFT Pricing Compared with Black-Scholes")

st.write(
    "Interactive visualization of European call prices "
    "generated using the Variance Gamma model and the "
    "classical Black-Scholes framework."
)

left_panel, right_panel = st.columns([1, 2])

with left_panel:

    st.header("Model Parameters")

    st.subheader("Market Inputs")

    S0 = st.number_input(
        "Initial Asset Price",
        value=100.0,
        min_value=1.0,
    )

    T = st.slider(
        "Time to Expiry",
        0.05,
        3.0,
        0.5,
        0.05,
    )

    r = st.slider(
        "Risk-Free Interest Rate",
        0.0,
        0.15,
        0.05,
        0.01,
    )

    q = st.slider(
        "Dividend Yield",
        0.0,
        0.10,
        0.00,
        0.01,
    )

    st.subheader("Variance Gamma Parameters")

    sigma = st.slider(
        "Volatility",
        0.05,
        0.60,
        0.20,
        0.01,
    )

    nu = st.slider(
        "Tail Thickness",
        0.01,
        0.80,
        0.25,
        0.01,
    )

    theta = st.slider(
        "Return Skewness",
        -0.60,
        0.00,
        -0.15,
        0.01,
    )

    st.subheader("FFT Configuration")

    N = st.selectbox(
        "Grid Size",
        [2048, 4096, 8192],
        index=1,
    )

    eta = st.slider(
        "Frequency Increment",
        0.05,
        0.50,
        0.25,
        0.05,
    )


# ==========================================================================
# Pricing Computation
# ==========================================================================

strikes, vg_prices = complete_fft_pricing_engine(
    S0,
    r,
    q,
    T,
    sigma,
    nu,
    theta,
    alpha=1.5,
    N=N,
    eta=eta,
)

bs_sigma = np.sqrt(sigma**2 + theta**2 * nu)

bs_prices = np.array([
    black_scholes_call(
        S0,
        strike,
        r,
        q,
        T,
        bs_sigma,
    )
    for strike in strikes
])

results = pd.DataFrame({
    "Strike": strikes,
    "VG FFT Price": vg_prices,
    "Black-Scholes Price": bs_prices,
    "Absolute Error": np.abs(vg_prices - bs_prices),
})

results = results[
    (results["Strike"] >= 0.7 * S0)
    &
    (results["Strike"] <= 1.3 * S0)
]


# ==========================================================================
# Display Results
# ==========================================================================

with right_panel:

    st.header("Pricing Results")

    metric1, metric2 = st.columns(2)

    metric1.metric(
        "Equivalent BS Volatility",
        f"{bs_sigma*100:.2f}%",
    )

    metric2.metric(
        "Maximum Difference",
        f"${results['Absolute Error'].max():.2f}",
    )

    st.divider()

    st.subheader("Option Price Comparison")

    st.line_chart(
        data=results,
        x="Strike",
        y=[
            "VG FFT Price",
            "Black-Scholes Price",
        ],
    )

    st.subheader("Numerical Results")

    st.dataframe(
        results.style.format({
            "Strike": "{:.2f}",
            "VG FFT Price": "${:.2f}",
            "Black-Scholes Price": "${:.2f}",
            "Absolute Error": "${:.2f}",
        }),
        use_container_width=True,
        height=250,
    )
