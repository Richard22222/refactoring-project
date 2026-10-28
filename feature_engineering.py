import numpy as np
import pandas as pd


def variable_price(data: pd.DataFrame) -> pd.DataFrame:
    data = data.copy()
    data["sqft_price"] = (data.price / (data.sqft_living + data.sqft_lot)).round(2)
    return data

def distance_wealth(data):
    data = data.copy()
    data["delta_lat"] = np.absolute(47.62774 - data["lat"])
    # Absolute difference in longitude between the center and the property.
    data["delta_long"] = np.absolute(-122.24194 - data["long"])
    # Distance between the center and the property.
    data["center_distance"] = (((data["delta_long"] * np.cos(np.radians(47.6219))) ** 2 + 
                                data["delta_lat"] ** 2)** (1 / 2) * 2 * np.pi * 6378 / 360)
    return data


def dist_waterfront(data):
    data = data.copy()
    def dist(long, lat, ref_long, ref_lat):
        delta_long = long - ref_long
        delta_lat = lat - ref_lat
        delta_long_corr = delta_long * np.cos(np.radians(ref_lat))
        return (((delta_long_corr) ** 2 + (delta_lat) ** 2) ** (1 / 2) * 2 * np.pi * 6378 / 360)
    
    water_list = data.query("waterfront == 1")
    water_distance = []
    for idx in data.index:
        ref_list = []
        for x, y in zip(list(water_list["long"]), list(water_list["lat"])):
            ref_list.append(dist(data["long"][idx], data["lat"][idx], x, y).min())
        water_distance.append(min(ref_list))
    data["water_distance"] = water_distance
    return data

def feature_engineering(data):
    data = variable_price(data)
    data = distance_wealth(data)
    data = dist_waterfront(data)
    return data