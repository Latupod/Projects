# Portfolio Lab

Portfolio Lab is a laptop calculator for learning portfolio risk. You pick stocks and ETFs, and it shows the weight vector, the covariance matrix, and the portfolio variance

`variance = wᵀ Σ w`

in three steps, with a plain-English line under the result. It also compares a few named mixes. It does not tell you what to buy, and it does not connect to a broker.

Figures use historical prices and a sample covariance. They are a description of the chosen window, not a forecast and not financial advice.

## Run it

From this folder:

```text
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m portfolio_lab.synthetic
python app.py
```

Open http://127.0.0.1:5050

`python -m portfolio_lab.synthetic` rewrites the sample price files. They are already in `data/fixtures`, so you only need that command if you want to regenerate them. The app still calculates with the network off.

Two terminal views, if you want the numbers before the page:

```text
python -m portfolio_lab.demo
python -m portfolio_lab.report --market US --window 1y --tickers AAPL,MSFT,JNJ,BND
```

Tests:

```text
python -m pytest
```

## A walkthrough

1. Create a portfolio.
2. Press **Load the lesson mix**. On the US market that selects Apple, Microsoft, Johnson & Johnson, Exxon Mobil, an equity ETF, a bond ETF, and cash.
3. Press **Calculate**. Read the weight vector `w`, the covariance `Σ`, the column `Σ w`, and the line that dots them together.
4. Switch the strategy to **Cautious**, then **Balanced**, then **Growth**, and press Calculate again. Compare the allocation pie with the risk pie. Cash can have a large weight and a zero risk slice, because this model gives cash no variance.
5. Type an expected-return override on one holding and calculate Balanced again. The covariance table does not change. The Balanced weights can.
6. Press **Save**. Restart the app. The portfolio is still in the list. The file stores your choices, not a copy of the prices.

The UK market is the same tool in pounds, with the FTSE 100 as the chart benchmark. One portfolio is one currency. US and UK prices are not mixed, because that would need an exchange rate.

**Add a live ticker** needs the network. It caches Yahoo Finance history under `data/cache` in the same CSV shape as the sample files. If the download fails, the sample files are untouched. London prices labelled in pence are converted to pounds when the level looks like pence (a median of 100 or more). A series that is already in pounds is left as it is, and the page says so.

## What the screen is doing

Simple daily returns, not log returns: today's price divided by yesterday's price, minus one. Weights apply to simple returns.

Annualisation multiplies the average daily return by 252, and multiplies every entry of the daily covariance by 252. The page says this so the 252 is not hidden. Covariance is the sample estimate, divided by the number of days minus one.

Component risk, used for the risk pie, is

`component_i = w_i × (Σ w)_i / volatility`

Those pieces add up to portfolio volatility. Weight times a holding's own volatility does not, so it is not used. If a piece is negative, that holding is hedging the rest and the chart switches to bars, because a pie cannot show a negative slice.

Sharpe is `(return − risk-free rate) / volatility`. It is undefined when volatility is zero. Historical Sharpe replays the window. Objective Sharpe uses the expected returns the optimiser saw, including any overrides you typed.

Drawdown, and the best and worst month, use a constant-mix path: the same weights applied every day, as if the mix were put back to those weights each day. That is not a backtest. There are no trading costs and no rebalance calendar.

Strategies, all long-only, weights sum to 100%, no holding above the cap you set:

- **Your weights** — scored as typed, and scaled to 100% only when they do not already sum to 100%.
- **Equal weight** — the same weight in each selected holding. A locked cash weight stays put. A blank lock lets cash join the split. Your weights treats a blank cash weight as 0%.
- **Cautious** — minimum variance. Cash is allowed to take a large share. That is the lesson.
- **Balanced** — maximum Sharpe, using historical average returns unless you override them.
- **Growth** — maximum Sharpe with cash capped at 10% as well. Without cash, Growth matches Balanced.

The frontier is the lowest-volatility mix at each expected return, under the same cap. Growth can sit inside that curve because of the extra cash limit.

