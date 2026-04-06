import pandas as pd


def filter_data(data, lastAction=None, shotType=None, situation=None):
    data = data.copy()
    filters = [("lastAction", lastAction), ("shotType", shotType), ("situation", situation)]
    for col, val in filters:
        if val != "All":
            data = data[data[col] == val]
    return data


def calculate_avg_xG(X, Y, data_filtered, precision):
    data_filtered_location = data_filtered[
        (data_filtered['X'] > (X - precision)) & (data_filtered['X'] < (X + precision)) &
        (data_filtered['Y'] > (Y - precision)) & (data_filtered['Y'] < (Y + precision))
    ]
    if data_filtered_location.empty:
        return 0.0
    return round(data_filtered_location['xG'].mean(), 2)


def output_results_distribution(X, Y, data_filtered, precision):
    data_filtered_location = data_filtered[
        (data_filtered['X'] > (X - precision)) & (data_filtered['X'] < (X + precision)) &
        (data_filtered['Y'] > (Y - precision)) & (data_filtered['Y'] < (Y + precision))
    ]
    if data_filtered_location.empty or "result" not in data_filtered_location.columns:
        return {
            "MissedShots": 0.0,
            "Goal": 0.0,
            "SavedShot": 0.0,
            "BlockedShot": 0.0,
            "ShotOnPost": 0.0,
            "OwnGoals": 0.0
        }
    class_counts = data_filtered_location["result"].value_counts(normalize=True) * 100
    return class_counts.to_dict()
