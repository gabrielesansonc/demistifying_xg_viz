import pandas as pd

# Field render dimensions — must match the frontend SVG
FIELD_W = 800
FIELD_H = 512


def filter_data(data, lastAction=None, shotType=None, situation=None):
    data = data.copy()
    filters = [("lastAction", lastAction), ("shotType", shotType), ("situation", situation)]
    for col, val in filters:
        if val != "All":
            data = data[data[col] == val]
    return data


def _circle_mask(X, Y, data_filtered, radius_px):
    """Return rows within radius_px pixels of (X, Y), using pixel-space distance."""
    dx = (data_filtered['X'] - X) * FIELD_W
    dy = (data_filtered['Y'] - Y) * FIELD_H
    return data_filtered[(dx**2 + dy**2) < radius_px**2]


def calculate_avg_xG(X, Y, data_filtered, radius_px=50):
    nearby = _circle_mask(X, Y, data_filtered, radius_px)
    if nearby.empty:
        return 0.0
    return round(nearby['xG'].mean(), 2)


def output_results_distribution(X, Y, data_filtered, radius_px=50):
    nearby = _circle_mask(X, Y, data_filtered, radius_px)
    if nearby.empty or "result" not in nearby.columns:
        return {
            "MissedShots": 0.0,
            "Goal": 0.0,
            "SavedShot": 0.0,
            "BlockedShot": 0.0,
            "ShotOnPost": 0.0,
            "OwnGoals": 0.0
        }
    class_counts = nearby["result"].value_counts(normalize=True) * 100
    return class_counts.to_dict()
