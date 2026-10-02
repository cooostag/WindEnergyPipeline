from DataClasses import *
from datetime import date

Cal27_Fut_Price = FuturePrices(
    maturity_type= "year",
    maturity= "2027",
    price_date= date(2026, 10, 1), #price observed on eex_market data website
    price= 129.97,
    currency= "EUR",
    unit= "MWh",
    market_area= "DE-LU",
    start_date= date(2027, 1, 1),
    end_date= date(2027, 12, 31)
)

Oct26_Fut_Price = FuturePrices(
    maturity_type= "month",
    maturity= "2027-10",
    price_date= date (2026, 10, 1), #price observed on eex_market data website
    price= 163.87, # this price will be used for the whole month of october because the manual initialization of weekly prices is too time consuming for this project
    currency= "EUR",
    unit= "MWh",
    market_area= "DE-LU",
    start_date= date (2026, 10, 1),
    end_date= date(2026, 10, 31)
)


Nov26_Fut_Price = FuturePrices(
    maturity_type= "month",
    maturity= "2027-11",
    price_date= date(2026, 10, 1), #price observed on eex_market data website
    price= 171.47,
    currency= "EUR",
    unit= "MWh",
    market_area= "DE-LU",
    start_date= date(2026, 11, 1),
    end_date= date(2026, 11, 30)
)

Dec26_Fut_Price = FuturePrices(
    maturity_type= "month",
    maturity= "2027-12",
    price_date= date(2026, 10, 1), #price observed on eex_market data website
    price= 166.41,
    currency= "EUR",
    unit= "MWh",
    market_area= "DE-LU",
    start_date= date(2026, 12, 1),
    end_date= date(2026, 12, 31)
)



def ForwardCurveConstruction(futures_prices_list: list[FuturePrices]) -> ForwardPriceCurve:

    # The list of future prices shares metadata that can be directly passed to the forwardpowercurve object.
        #these are: price_date, currency, unit, market_area

    #for the start / end date, a list of start and end dates will be created and the min / max will be used for the forward curve object
    start_dates = [f.start_date for f in futures_prices_list]
    end_dates = [f.end_date for f in futures_prices_list]

    forward_start_date = min(start_dates)
    forward_end_date = max(end_dates)

    Forward_Curve = ForwardPriceCurve(
        market_area=futures_prices_list[0].market_area,
        price_date=futures_prices_list[0].price_date,
        data=pd.DataFrame(),
        unit=futures_prices_list[0].unit,
        currency=futures_prices_list[0].currency,
        start_date=forward_start_date,
        end_date=forward_end_date
    )

    #now fill up the data into the data frame with daily granularity
    #first initialize a column with progressive dates from start date to end date
    date_range = pd.date_range(start=forward_start_date, end=forward_end_date, freq='D')
    Forward_Curve.data = pd.DataFrame(index=date_range)

    #now based on the start end date of the single entry to forward cure, initialize price

    for f in futures_prices_list:
        #create a date range for the single future price entry
        f_date_range = pd.date_range(start=f.start_date, end=f.end_date, freq='D')
        #fill the price into the forward curve data frame for the corresponding dates
        Forward_Curve.data.loc[f_date_range, 'price'] = f.price

    return Forward_Curve


test_Forward_Curve = ForwardCurveConstruction([Cal27_Fut_Price, Oct26_Fut_Price, Nov26_Fut_Price, Dec26_Fut_Price])

print("Forward Curve Data:")
print(test_Forward_Curve.data)

print ("success")