# Renewable PPA Valuation Pipeline

## Project status

**Stage 1 --- completed**

This project was built as a compact end-to-end prototype for valuing the
economics of a renewable power asset under a Power Purchase Agreement
(PPA).

Stage 1 is intentionally simple: it connects weather data, renewable
generation modelling, electricity market prices and a basic PPA
valuation into one reproducible pipeline.

The Stage 1 scope is now considered **complete and terminated**. The
next steps listed below are potential extensions rather than unfinished
Stage 1 requirements.

------------------------------------------------------------------------

## 1. Objective

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

## 2. Stage 1 components

### 2.1 Weather data

Weather forecast data is retrieved at 15-minute resolution from open-meteo
https://api.open-meteo.com/v1/forecast

The prototype uses wind speed at 80 m as the main input for the
simplified wind generation model.

Additional weather variables such as temperature and precipitation are
also retrieved and retained in the weather dataset.

The weather data is represented as a time series with timezone-aware
timestamps.

------------------------------------------------------------------------

### 2.2 Wind generation model

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

### 2.3 Day-Ahead market prices

Day-Ahead electricity prices are retrieved for the DE-LU market area from energy-charts:
https://api.energy-charts.info/price

The prices are aligned to the same 15-minute time grid as the generation
forecast.


------------------------------------------------------------------------

### 2.4 PPA

Stage 1 uses a simple fixed-price PPA.

Example:

``` text
PPA price = 50 €/MWh
```

The PPA price is assumed to apply to the generated electricity.

The project structure is designed so that additional PPA types can be
introduced later through specialised classes.

------------------------------------------------------------------------

## 3. Valuation calculation

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

## 4. Aggregating the valuation

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

## 6. Why the timestamp is an index

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

# Stage 1 architecture

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

# Stage 2 --- potential improvements

Stage 1 intentionally stops before introducing the complexity normally
required for a more realistic renewable trading / PPA valuation model.

Possible next stages include the following.

## 1. More realistic generation modelling

Replace the simplified power curve with more realistic ones


------------------------------------------------------------------------

## 2. Actual versus forecast generation

Separate:

``` text
Forecast generation
Actual generation
```


------------------------------------------------------------------------

## 3. Imbalance modelling

Introduce imbalance costs and revenues.

------------------------------------------------------------------------

## 4. More sophisticated PPA contracts

The current fixed-price PPA can be extended with different contract
structures.

------------------------------------------------------------------------

## 5. Market-price risk

The current valuation uses a single Day-Ahead price scenario.

A more advanced model to be evaluated:

------------------------------------------------------------------------

## 6. P&L and risk analytics

The next level could introduce...

------------------------------------------------------------------------

## 7. Data quality and production robustness

The prototype can eventually include

------------------------------------------------------------------------

## 8. Testing

A production-oriented version should introduce unit and integration
tests.
