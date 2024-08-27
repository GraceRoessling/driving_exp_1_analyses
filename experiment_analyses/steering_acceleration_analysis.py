import numpy as np

def calculate_average_steering_acceleration(df):
    # Get desired arrays (time and steering angle)
    time_series = df["time"]
    steering_angle = df["steering_angle"]
    steering_angle_smoothed = steering_angle.rolling(window=10).mean() # first, smooth out original steering angle over time

    # Transform data for differentiation
    steering_angles,time_series = np.array(steering_angle_smoothed),np.array(time_series) # Convert input arrays are numpy arrays
    time_diffs = np.diff(time_series) # Calculate time differences (delta t)
    
    # Calculate steering rate (angular velocity) ------------
    df["steering_rates"] = np.append((np.diff(steering_angles) / time_diffs), [np.nan])
    df["steering_rates"] = df["steering_rates"].rolling(window=10).mean()

    # Calculate steering acceleration (angular acceleration) ---------
    steering_rate_smoothed = np.delete(np.array(df["steering_rates"]), -1) # Apply rolling window average to steering rate
    steering_accelerations = np.diff(steering_rate_smoothed) / time_diffs[1:]
    steering_acceleration_column = np.append(steering_accelerations, [np.nan, np.nan])
    df["steering_acceleration"] = steering_acceleration_column
    df["steering_acceleration"] = df["steering_acceleration"].rolling(window=10).mean().abs()

    return df["steering_acceleration"]