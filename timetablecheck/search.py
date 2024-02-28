import json
from datetime import datetime, time

def loadjson():
    with open('times.json', 'r') as f:
        data = json.load(f)
        return data
def search(data, target_key, target_value):
    result = []
    if isinstance(data, dict):
        if data.get(target_key) == target_value:  # Check parent object first
            result.append(data.copy())  # Make a copy to avoid modifying original
        for value in data.values():
            result.extend(search(value, target_key, target_value))
    elif isinstance(data, list):
        for item in data:
            result.extend(search(item, target_key, target_value))
    return result
def getcurrentperiod(times=None):
    if times != None:
        period_start_times = times
    else:
        period_start_times = [time(8, 25), time(9, 20), time(11, 5), time(12, 00), time(13, 30), time(14, 25), time(15, 30)]  # Adjust according to your actual periods
    current_time = datetime.now().time()
    current_period = 0
    for i, start_time in enumerate(period_start_times):
        if current_time >= start_time and current_time <= time(15, 30):
            current_period = i + 1
        else:
            return [current_period, period_start_times]
        
def search_(data, target_key):
    matching_values = {}
    if isinstance(data, dict):
        for key, value in data.items():
            if key == target_key:
                matching_values[key] = value
            else:
                matching_values.update(search_(value, target_key))  # Recurse
    elif isinstance(data, list):
        for item in data:
            matching_values.update(search_(item, target_key))  # Recurse

    return matching_values
