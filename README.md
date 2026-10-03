# Renewable PPA Valuation Pipeline

## Project status

**Stage 1 --- completed**

End-to-end PPA valuation using renewable generation and Day-Ahead
electricity prices.

**Stage 2 --- in progress**


------------------------------------------------------------------------

## 1.1 Objective

The purpose of the project is to answer a simple energy-market question:

> Given an expected renewable generation profile, a fixed PPA price and
> the corresponding Day-Ahead market price, what is the resulting
> revenue and P&L for the asset?

The prototype uses a 15-minute time resolution, allowing the generation
forecast and market price to be aligned interval by interval.

Conceptually:

``` text
Weather data
     ↓
Wind generation model
     ↓
Generation forecast
     ↓
        ┌──────────────────┐
        │  PPA valuation   │
        └──────────────────┘
             ↑        ↑
             │        │
       PPA price   Day-Ahead price
```

------------------------------------------------------------------------

## 1.2 Stage 1 components

### 1.2.1 Weather data

Weather forecast data is retrieved at 15-minute resolution from open-meteo
https://api.open-meteo.com/v1/forecast

The prototype uses wind speed at 80 m as the main input for the
simplified wind generation model.

Additional weather variables such as temperature and precipitation are
also retrieved and retained in the weather dataset.

The weather data is represented as a time series with timezone-aware
timestamps.

------------------------------------------------------------------------

### 1.2.2 Wind generation model

A simplified wind-turbine power curve converts wind speed into
electrical output.

The model uses the following basic operating regions:

-   Below cut-in wind speed → 0 output
-   Between cut-in and rated wind speed → increasing output
-   Between rated wind speed and cut-out wind speed → rated output
-   Above cut-out wind speed → 0 output

For Stage 1, this is deliberately a simplified engineering model rather
than a manufacturer-specific turbine power curve.


The model can later be extended to represent a complete wind farm with
multiple turbines.

------------------------------------------------------------------------

### 1.2.3 Day-Ahead market prices

Day-Ahead electricity prices are retrieved for the DE-LU market area from energy-charts:
https://api.energy-charts.info/price

The project aims to align all timeseries to a 15 min resolution, this is in line with the German Day-Ahead market settlement period.


------------------------------------------------------------------------

### 1.2.4 PPA

Stage 1 uses a simple fixed-price PPA.

Example:

``` text
PPA price = 50 €/MWh
```

The PPA price is assumed to apply to the generated electricity.

The project structure is designed so that additional PPA types can be
introduced later through specialised classes.

------------------------------------------------------------------------

## 1.2.3 Valuation calculation

The central output of Stage 1 is the valuation DataFrame.

It combines:

-   timestamp
-   weather variables
-   `power_output`
-   `DA_price`
-   `PPA_price`
-   `Revenue`
-   `P&L`

A simplified interval-level calculation is:

### Revenue

``` text
Revenue = PPA_price × generated_energy
```

### P&L versus Day-Ahead market

``` text
P&L = (PPA_price - DA_price) × generated_energy
```

This can also be understood as:

``` text
P&L = PPA revenue - market value of generation
```

For a seller with a fixed-price PPA:

-   If `PPA_price > DA_price`, the PPA generates positive value relative
    to selling at Day-Ahead.
-   If `PPA_price < DA_price`, the PPA generates negative value relative
    to the Day-Ahead reference.
-   If there is no generation, the interval P&L is zero.

------------------------------------------------------------------------


------------------------------------------------------------------------

## 1.2.4 Aggregating the valuation

Once each interval contains a correctly calculated euro value, the total
daily P&L can simply be calculated as:

``` text
Daily P&L = sum(interval P&L)
```

For example:

``` python
daily_pnl = valuation_df["P&L"].sum()
```

The same approach can be used for:

``` text
Daily revenue
Monthly revenue
Annual revenue
Daily P&L
Monthly P&L
Annual P&L
```

provided that the underlying intervals are correctly represented in
energy units.

------------------------------------------------------------------------

## 1.2.5 Why the timestamp is an index

The valuation DataFrame uses the timestamp as its index.

This is appropriate for a time-series dataset because the timestamp is
the natural key used to:

-   align generation and market prices
-   join different time series
-   resample data
-   filter specific periods
-   calculate daily/monthly aggregates
-   plot time series

For example:

``` python
valuation_df.loc["2026-09-30"]
```

can directly select the relevant day.

A timestamp can still be converted back to a normal column when
exporting data to systems where a conventional tabular structure is
preferred.

------------------------------------------------------------------------

# 1.3 Stage 1 architecture

A simplified conceptual architecture is:

``` text
                    ┌─────────────────┐
                    │  Weather API    │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Weather object  │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Generation      │
                    │ model           │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Generation DF   │
                    └────────┬────────┘
                             │
                             │
             ┌───────────────┴────────────────┐
             │                                │
             ▼                                ▼
    ┌─────────────────┐              ┌─────────────────┐
    │ Day-Ahead price │              │ PPA contract    │
    │ time series     │              │                 │
    └────────┬────────┘              └────────┬────────┘
             │                                │
             └───────────────┬────────────────┘
                             ▼
                    ┌─────────────────┐
                    │ PPA valuation   │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Valuation DF    │
                    │ Revenue / P&L   │
                    └─────────────────┘
```

------------------------------------------------------------------------

# Project structure
WIP

``` text

```



------------------------------------------------------------------------

# 2. Stage 2 --- in progress

------------------------------------------------------------------------
# 2.1 Market forward curve

Build a German power forward curve from EEX futures data.

The current prototype uses a manually collected market snapshot due to
limited access to historical EEX derivatives data.

Current implementation:
- Monthly futures
- Yearly futures

Potential extension:
- Quarterly futures
- Weekly / shorter-term maturities

The forward curve is represented as a daily market observation
and is used as the market basis for forward PPA valuation. The forward curve is also computed on daily basis and the resolution of the project switches from 15-min to daily from d+2, where DA prices are not available. 

Historical forward curves are currently outside the project scope due to
limited access to historical EEX derivatives data. The architecture is
designed so that historical observations can be integrated when
available.

------------------------------------------------------------------------

# 2.2 Stochastic market-price modelling

Develop a stochastic model for German power forward prices starting from the forward curve computed in 2.1.

Potential components:

- Define a volatility structure across delivery periods
- Define correlations between delivery periods
- Generate correlated stochastic forward-price scenarios
- Compare different stochastic assumptions/models

Where historical market data is unavailable, parameters will initially
be informed by relevant academic literature and explicitly documented
as assumptions.
------------------------------------------------------------------------
# 2.3 PPA mark-to-market

Extend the PPA valuation from Day-Ahead prices to forward market prices.

- Revalue the PPA against the current forward curve
- Calculate PPA mark-to-market (MtM)
- Calculate sensitivity to changes in forward prices

------------------------------------------------------------------------
# 2.4 MonteCarlo valuation & market risk

Use the stochastic forward-price scenarios to:

- Revalue the PPA under each scenario
- Produce a simulated P&L distribution
- Calculate VaR
- Calculate Expected Shortfall
- Analyse sensitivity to stochastic model assumptions
------------------------------------------------------------------------
# 2.5 Market risk - OPTIONAL
Historical P&L distribution
VaR
Expected Shortfall
Stress scenarios

------------------------------------------------------------------------
# 2.6 Renewable capture pricing - separate analysis

Generation-weighted market price

Capture price vs Baseload

Capture-price factor

PPA pricing