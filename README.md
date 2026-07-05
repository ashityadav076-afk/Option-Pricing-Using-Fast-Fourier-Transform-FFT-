# 📈 Algorithmic Option Pricing with Fast Fourier Transform

> An implementation of the **Carr-Madan Fast Fourier Transform (FFT)** framework for pricing European call options under the **Variance Gamma (VG)** stochastic process. The project benchmarks FFT-based prices against the analytical **Black-Scholes-Merton (BSM)** model while demonstrating how Fourier analysis significantly accelerates option valuation.

---

# 📖 Project Overview

Financial markets rarely satisfy the assumptions underlying the classical Black-Scholes model. Empirical asset returns often display **heavy tails**, **asymmetric distributions**, and the well-known **volatility smile**, leading to systematic pricing errors.

This project develops an FFT-based option pricing engine that addresses these limitations by combining:

- **Variance Gamma stochastic process** to model realistic asset dynamics
- **Carr-Madan Fourier pricing methodology** for efficient computation
- **Black-Scholes-Merton model** as a benchmark for comparison

Instead of pricing one option at a time, the FFT computes an entire spectrum of strike prices simultaneously with computational complexity

\[
O(N\log N),
\]

making it highly suitable for quantitative finance applications.

---

# 🎯 Objectives

The project focuses on two primary goals:

### Realistic Asset Modeling

Replace the constant-volatility assumption of Black-Scholes with the **Variance Gamma process**, allowing the model to capture:

- Skewed return distributions
- Heavy-tailed behaviour
- Jump-like market movements

### Efficient Numerical Pricing

Transform the pricing problem from the time domain into the frequency domain using Fourier transforms, enabling simultaneous valuation of thousands of European options.

---

# 🧮 Mathematical Background

## 1. Foundations of Stochastic Calculus

Modern derivative pricing is built upon stochastic processes that describe the evolution of financial assets.

The mathematical concepts used throughout the project include:

| Concept | Purpose |
|---------|---------|
| **Brownian Motion** | Models the random evolution of asset prices through continuous stochastic paths. |
| **Itô Integral** | Extends integration to stochastic processes with non-differentiable trajectories. |
| **Itô's Lemma** | Generalizes the chain rule for stochastic differential equations. |
| **Martingale Theory** | Forms the basis of pricing under the risk-neutral probability measure. |
| **Quadratic Variation** | Measures accumulated variance of Brownian motion and underpins stochastic calculus. |

These concepts collectively provide the theoretical foundation for modern option pricing models.

---

## 2. Black-Scholes-Merton Framework

Applying Itô's Lemma together with the no-arbitrage principle yields the Black-Scholes partial differential equation

\[
\frac{\partial V}{\partial t}
+
\frac12\sigma^2S^2
\frac{\partial^2V}{\partial S^2}
+
rS
\frac{\partial V}{\partial S}
-
rV
=
0.
\]

The corresponding European call option price is

\[
C=S_0N(d_1)-Ke^{-rT}N(d_2),
\]

where

\[
d_1=
\frac{\ln(S_0/K)+\left(r+\frac12\sigma^2\right)T}
{\sigma\sqrt T},
\qquad
d_2=d_1-\sigma\sqrt T.
\]

Although computationally efficient, the BSM framework assumes constant volatility and log-normal returns, preventing it from accurately reproducing market-observed volatility smiles.

---

## 3. Variance Gamma Process

To model financial markets more realistically, this project adopts the **Variance Gamma (VG)** process.

Instead of evolving on deterministic time, Brownian motion is evaluated on a random Gamma clock, producing distributions that naturally exhibit

- **Skewness** (\(\theta\))
- **Excess Kurtosis** (\(\nu\))
- Heavy-tailed returns
- Jump-like price behaviour

The characteristic function of the VG process is

\[
\phi_{VG}(u)=
\left(
1-iu\theta\nu
+\frac{\sigma^2\nu u^2}{2}
\right)^{-T/\nu}.
\]

Because the characteristic function is available in closed form, Fourier transform methods become computationally attractive.

---

## 4. Carr-Madan FFT Pricing

Instead of integrating the probability density function directly, pricing is performed using the characteristic function in Fourier space.

### Step 1 — Damped Fourier Transform

An exponential damping factor is introduced so that the option payoff satisfies square-integrability.

\[
\psi(v)=
\frac{
e^{-rT}
\phi(v-(\alpha+1)i)
}{
\alpha^2+\alpha-v^2+i(2\alpha+1)v
}.
\]

---

### Step 2 — Numerical Integration

