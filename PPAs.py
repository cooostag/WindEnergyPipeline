from dataclasses import dataclass
import pandas as pd

#TODO: Insert direction logic in PPA parent class


@dataclass
class PPA:
    ppa_id: str
    project_name: str
    project_location: str
    project_capacity_numberAssets: float
    ppa_start_date: str
    ppa_end_date: str
    #ppa_price_per_mwh: float
    offtaker_name: str
    offtaker_credit_rating: str
    direction_type: str
    direction_multiplier: int


@dataclass
class FixedPricePPA_asProduced (PPA):
    price_mwh: float
    price_type: str = "Fixed Price"

@dataclass
class IndexPricePPA_asProduced (PPA):
    price_data: float
    index_market: pd.DataFrame
    price_type: str = "Index Price"
