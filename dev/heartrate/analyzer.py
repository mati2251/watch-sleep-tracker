import numpy as np

def calculate_rmssd(ibi_values):
    if len(ibi_values) < 2:
        return None
    squared_differences = np.diff(ibi_values) ** 2
    mean_squared_diff = np.mean(squared_differences)
    return np.sqrt(mean_squared_diff)

def calculate_sdnn(ibi_values):
    if len(ibi_values) < 2:
        return None
    return np.std(ibi_values)

def calculate_stress_score(hr, rmssd, sdnn, max_hr=110, max_rmssd=50, max_sdnn=50):
    normalized_hr = min((hr - 45) / (max_hr - 45), 1)
    normalized_rmssd = min((rmssd - 5) / (max_rmssd - 5), 1)
    normalized_sdnn = min(sdnn / max_sdnn, 1)

    stress_from_hr = normalized_hr
    stress_from_rmssd = 1 - normalized_rmssd
    stress_from_sdnn = 1 - normalized_sdnn

    final_stress_score = (stress_from_hr * 0.4 + stress_from_rmssd * 0.3 + stress_from_sdnn * 0.3) * 100

    return final_stress_score