Dividend yield is shown only when the file or the download has it. AstraZeneca in the UK sample has none, so the cell says Unavailable. Yield is not added into the return. Historical returns are price changes only.

The sample prices are synthetic. They are generated from a fixed seed so the app works offline and the repository does not ship a scraped price database. Do not read a sample return as a real company's return.

## The hand-worked check

`python -m portfolio_lab.demo` prints this example. The tests lock the same figures. The daily moves are large on purpose: annualising four noisy days makes the average returns look enormous. That is the formula doing what it was told, and it is why a short window is a poor forecast.

Daily simple returns, columns A, B, and C:

```text
 0.02   0.01  -0.01
 0.01  -0.02   0.02
-0.01   0.02   0.01
 0.02   0.01   0.00
```

Average daily return: `0.01`, `0.005`, `0.005`.
Times 252: `2.52`, `1.26`, `1.26`.

Deviations of A from its average: `0.01, 0, -0.02, 0.01`.
Deviations of B: `0.005, -0.025, 0.015, 0.005`.
Products: `0.00005 + 0 + -0.0003 + 0.00005 = -0.0002`.
Divide by `n − 1 = 3`, then multiply by 252: covariance of A and B is `-0.0168`.

Annualised covariance, weights `0.50`, `0.30`, `0.20`:

```text
        A         B         C
A   0.0504   -0.0168   -0.0252
B  -0.0168    0.0756   -0.0336
C  -0.0252   -0.0336    0.0420
```

`Σ w` is `0.01512`, `0.00756`, `-0.01428`.
Dot with the weights: variance `0.006972`, volatility `0.083499` (about 8.35% a year).
Component risk: `0.090541`, `0.027162`, `-0.034204`. C is a hedge, so its piece is negative, and the three pieces still add up to the volatility.

A on its own has variance `0.0504`, so volatility about 22%. The mix is much calmer because the holdings do not all move together. That gap is the reason to look at the covariance instead of averaging the three volatilities.

## Layout

```text
app.py                     Flask pages and JSON
portfolio_lab/returns.py   simple returns, annualise by 252
portfolio_lab/risk.py      covariance, wᵀ Σ w, component risk
portfolio_lab/stats.py     Sharpe, drawdown, best and worst month
portfolio_lab/optimize.py  equal weight, minimum variance, maximum Sharpe, frontier
portfolio_lab/data.py      sample files, cache, pence conversion
portfolio_lab/live.py      optional Yahoo Finance download
portfolio_lab/store.py     named portfolios as JSON
portfolio_lab/analysis.py  one request in, one teaching payload out
data/fixtures/             synthetic sample prices, safe to commit
data/cache/                live downloads, not committed
data/portfolios/           your saved portfolios, not committed
```

Charts use Chart.js 4.4.6, stored at `static/js/chart.umd.min.js` so the page can draw them without the network. The correlation heatmap is an HTML table, so you can read the same matrix the calculation used. Colours follow the budget tracker's palette: green `#1a5f4a` on a light background. This app does not share data with the budget tracker.

Saved JSON keeps the name, market, window, risk-free rate, cap, cash yield, tickers, weights, strategy, and expected-return overrides.

## Limits

- Historical average return is a weak forecast. Maximum Sharpe will lean on whatever means you give it, including a number you typed.
- A covariance estimated from a short window, or from many holdings, is noisy. The page warns when the window is short relative to the number of risky holdings.
- Constant-mix drawdowns pretend you rebalanced every day for free.
- Sample prices are not market prices. Live prices are split-adjusted closes from Yahoo Finance and can be delayed, missing, or rate-limited. They may also fold dividends into the adjusted price. The dividend line is separate and can be missing.
- Cash is synthetic. You type the yield. Its variance and covariances are zero. It is not a savings account and not a bond.
- There is no short selling, no leverage, no tax, and no brokerage connection.
- US and UK holdings are not combined in one portfolio.

## Later, if you want to change direction

Beta against the benchmark, a monthly rebalance with a trading cost, mixing US and UK through an exchange rate, a simple Value at Risk, a phone layout, or an account system. Local JSON does not block accounts, but accounts are a different project.
