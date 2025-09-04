

import pandas as pd
import zipfile

zip = "temperatures.zip"


with zipfile.ZipFile(zip, "r") as z:
    csv_files = [f for f in z.namelist() if f.endswith(".csv")]
    dfs = [pd.read_csv(z.open(f)) for f in csv_files]
    data = pd.concat(dfs, ignore_index=True)

print("Merged shape:", data.shape)

# Reshaping
data_long = data.melt(
    id_vars=["STATION_NAME", "STN_ID", "LAT", "LON"],
    value_vars=["January","February","March","April","May","June",
                "July","August","September","October","November","December"],
    var_name="Month",
    value_name="Temperature"
)

# Dropping missing values
data_long = data_long.dropna(subset=["Temperature"])

# Map months to Australian seasons
season_map = {
    "December": "Summer", "January": "Summer", "February": "Summer",
    "March": "Autumn", "April": "Autumn", "May": "Autumn",
    "June": "Winter", "July": "Winter", "August": "Winter",
    "September": "Spring", "October": "Spring", "November": "Spring"
}
data_long["Season"] = data_long["Month"].map(season_map)

seasonal_avg = data_long.groupby("Season")["Temperature"].mean()

with open("average_temp.txt", "w") as f:
    for season, temp in seasonal_avg.items():
        f.write(f"{season}: {temp:.1f}°C\n")

print("✅ Seasonal averages saved to average_temp.txt")

# Temperature Range per station
station_stats = data_long.groupby("STATION_NAME")["Temperature"].agg(["max", "min"])
station_stats["range"] = station_stats["max"] - station_stats["min"]

# Find max range value and all stations that match this max range
max_range = station_stats["range"].max()
largest_range_stations = station_stats[station_stats["range"] == max_range]

# Results
with open("largest_temp_range_station.txt", "w") as f:
    for station, row in largest_range_stations.iterrows():
        f.write(f"{station}: Range {row['range']:.1f}°C (Max: {row['max']:.1f}°C, Min: {row['min']:.1f}°C)\n")

print("✅ Largest temp range station(s) saved to largest_temp_range_station.txt")

month_cols = ["January","February","March","April","May","June",
              "July","August","September","October","November","December"]

# Compute std dev across months for each station
data["StdDev"] = data[month_cols].std(axis=1)

min_std = data["StdDev"].min()
max_std = data["StdDev"].max()

most_stable = data[data["StdDev"] == min_std]
most_variable = data[data["StdDev"] == max_std]

with open("temperature_stability_stations.txt", "w") as f:
    for _, row in most_stable.iterrows():
        f.write(f"Most Stable: Station {row['STATION_NAME']}: StdDev {row['StdDev']:.1f}°C\n")
    for _, row in most_variable.iterrows():
        f.write(f"Most Variable: Station {row['STATION_NAME']}: StdDev {row['StdDev']:.1f}°C\n")
print("✅ Temperature stability results saved to temperature_stability_stations.txt")