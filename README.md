# Algorithmic-Options-Pricing-Fourier-Transform-

# 📈 Option Pricing Using Fast Fourier Transform (FFT)

An interactive quantitative finance application for pricing **European Call Options** using the **Carr-Madan Fast Fourier Transform (FFT)** approach under the **Variance Gamma (VG) model**. The project also compares FFT-based prices with the classical **Black-Scholes-Merton** analytical solution through an intuitive Streamlit dashboard.

---

## 📖 Overview

This project was developed as part of the **DMS613 – Introduction to Mathematical Finance** course under the guidance of **Prof. Sourav Majumdar**.

The objective is to demonstrate how option pricing can be transformed from the traditional time-domain formulation into the frequency domain, allowing an entire spectrum of strike prices to be computed efficiently using the **Fast Fourier Transform (FFT)** with computational complexity of **O(N log N)**.

Unlike the Black-Scholes model, the Variance Gamma framework captures **non-normal return distributions**, making it more suitable for modeling real financial markets.

---

## ✨ Features

- **Variance Gamma Pricing Model**
  - Prices European options under the Variance Gamma stochastic process.
  - Captures asymmetric returns and heavy-tailed distributions through skewness and kurtosis parameters.

- **Carr-Madan FFT Algorithm**
  - Implements the Carr-Madan Fourier pricing framework for rapid option valuation.
  - Simultaneously computes option prices across a large range of strike prices.

- **Exponential Damping**
  - Applies a damping parameter to ensure numerical stability and convergence of the Fourier transform.

- **Numerical Integration**
  - Uses Simpson's Rule to improve the accuracy of Fourier inversion.
  - Maintains the FFT grid consistency condition:
    \[
    \lambda \eta = \frac{2\pi}{N}
    \]

- **Black-Scholes Comparison**
  - Computes benchmark European option prices using the Black-Scholes analytical formula.
  - Enables direct comparison between the two pricing models.

- **Interactive Streamlit Dashboard**
  - Modify market conditions in real time.
  - Adjust Variance Gamma parameters.
  - Visualize pricing curves and pricing differences instantly.

---

# ⚙ Mathematical Framework

---

# 🧮 Mathematical Foundation

The pricing engine combines ideas from **stochastic calculus**, **risk-neutral valuation**, and **Fourier analysis** to efficiently compute European option prices. Rather than relying solely on the assumptions of the Black-Scholes framework, it employs the Variance Gamma process together with the Carr-Madan FFT algorithm to model realistic asset return dynamics.

## 1. Stochastic Calculus and Asset Price Dynamics

Financial asset prices are commonly represented using stochastic differential equations, where randomness is introduced through Brownian motion. Several mathematical concepts provide the theoretical basis for this formulation.

| Concept | Role in Option Pricing |
|---------|------------------------|
| **Brownian Motion** | Models the continuous random evolution of asset prices. |
| **Itô Integral** | Defines integration with respect to stochastic processes whose paths are nowhere differentiable. |
| **Itô's Lemma** | Extends the classical chain rule to stochastic processes and forms the basis of derivative pricing. |
| **Martingale Theory** | Under the risk-neutral measure, discounted asset prices evolve as martingales. |
| **Quadratic Variation** | Captures the accumulated variance of Brownian motion and is essential in stochastic calculus. |

These concepts establish the mathematical framework from which modern option pricing models are derived.

---

## 2. Black-Scholes-Merton Model

Using Itô's Lemma together with the principle of no-arbitrage, the Black-Scholes-Merton framework leads to the celebrated partial differential equation governing European option prices:

\[
\frac{\partial V}{\partial t}
+
\frac{1}{2}\sigma^2S^2
\frac{\partial^2V}{\partial S^2}
+
rS
\frac{\partial V}{\partial S}
-
rV
=
0
\]

Its analytical solution for a European call option is

\[
C
=
S_0N(d_1)
-
Ke^{-rT}N(d_2)
\]

where

\[
d_1=
\frac{\ln(S_0/K)+\left(r+\frac{\sigma^2}{2}\right)T}
{\sigma\sqrt{T}},
\qquad
d_2=d_1-\sigma\sqrt{T}.
\]

Although computationally efficient, this model assumes **constant volatility** and **log-normal returns**, making it unable to reproduce important market phenomena such as asymmetric returns and the volatility smile.

---

## 3. Variance Gamma Process

To overcome these limitations, the project adopts the **Variance Gamma (VG) process**, which models asset returns by evaluating Brownian motion over a random Gamma time clock.

Compared with the Black-Scholes model, the VG process naturally captures:

- **Skewness (\(\theta\))**, allowing asymmetric return distributions.
- **Kurtosis (\(\nu\))**, producing heavier tails than the normal distribution.
- More realistic pricing of deep in-the-money and out-of-the-money options.

The characteristic function of the Variance Gamma process is given by

