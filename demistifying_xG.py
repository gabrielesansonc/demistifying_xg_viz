from utility_demistifying_xG import filter_data, calculate_avg_xG, output_results_distribution

from flask import Flask, request, jsonify
from flask_cors import CORS  # 🔹 Import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)  # 🔹 Enable CORS for all routes

df = pd.read_csv('shots.csv')
print(output_results_distribution(.90, 0.5, df, 0.025))

@app.route('/compute', methods=['POST'])
def compute():
    data = request.json  

    # Extract values
    x = float(data.get("x", 0))
    y = float(data.get("y", 0))
    last_action = data.get("last_action")
    shot_type = data.get("shot_type")
    situation = data.get("situation")



    data_filtered = filter_data(df, lastAction=last_action, shotType=shot_type, situation=situation)
    
    average_xG = calculate_avg_xG(x, y, data_filtered, 0.025)
    results_df = output_results_distribution(x, y, data_filtered, 0.025)

    results_json = results_df

    return jsonify({
        "Average xG": average_xG,
        "Result": results_json
    })

if __name__ == '__main__':
    app.run(debug=True)
