from http.server import BaseHTTPRequestHandler
import json
import os
import sys
import pandas as pd

sys.path.insert(0, os.path.dirname(__file__))
from utility import filter_data, calculate_avg_xG, output_results_distribution

csv_path = os.path.join(os.path.dirname(__file__), '..', 'shots.csv')
df = pd.read_csv(csv_path)


class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        data = json.loads(body)

        x = float(data.get("x", 0))
        y = float(data.get("y", 0))
        last_action = data.get("last_action")
        shot_type = data.get("shot_type")
        situation = data.get("situation")

        data_filtered = filter_data(df, lastAction=last_action, shotType=shot_type, situation=situation)
        average_xG = calculate_avg_xG(x, y, data_filtered, radius_px=25)
        results_json = output_results_distribution(x, y, data_filtered, radius_px=25)

        response = {
            "Average xG": average_xG,
            "Result": results_json
        }

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())
