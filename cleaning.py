import pandas as pd


def load_data(path):
    data = pd.read_csv(path)
    return data

def drop_data(data: pd.DataFrame) -> pd.DataFrame:
    data = data[data["bedrooms"] != 33].copy()
    return data

def reconstruct_basement_size(data):
    data = data.copy()
    data_new = data["sqft_living"] - data["sqft_above"]
    data["sqft_basement"] = data_new
    return data

def replace_missing_values(data):
    data = data.copy()
    data_view = data["view"].fillna(0)
    data_waterfront = data["waterfront"].fillna(0)
    data["view"] = data_view
    data["waterfront"] = data_waterfront
    return data

def transfer_built_renovated(data):
    data = data.copy()
    last_known_change = []
    for idx, yr_re in data["yr_renovated"].items():
        if str(yr_re) == "nan" or yr_re == 0.0:
            last_known_change.append(data["yr_built"][idx])
        else:
            last_known_change.append(int(yr_re))
    data["last_known_change"] = last_known_change
    data = data.drop("yr_renovated", axis=1)
    data = data.drop("yr_built", axis=1)
    return data

def cleaning_pipeline(data):
    data = drop_data(data)
    data = reconstruct_basement_size(data)
    data = replace_missing_values(data)
    data = transfer_built_renovated(data)
    return data