The inverse transform is approximated numerically using **Simpson's Rule**, producing a weighted discrete summation

\[
C(k_u)
\approx
\frac{e^{-\alpha k_u}}{\pi}
\sum_{j=1}^{N}
e^{-i\frac{2\pi}{N}(j-1)(u-1)}
e^{ibv_j}
\psi(v_j)
\frac{\eta}{3}
\left[
3+(-1)^j-\delta_{j-1}
\right].
\]

---

### Step 3 — Fast Fourier Transform

To align the discrete approximation with the Discrete Fourier Transform, the computational grid satisfies

\[
\lambda\eta=\frac{2\pi}{N}.
\]

This enables the FFT algorithm to evaluate prices across an entire strike grid with computational complexity

\[
O(N\log N),
\]

instead of repeatedly evaluating individual integrals.

---

# ✨ Key Features

- Fast Fourier Transform implementation based on Carr-Madan methodology
- Variance Gamma stochastic process for realistic asset dynamics
- Black-Scholes analytical pricing benchmark
- Simpson's Rule numerical integration
- Interactive Streamlit dashboard
- Adjustable volatility, skewness, kurtosis, and maturity parameters
- Real-time comparison between VG and Black-Scholes pricing curves

---

# 📊 Black-Scholes vs Variance Gamma

| Feature | Black-Scholes | Variance Gamma |
|----------|--------------|----------------|
| Return Distribution | Log-normal | Skewed & Heavy-tailed |
| Volatility | Constant | Time-changed stochastic process |
| Jump Behaviour | Not captured | Naturally represented |
| Volatility Smile | Cannot explain | Captured implicitly |
| Pricing Method | Closed-form | FFT-based numerical pricing |
| Computational Cost | Constant | \(O(N\log N)\) for multiple strikes |

---

# 📐 Risk-Neutral Valuation

The project also explores the theory of risk-neutral pricing by studying:

- Equivalent martingale measures
- Discounted expected payoffs
- No-arbitrage pricing principles
- Sub-hedging and super-hedging arguments
- Relationship between Black-Scholes and modern stochastic pricing models

---

# 🛠 Technology Stack

| Category | Tools |
|-----------|-------|
| Programming Language | Python 3 |
| Scientific Computing | NumPy, SciPy |
| Data Processing | Pandas |
| Interactive Dashboard | Streamlit |
| Visualization | Matplotlib |
| Market Data | yfinance |
| Development | Jupyter Notebook |

---

# 📁 Repository Structure

```
.
├── Pricing_Engine.py
├── notebooks/
│   ├── bsm_derivation.ipynb
│   ├── variance_gamma.ipynb
│   └── fft_pricing.ipynb
├── results/
│   └── volatility_smile.png
├── requirements.txt
└── README.md
```

---

# 🚀 Installation

Clone the repository

```bash
git clone https://github.com/ashityadav076-afk
```

Navigate into the project

```bash
cd Algorithmic-Option-Pricing
```

Install the required libraries

```bash
pip install numpy scipy pandas matplotlib streamlit yfinance
```

---

# ▶ Running the Project

Run the pricing engine

```bash
python Pricing_Engine.py
```

Or launch the interactive dashboard

```bash
streamlit run Pricing_Engine.py
```

The dashboard is typically available at

```
http://localhost:8501
```

---

# 📊 Experimental Analysis

The dashboard enables users to investigate the impact of model parameters in real time.

Some notable observations include:

- As **θ → 0** and **ν → 0**, the Variance Gamma model converges toward Black-Scholes behaviour.
- Increasing **ν** introduces heavier tails and larger probabilities of extreme returns.
- Negative **θ** generates asymmetric pricing curves and emphasizes the volatility smile.
- The comparison illustrates pricing discrepancies where the constant-volatility assumption becomes inadequate.

---

# 📚 Topics Covered

Throughout the project, the following concepts are explored:

- Probability Theory
- Brownian Motion
- Itô Calculus
- Martingale Pricing
- Black-Scholes Derivation
- Risk-Neutral Valuation
- Variance Gamma Process
- Characteristic Functions
- Fourier Transform Methods
- Carr-Madan FFT Algorithm
- Numerical Integration
- Computational Finance

---

# 👨‍💻 Author

**Ashit Yadav**

B.Tech, Civil Engineering  
Indian Institute of Technology Kanpur (IIT Kanpur)

---

## ⭐ Acknowledgement

This project was developed as part of academic coursework in **Mathematical Finance**, focusing on the application of stochastic calculus and Fourier methods to computational option pricing.
