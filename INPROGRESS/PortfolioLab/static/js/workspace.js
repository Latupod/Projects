/* Portfolio workspace. Chart.js is loaded before this file. */
const PortfolioWorkspace = (() => {
  const LESSONS = {
    US: ["AAPL", "MSFT", "JNJ", "XOM", "SPY", "BND"],
    UK: ["SHEL.L", "AZN.L", "HSBA.L", "ULVR.L", "ISF.L", "IGLT.L"],
  };
  const STRATEGY_HINTS = {
    user: "Scores the weights you type. They are scaled to 100% only if they do not already add up.",
    equal: "Gives every selected holding the same weight. A locked cash weight stays fixed and the rest is split.",
    min_variance: "Lowest portfolio volatility under the cap. Cash can take a large share. That is the point of Cautious.",
    max_sharpe: "Highest excess return per unit of volatility, using historical averages unless you override an expected return.",
    growth: "Same goal as Balanced, but cash is capped at 10%. Without cash, Growth matches Balanced.",
  };
  const PALETTE = ["#1a5f4a", "#0f766e", "#b45309", "#3d6b8c", "#6b4c7a", "#1c2421", "#8a6a2f", "#b42318"];
  const charts = {};
  let portfolioId = "";
  let assets = [];
  let previousMarket = "US";

  function start(id) {
    portfolioId = id;
    Chart.defaults.font.family = 'system-ui, "Segoe UI", sans-serif';
    Chart.defaults.color = "#5c6b64";
    document.getElementById("calculate").addEventListener("click", () => calculate());
    document.getElementById("save").addEventListener("click", save);
    document.getElementById("delete").addEventListener("click", remove);
    document.getElementById("lesson").addEventListener("click", applyLesson);
    document.getElementById("live-form").addEventListener("submit", fetchLive);
    document.getElementById("market").addEventListener("change", changeMarket);
    document.getElementById("include-cash").addEventListener("change", () => {
      renderWeightRows();
      updateWeightSum();
    });
    document.getElementById("cash-weight").addEventListener("input", () => {
      document.getElementById("cash-weight").dataset.exact = "";
      updateWeightSum();
    });
    document.querySelectorAll('input[name="strategy"]').forEach((input) => {
      input.addEventListener("change", showStrategyHint);
    });
    showStrategyHint();
    load().catch((error) => showError(error.message));
  }

  async function load() {
    const portfolio = await readJson(await fetch(`/api/portfolio/${portfolioId}`));
    fillForm(portfolio);
    previousMarket = portfolio.market;
    await loadUniverse(portfolio.market, portfolio.tickers || []);
    renderWeightRows(portfolio.weights || {}, portfolio.expected_return_overrides || {}, portfolio.cash_weight);
    updateWeightSum();
    if ((portfolio.tickers || []).length) {
      await calculate();
    }
  }

  function fillForm(portfolio) {
    document.getElementById("name").value = portfolio.name || "New portfolio";
    document.getElementById("market").value = portfolio.market || "US";
    document.getElementById("window").value = portfolio.window || "3y";
    document.getElementById("rf").value = percentNumber(portfolio.risk_free_rate ?? 0.04);
    document.getElementById("cap").value = percentNumber(portfolio.max_weight ?? 0.4);
    document.getElementById("include-cash").checked = Boolean(portfolio.include_cash);
    document.getElementById("cash-yield").value = percentNumber(portfolio.cash_yield ?? 0.04);
    const cash = document.getElementById("cash-weight");
    if (portfolio.cash_weight === null || portfolio.cash_weight === undefined) {
      cash.value = "";
      cash.dataset.exact = "";
    } else {
      setExact(cash, portfolio.cash_weight);
    }
    const strategy = document.querySelector(`input[name="strategy"][value="${portfolio.strategy || "user"}"]`);
    if (strategy) strategy.checked = true;
    showStrategyHint();
  }

  async function loadUniverse(market, selected) {
    const universe = await readJson(await fetch(`/api/universe/${market}`));
    assets = universe.assets;
    const list = document.getElementById("ticker-list");
    list.replaceChildren();
    assets.forEach((asset) => {
      const item = document.createElement("li");
      const label = document.createElement("label");
      const box = document.createElement("input");
      box.type = "checkbox";
      box.value = asset.ticker;
      box.checked = selected.includes(asset.ticker);
      box.addEventListener("change", () => {
        renderWeightRows(currentWeights(), currentOverrides(), currentCashWeight());
        updateWeightSum();
      });
      label.append(box, document.createTextNode(`${asset.ticker} · ${asset.name}`));
      item.append(label);
      list.append(item);
    });
    document.getElementById("universe-note").textContent =
      `${universe.currency_label}. Benchmark for the chart: ${universe.benchmark.name}. Sample prices are synthetic. A fetched ticker is cached on this computer.`;
  }

  async function changeMarket() {
    const select = document.getElementById("market");
    const selected = selectedTickers();
    if (selected.length && !confirm("Changing market clears the selected holdings.")) {
      select.value = previousMarket;
      return;
    }
    previousMarket = select.value;
    await loadUniverse(select.value, []);
    renderWeightRows();
    updateWeightSum();
    document.getElementById("results-body").hidden = true;
    document.getElementById("results-hint").hidden = false;
  }

  function applyLesson() {
    const market = document.getElementById("market").value;
    const tickers = LESSONS[market];
    document.getElementById("window").value = "3y";
    document.getElementById("rf").value = "4";
    document.getElementById("cap").value = "40";
    document.getElementById("include-cash").checked = true;
    document.getElementById("cash-yield").value = "4";
    document.getElementById("cash-weight").value = "";
    document.querySelector('input[name="strategy"][value="user"]').checked = true;
    showStrategyHint();
    document.querySelectorAll("#ticker-list input").forEach((box) => {
      box.checked = tickers.includes(box.value);
    });
    const chosen = selectedTickers();
    const count = chosen.length + 1;
    const share = 1 / count;
    const weights = {};
    chosen.forEach((ticker) => {
      weights[ticker] = share;
    });
    renderWeightRows(weights, {}, share);
    updateWeightSum();
    setStatus("Lesson mix loaded. Press Calculate.");
  }

  async function fetchLive(event) {
    event.preventDefault();
    const symbol = document.getElementById("live-symbol").value.trim();
    const note = document.getElementById("live-note");
    note.textContent = "Fetching prices…";
    try {
      const body = await readJson(await fetch("/api/live", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ market: document.getElementById("market").value, symbol }),
      }));
      note.textContent = body.asset.note || `Cached ${body.asset.ticker}.`;
      const selected = selectedTickers();
      if (!selected.includes(body.asset.ticker)) selected.push(body.asset.ticker);
      await loadUniverse(document.getElementById("market").value, selected);
      renderWeightRows(currentWeights(), currentOverrides(), currentCashWeight());
    } catch (error) {
      note.textContent = error.message;
    }
  }

  function renderWeightRows(weights = {}, overrides = {}, cashWeight = null) {
    const body = document.querySelector("#weight-table tbody");
    body.replaceChildren();
    selectedTickers().forEach((ticker) => {
      body.append(weightRow(ticker, labelFor(ticker), weights[ticker], overrides[ticker]));
    });
    if (document.getElementById("include-cash").checked) {
      const cash = document.getElementById("cash-weight");
      const value = cashWeight === null || cashWeight === undefined || cashWeight === ""
        ? (cash.dataset.exact ? Number(cash.dataset.exact) : null)
        : cashWeight;
      body.append(weightRow("CASH", "Cash", value, null, true));
    }
  }

  function weightRow(ticker, label, weight, override, isCash) {
    const row = document.createElement("tr");
    row.dataset.ticker = ticker;
    const name = document.createElement("td");
    name.textContent = label;
    const weightCell = document.createElement("td");
    const weightInput = document.createElement("input");
    weightInput.type = "number";
    weightInput.step = "0.01";
    weightInput.min = "0";
    weightInput.dataset.role = "weight";
    if (weight !== null && weight !== undefined && weight !== "") {
      setExact(weightInput, Number(weight));
    }
    weightInput.addEventListener("input", () => {
      weightInput.dataset.exact = "";
      if (isCash) {
        const cash = document.getElementById("cash-weight");
        cash.value = weightInput.value;
        cash.dataset.exact = "";
      }
      updateWeightSum();
    });
    weightCell.append(weightInput);
    const historical = document.createElement("td");
    historical.dataset.role = "historical";
    historical.textContent = "—";
    const overrideCell = document.createElement("td");
    if (isCash) {
      overrideCell.textContent = "Uses cash yield";
    } else {
      const overrideInput = document.createElement("input");
      overrideInput.type = "number";
      overrideInput.step = "0.1";
      overrideInput.dataset.role = "override";
      overrideInput.placeholder = "Historical";
      if (override !== null && override !== undefined && override !== "") {
        overrideInput.value = percentNumber(override);
      }
      overrideCell.append(overrideInput);
    }
    row.append(name, weightCell, historical, overrideCell);
    return row;
  }

  function selectedTickers() {
    return [...document.querySelectorAll("#ticker-list input:checked")].map((box) => box.value);
  }

  function labelFor(ticker) {
    const asset = assets.find((item) => item.ticker === ticker);
    return asset ? `${ticker}` : ticker;
  }

  function currentWeights() {
    const weights = {};
    document.querySelectorAll("#weight-table tbody tr").forEach((row) => {
      if (row.dataset.ticker === "CASH") return;
      const input = row.querySelector('[data-role="weight"]');
      const value = numberFrom(input);
      if (value !== null) weights[row.dataset.ticker] = value;
    });
    return weights;
  }

  function currentOverrides() {
    const overrides = {};
    document.querySelectorAll("#weight-table tbody tr").forEach((row) => {
      const input = row.querySelector('[data-role="override"]');
      if (!input || input.value === "") return;
      overrides[row.dataset.ticker] = Number(input.value) / 100;
    });
    return overrides;
  }

  function lockCashWeight() {
    if (!document.getElementById("include-cash").checked) return null;
    const input = document.getElementById("cash-weight");
    if (input.value === "") return null;
    return numberFrom(input);
  }

  function userCashWeight() {
    if (!document.getElementById("include-cash").checked) return null;
    const input = document.querySelector('#weight-table tr[data-ticker="CASH"] [data-role="weight"]');
    if (!input || input.value === "") return null;
    return numberFrom(input);
  }

  function currentCashWeight() {
    return lockCashWeight();
  }

  function spec() {
    const weights = {};
    document.querySelectorAll("#weight-table tbody tr").forEach((row) => {
      if (row.dataset.ticker === "CASH") return;
      const input = row.querySelector('[data-role="weight"]');
      weights[row.dataset.ticker] = numberFrom(input) || 0;
    });
    return {
      name: document.getElementById("name").value.trim() || "New portfolio",
      market: document.getElementById("market").value,
      window: document.getElementById("window").value,
      risk_free_rate: Number(document.getElementById("rf").value) / 100,
      max_weight: Number(document.getElementById("cap").value) / 100,
      include_cash: document.getElementById("include-cash").checked,
      cash_yield: Number(document.getElementById("cash-yield").value) / 100,
      cash_weight: document.querySelector('input[name="strategy"]:checked').value === "user"
        ? userCashWeight()
        : lockCashWeight(),
      tickers: selectedTickers(),
      weights,
      strategy: document.querySelector('input[name="strategy"]:checked').value,
      expected_return_overrides: currentOverrides(),
    };
  }

  async function calculate() {
    showError("");
    setStatus("");
    const button = document.getElementById("calculate");
    button.disabled = true;
    document.getElementById("results-hint").hidden = false;
    document.getElementById("results-hint").textContent = "Calculating the covariance, the strategies, and the frontier…";
    try {
      const response = await fetch("/api/analyse", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(spec()),
      });
      const body = await response.json();
      if (!response.ok) throw new Error(body.error || "Calculation failed.");
      renderComparison(body.comparison || []);
      if (!body.ok) {
        document.getElementById("results-body").hidden = false;
        document.getElementById("results-hint").hidden = true;
        showError(body.error || "This strategy is not possible under the cap.");
        return;
      }
      applySolvedWeights(body);
      renderResult(body);
    } catch (error) {
      showError(error.message);
      if (document.getElementById("results-body").hidden) {
        document.getElementById("results-hint").textContent =
          "Choose holdings and press Calculate. The weight vector, covariance matrix, and charts appear here.";
      }
    } finally {
      button.disabled = false;
    }
  }

  function applySolvedWeights(body) {
    const active = (body.comparison || []).find((row) => row.key === bodyActive(body) && row.ok);
    if (!active) return;
    const byTicker = Object.fromEntries(active.weights.map((item) => [item.ticker, item.weight]));
    document.querySelectorAll("#weight-table tbody tr").forEach((row) => {
      const input = row.querySelector('[data-role="weight"]');
      if (byTicker[row.dataset.ticker] === undefined) return;
      setExact(input, byTicker[row.dataset.ticker]);
    });
    body.assets.forEach((asset) => {
      const row = document.querySelector(`#weight-table tr[data-ticker="${cssEscape(asset.ticker)}"]`);
      if (!row) return;
      row.querySelector('[data-role="historical"]').textContent = pct(asset.historical_return);
    });
    updateWeightSum();
  }

  function bodyActive(body) {
    return document.querySelector('input[name="strategy"]:checked').value;
  }

  function renderResult(body) {
    document.getElementById("results-hint").hidden = true;
    document.getElementById("results-body").hidden = false;
    const warning = document.getElementById("warning-banner");
    warning.hidden = !body.warning;
    warning.textContent = body.warning || "";
    const windowNote = document.getElementById("window-note");
    windowNote.hidden = !body.window_note;
    windowNote.textContent = body.window_note || "";
    document.getElementById("annualization-note").textContent = body.annualization_note;
    document.getElementById("dividend-note").textContent = body.dividend_note;
    renderSummary(body.portfolio);
    renderCaptions(body.captions);
    renderVector("weight-vector", body.math.tickers, body.math.weights, "Weight");
    renderVector("sigma-w", body.math.tickers, body.math.sigma_w, "Σ w");
    renderMatrix("covariance", body.math.tickers, body.math.covariance, (value) => num(value));
    document.getElementById("equation").textContent = equation(body.math);
    document.getElementById("variance-caption").textContent = body.captions.variance;
    document.getElementById("allocation-caption").textContent = body.captions.allocation;
    document.getElementById("risk-caption").textContent = [body.captions.risk, body.captions.cash_risk].filter(Boolean).join(" ");
    document.getElementById("drawdown-caption").textContent = body.captions.drawdown;
    document.getElementById("frontier-caption").textContent = body.captions.frontier;
    renderHeatmap(body.math.tickers, body.math.correlation);
    renderAssets(body.assets);
    renderCharts(body);
  }

  function renderSummary(stats) {
    const cards = [
      ["Expected return", pct(stats.expected_return)],
      ["Historical return", pct(stats.historical_return)],
      ["Volatility", pct(stats.volatility)],
      ["Variance", num(stats.variance)],
      ["Historical Sharpe", ratio(stats.historical_sharpe)],
      ["Objective Sharpe", ratio(stats.objective_sharpe)],
      ["Max drawdown", pct(stats.max_drawdown)],
      ["Best month", month(stats.best_month)],
      ["Worst month", month(stats.worst_month)],
    ];
    const grid = document.getElementById("summary");
    grid.replaceChildren();
    cards.forEach(([label, value]) => {
      const card = document.createElement("div");
      card.className = "stat";
      const name = document.createElement("span");
      name.textContent = label;
      const figure = document.createElement("b");
      figure.textContent = value;
      card.append(name, figure);
      grid.append(card);
    });
  }

  function renderCaptions(captions) {
    const box = document.getElementById("captions");
    box.replaceChildren();
    ["volatility", "sharpe", "expected", "scaled", "cash", "growth"].forEach((key) => {
      if (!captions[key]) return;
      const paragraph = document.createElement("p");
      paragraph.textContent = captions[key];
      box.append(paragraph);
    });
  }

  function renderVector(id, tickers, values, heading) {
    const table = document.createElement("table");
    table.className = "matrix";
    const head = document.createElement("tr");
    head.append(th("Holding"), th(heading));
    const thead = document.createElement("thead");
    thead.append(head);
    const body = document.createElement("tbody");
    tickers.forEach((ticker, index) => {
      const row = document.createElement("tr");
      row.append(td(ticker), td(num(values[index])));
      body.append(row);
    });
    table.append(thead, body);
    document.getElementById(id).replaceChildren(table);
  }

  function renderMatrix(id, tickers, matrix, format) {
    const table = document.createElement("table");
    table.className = "matrix";
    const head = document.createElement("tr");
    head.append(th(""));
    tickers.forEach((ticker) => head.append(th(ticker)));
    const thead = document.createElement("thead");
    thead.append(head);
    const body = document.createElement("tbody");
    matrix.forEach((rowValues, rowIndex) => {
      const row = document.createElement("tr");
      row.append(th(tickers[rowIndex]));
      rowValues.forEach((value) => row.append(td(format(value))));
      body.append(row);
    });
    table.append(thead, body);
    document.getElementById(id).replaceChildren(table);
  }

  function renderHeatmap(tickers, matrix) {
    const table = document.createElement("table");
    table.className = "matrix heat";
    const head = document.createElement("tr");
    head.append(th(""));
    tickers.forEach((ticker) => head.append(th(ticker)));
    const thead = document.createElement("thead");
    thead.append(head);
    const body = document.createElement("tbody");
    matrix.forEach((rowValues, rowIndex) => {
      const row = document.createElement("tr");
      row.append(th(tickers[rowIndex]));
      rowValues.forEach((value) => {
        const cell = td(value === null ? "—" : Number(value).toFixed(2));
        cell.style.background = heatColor(value);
        row.append(cell);
      });
      body.append(row);
    });
    table.append(thead, body);
    document.getElementById("heatmap").replaceChildren(table);
  }

  function renderAssets(assets) {
    const table = document.createElement("table");
    table.className = "data";
    const headers = ["Ticker", "Weight", "Hist. return", "Expected", "Vol", "Sharpe", "Max DD", "Best month", "Worst month", "Dividend", "Risk share"];
    const head = document.createElement("tr");
    headers.forEach((header) => head.append(th(header)));
    const thead = document.createElement("thead");
    thead.append(head);
    const body = document.createElement("tbody");
    assets.forEach((asset) => {
      const row = document.createElement("tr");
      [
        asset.ticker,
        pct(asset.weight),
        pct(asset.historical_return),
        pct(asset.expected_return),
        pct(asset.volatility),
        ratio(asset.sharpe),
        pct(asset.max_drawdown),
        month(asset.best_month),
        month(asset.worst_month),
        asset.dividend_yield === null ? "Unavailable" : pct(asset.dividend_yield),
        asset.component_share === null ? "—" : pct(asset.component_share),
      ].forEach((value) => row.append(td(value)));
      body.append(row);
    });
    table.append(thead, body);
    document.getElementById("asset-table").replaceWith(table);
    table.id = "asset-table";
  }

  function renderComparison(rows) {
    const table = document.createElement("table");
    table.className = "data";
    const head = document.createElement("tr");
    ["Strategy", "Volatility", "Expected return", "Objective Sharpe", "Weights"].forEach((header) => head.append(th(header)));
    const thead = document.createElement("thead");
    thead.append(head);
    const body = document.createElement("tbody");
    rows.forEach((row) => {
      const line = document.createElement("tr");
      if (!row.ok) {
        line.append(td(row.name), td(row.error));
        line.lastChild.colSpan = 4;
        body.append(line);
        return;
      }
      const mix = row.weights.map((item) => `${item.ticker} ${pct(item.weight)}`).join(", ");
      [row.name, pct(row.volatility), pct(row.expected_return), ratio(row.objective_sharpe), mix].forEach((value) => {
        line.append(td(value));
      });
      body.append(line);
    });
    table.append(thead, body);
    const existing = document.getElementById("comparison-table");
    table.id = "comparison-table";
    existing.replaceWith(table);
    document.getElementById("results-body").hidden = false;
    document.getElementById("results-hint").hidden = true;
  }

  function renderCharts(body) {
    const labels = body.charts.dates;
    const growthSets = [{
      label: "Portfolio",
      data: body.charts.growth.portfolio,
      borderColor: "#1a5f4a",
      borderWidth: 2.5,
      pointRadius: 0,
      tension: 0.1,
    }];
    Object.entries(body.charts.growth.assets).forEach(([ticker, data], index) => {
      growthSets.push(lineSet(ticker, data, PALETTE[(index + 1) % PALETTE.length]));
    });
    if (body.charts.growth.benchmark) {
      growthSets.push(lineSet(body.charts.growth.benchmark_name, body.charts.growth.benchmark, "#b42318"));
    }
    drawChart("growth-chart", {
      type: "line",
      data: { labels, datasets: growthSets },
      options: chartOptions("Growth of 1"),
    });
    drawChart("drawdown-chart", {
      type: "line",
      data: {
        labels,
        datasets: [{
          label: "Drawdown",
          data: body.charts.drawdown.map((value) => value * 100),
          borderColor: "#b42318",
          backgroundColor: "rgba(180, 35, 24, 0.15)",
          fill: true,
          pointRadius: 0,
        }],
      },
      options: chartOptions("Drawdown %"),
    });
    const positive = body.math.weights
      .map((weight, index) => ({ label: body.math.tickers[index], weight }))
      .filter((item) => item.weight > 0.0005);
    drawChart("allocation-chart", pieConfig(positive.map((item) => item.label), positive.map((item) => item.weight * 100)));
    if (body.math.negative_component || body.math.zero_risk) {
      drawChart("risk-chart", {
        type: "bar",
        data: {
          labels: body.math.tickers,
          datasets: [{
            label: "Component risk",
            data: body.math.component_risk.map((value) => value * 100),
            backgroundColor: "#1a5f4a",
          }],
        },
        options: chartOptions("Contribution to volatility, percentage points"),
      });
    } else {
      const slices = body.math.component_share
        .map((share, index) => ({ label: body.math.tickers[index], share }))
        .filter((item) => item.share > 0.0005);
      drawChart("risk-chart", pieConfig(slices.map((item) => item.label), slices.map((item) => item.share * 100)));
    }
    const frontier = body.charts.frontier.map((point) => ({
      x: point.volatility * 100,
      y: point.expected_return * 100,
    }));
    const strategySets = body.charts.strategy_points.map((point, index) => ({
      label: point.name,
      data: [{ x: point.volatility * 100, y: point.expected_return * 100 }],
      backgroundColor: PALETTE[index % PALETTE.length],
      pointRadius: 6,
    }));
    drawChart("frontier-chart", {
      type: "scatter",
      data: {
        datasets: [{
          label: "Frontier",
          data: frontier,
          showLine: true,
          borderColor: "#8a9a93",
          backgroundColor: "#8a9a93",
          pointRadius: 2,
        }, ...strategySets],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { position: "bottom" } },
        scales: {
          x: { title: { display: true, text: "Volatility % per year" } },
          y: { title: { display: true, text: "Expected return % per year" } },
        },
      },
    });
  }

  async function save() {
    try {
      await readJson(await fetch(`/api/portfolio/${portfolioId}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(spec()),
      }));
      setStatus("Saved on this computer.");
    } catch (error) {
      showError(error.message);
    }
  }

  async function remove() {
    if (!confirm("Delete this portfolio?")) return;
    const response = await fetch(`/api/portfolio/${portfolioId}`, { method: "DELETE" });
    if (response.ok) location.href = "/";
  }

  function updateWeightSum() {
    let sum = 0;
    document.querySelectorAll('#weight-table [data-role="weight"]').forEach((input) => {
      sum += numberFrom(input) || 0;
    });
    document.getElementById("weight-sum").textContent = `Weights add up to ${(sum * 100).toFixed(2)}%.`;
  }

  function showStrategyHint() {
    const key = document.querySelector('input[name="strategy"]:checked').value;
    document.getElementById("strategy-hint").textContent = STRATEGY_HINTS[key];
  }

  function showError(message) {
    const banner = document.getElementById("error-banner");
    banner.hidden = !message;
    banner.textContent = message || "";
  }

  function setStatus(message) {
    document.getElementById("status").textContent = message;
  }

  async function readJson(response) {
    const body = await response.json();
    if (!response.ok) throw new Error(body.error || "Request failed.");
    return body;
  }

  function drawChart(id, config) {
    if (charts[id]) charts[id].destroy();
    charts[id] = new Chart(document.getElementById(id), config);
  }

  function lineSet(label, data, color) {
    return { label, data, borderColor: color, backgroundColor: color, borderWidth: 1.4, pointRadius: 0, tension: 0.1 };
  }

  function pieConfig(labels, data) {
    return {
      type: "pie",
      data: { labels, datasets: [{ data, backgroundColor: labels.map((_, index) => PALETTE[index % PALETTE.length]) }] },
      options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: "bottom" } } },
    };
  }

  function chartOptions(label) {
    return {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { position: "bottom" } },
      scales: { y: { title: { display: true, text: label } } },
    };
  }

  function equation(math) {
    const terms = math.weights.map((weight, index) => `${weight.toFixed(4)} × ${math.sigma_w[index].toFixed(4)}`);
    return `variance = wᵀ (Σ w) = ${terms.join(" + ")} = ${math.variance.toFixed(6)}. Volatility = ${pct(math.volatility)}.`;
  }

  function setExact(input, value) {
    input.dataset.exact = String(value);
    input.value = (value * 100).toFixed(2);
  }

  function numberFrom(input) {
    if (!input || input.value === "") return null;
    if (input.dataset.exact && input.value === (Number(input.dataset.exact) * 100).toFixed(2)) {
      return Number(input.dataset.exact);
    }
    return Number(input.value) / 100;
  }

  function percentNumber(value) {
    return (Number(value) * 100).toFixed(2).replace(/\.00$/, "");
  }

  function pct(value) {
    if (value === null || value === undefined || Number.isNaN(value)) return "Unavailable";
    return `${(value * 100).toFixed(2)}%`;
  }

  function num(value) {
    if (value === null || value === undefined || Number.isNaN(value)) return "—";
    const absolute = Math.abs(value);
    if (absolute < 5e-5) return "0.0000";
    if (absolute < 0.0001) return value.toExponential(2);
    return value.toFixed(4);
  }

  function ratio(value) {
    if (value === null || value === undefined) return "Undefined";
    return Number(value).toFixed(2);
  }

  function month(entry) {
    if (!entry) return "—";
    return `${entry.label} ${pct(entry.return)}`;
  }

  function th(text) {
    const cell = document.createElement("th");
    cell.textContent = text;
    return cell;
  }

  function td(text) {
    const cell = document.createElement("td");
    cell.textContent = text;
    return cell;
  }

  function heatColor(value) {
    if (value === null || Number.isNaN(value)) return "#eef2f0";
    const amount = Math.max(-1, Math.min(1, value));
    return amount >= 0 ? mix("#ffffff", "#1a5f4a", amount) : mix("#ffffff", "#b42318", -amount);
  }

  function mix(start, end, amount) {
    const from = hex(start);
    const to = hex(end);
    const channels = from.map((channel, index) => Math.round(channel + (to[index] - channel) * amount));
    return `rgb(${channels[0]}, ${channels[1]}, ${channels[2]})`;
  }

  function hex(color) {
    return [1, 3, 5].map((offset) => parseInt(color.slice(offset, offset + 2), 16));
  }

  function cssEscape(value) {
    if (window.CSS && CSS.escape) return CSS.escape(value);
    return value.replace(/[^a-zA-Z0-9_-]/g, "\\$&");
  }

  return { start };
})();
