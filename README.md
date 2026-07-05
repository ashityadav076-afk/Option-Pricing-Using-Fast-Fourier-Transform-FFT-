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