\[
\phi_{VG}(u)
=
\left(
1
-
iu\theta\nu
+
\frac{\sigma^2\nu u^2}{2}
\right)^{-T/\nu}.
\]

Unlike the probability density function, this characteristic function has a simple closed-form representation, making it well suited for Fourier-based pricing techniques.

---

## 4. Carr-Madan Fourier Pricing Method

Instead of evaluating option prices directly from the probability density function, the Carr-Madan approach operates in the **frequency domain** using the characteristic function.

### Step 1 — Exponential Damping

Since the call payoff is not square-integrable, an exponential damping factor is introduced to stabilize the Fourier transform.

The transformed pricing function becomes

\[
\psi(v)
=
\frac{
e^{-rT}
\phi\!\left(v-(\alpha+1)i\right)
}{
\alpha^2+\alpha-v^2+i(2\alpha+1)v
}.
\]

Here, the parameter \(\alpha\) controls the damping and ensures numerical convergence.

---

### Step 2 — Numerical Approximation

The inverse Fourier transform is discretized using **Simpson's Rule**, replacing the continuous integral with a finite weighted summation over the frequency grid.

The resulting approximation is

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

This formulation substantially improves numerical accuracy before applying the FFT.

---

### Step 3 — Fast Fourier Transform

To exploit the computational efficiency of the FFT, the strike and frequency grids are selected such that

\[
\lambda\eta
=
\frac{2\pi}{N}.
\]

This relationship aligns the numerical summation with the structure of the Discrete Fourier Transform, allowing option prices for **thousands of strike prices** to be evaluated simultaneously with computational complexity

\[
O(N\log N),
\]

rather than computing each strike individually.

---

## Characteristic Function

Instead of working directly with the probability density function, the Variance Gamma model uses its characteristic function, which admits a closed-form expression and is well suited for Fourier-based pricing methods.

---

## Damped Fourier Transform

To satisfy square-integrability conditions required by the FFT, the call payoff is exponentially damped.

The modified Fourier transform is

\[
\psi(v)=
\frac{
e^{-rT}\phi\left(v-(\alpha+1)i\right)
}{
\alpha^2+\alpha-v^2+i(2\alpha+1)v
}
\]

where

- \(\phi(v)\) is the Variance Gamma characteristic function
- \(\alpha\) is the damping coefficient
- \(r\) is the risk-free rate
- \(T\) is the time to maturity

---

## FFT Discretization

The inverse Fourier integral is approximated numerically using Simpson's Rule before applying the Fast Fourier Transform.

The pricing grid satisfies

\[
\lambda \eta=\frac{2\pi}{N}
\]

where

- **N** → FFT grid size
- **η** → frequency spacing
- **λ** → log-strike spacing

This relationship guarantees compatibility with the discrete Fourier transform.

---

# 📊 Technology Stack

| Category | Tools |
|----------|------|
| Language | Python 3 |
| Numerical Computing | NumPy, SciPy |
| Data Processing | Pandas |
| Visualization | Streamlit |
| Fourier Transform | scipy.fft |
| Probability Functions | scipy.stats |

---

# 📁 Project Structure

```
Option-Pricing-FFT/
│
├── Pricing_Engine.py        # FFT pricing engine
├── README.md
├── requirements.txt
└── assets/
```

---

# 🚀 Installation

Clone the repository

```bash
git clone[https://github.com/ashityadav076-afk/Option-Pricing-Using-Fast-Fourier-Transform-FFT-]
```



# 📊 Dashboard Features

The interactive interface allows users to modify:

### Market Parameters

- Initial Stock Price
- Risk-Free Interest Rate
- Dividend Yield
- Time to Maturity

### Variance Gamma Parameters

- Volatility (σ)
- Skewness (θ)
- Kurtosis (ν)

### FFT Configuration

- Grid Size (N)
- Frequency Step (η)

The application automatically updates

- Option price curves
- Pricing comparison
- Absolute pricing error
- Equivalent Black-Scholes volatility

---

# 📈 Experimental Insights

The dashboard provides an intuitive understanding of how the Variance Gamma model differs from the Black-Scholes framework.

Some observations include:

- As **ν → 0** and **θ → 0**, the Variance Gamma model gradually approaches Black-Scholes behaviour.

- Increasing **ν** produces heavier tails, reflecting larger probabilities of extreme price movements.

- Negative **θ** introduces left-skewed return distributions, leading to noticeable deviations in option prices.

- The comparison plot highlights regions where the Black-Scholes assumption of constant volatility fails to capture observed market behaviour.

---

# 🎯 Learning Outcomes

This project demonstrates practical implementation of

- Fast Fourier Transform in computational finance
- Fourier-based option pricing
- Characteristic function methods
- Variance Gamma stochastic process
- Numerical integration using Simpson's Rule
- Black-Scholes option pricing
- Interactive financial visualization with Streamlit

---

# 👨‍💻 Author

**Ashit Yadav**

B.Tech, Civil Engineering  
Indian Institute of Technology Kanpur (IIT Kanpur)

---
