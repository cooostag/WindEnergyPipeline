from dataclasses import dataclass
import pandas as pd

@dataclass
class PPA:
    ppa_id: str
    project_name: str
    project_location: str
    project_capacity_mw: float
    ppa_start_date: str
    ppa_end_date: str
    #ppa_price_per_mwh: float
    offtaker_name: str
    offtaker_credit_rating: str


@dataclass
class FixedPricePPA_asProduced (PPA):
    ppa_price_per_mwh: float
    price_type: str = "Fixed Price"

@dataclass
class IndexPricePPA_asProduced (PPA):
    price_index: float
    index_market: pd.DataFrame
    price_type: str = "Index Price"
