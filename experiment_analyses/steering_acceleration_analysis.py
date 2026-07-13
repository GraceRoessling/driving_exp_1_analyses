import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math

def calculate_average_steering_acceleration(df):
    if len(df) < 5:
        return np.nan
    else:
        # Prepare data for differentiation
        time_series,steering_angle = df["time"].values,df["steering_angle"].values      # Get time and steering angle arrays
        time_diffs = np.diff(time_series) # Get delta T
        steering_angle_smoothed = pd.Series(steering_angle).rolling(window=13,center=True).mean().values # Smooth steering angle

        # Calculate steering rate (angular velocity)
        steering_rates = np.diff(steering_angle_smoothed) / time_diffs
        steering_rates = np.append(steering_rates, np.nan) # Pad to keep alignment with time series (same length)
        steering_rate_smoothed = pd.Series(steering_rates).rolling(window=13,center=True).mean().values # Smooth the steering rates
        
        # Add padding/maintain alignment before last differentiation
        valid_rates = steering_rate_smoothed[:-1] # Remove the last nan from rolling window avg
        
        # Calculate steering acceleration
        steering_acceleration = np.diff(valid_rates) / time_diffs[1:] # Compute steering acceleration
        steering_acceleration = np.append(steering_acceleration, [np.nan, np.nan])  # Two padding values to match original size
        steering_acceleration_smoothed = pd.Series(steering_acceleration).rolling(window=13,center=True).mean().abs() # Smooth and take absolute value

        # plt.plot(time_series, steering_angle)
        # plt.plot(time_series, steering_angle_smoothed)
        # plt.show()
        # if len(df["steering_acceleration"]) == 0:
        # plot_everything(time_series,steering_angle,steering_angle_smoothed,steering_rate_smoothed,steering_acceleration_smoothed)

        return steering_acceleration_smoothed


def plot_everything(time_series,steering_angle,steering_angle_smoothed,steering_rate_smoothed,steering_acceleration_smoothed):
    
    # Plot 1: Original steering angle
    fig, axs = plt.subplots(2, 2, figsize=(12, 8))
    axs[0, 0].plot(time_series, steering_angle, label="Original")
    axs[0, 0].set_title("Original Steering Angle")
    axs[0, 0].set_xlabel("Time")
    axs[0, 0].set_ylabel("Steering Angle")
    axs[0, 0].legend()

    # Plot 2: Smoothed steering angle
    axs[1, 0].plot(time_series, steering_angle_smoothed, label="Smoothed", color='orange')
    axs[1, 0].set_title("Smoothed Steering Angle")
    axs[1, 0].set_xlabel("Time")
    axs[1, 0].set_ylabel("Steering Angle")
    axs[1, 0].legend()
    
    # Plot 3: Steering rate
    axs[0, 1].plot(time_series, steering_rate_smoothed, label="Steering Rate Smoothed", color='green')
    axs[0, 1].set_title("Steering Rate")
    axs[0, 1].set_xlabel("Time")
    axs[0, 1].set_ylabel("Rate (deg/s)")
    axs[0, 1].legend()

    # Plot 4: Steering acceleration
    axs[1, 1].plot(time_series,steering_acceleration_smoothed, label="Steering Acceleration Smoothed", color='red')
    axs[1, 1].set_title("Steering Acceleration")
    axs[1, 1].set_xlabel("Time")
    axs[1, 1].set_ylabel("Acceleration (deg/s²)")
    axs[1, 1].legend()

    plt.tight_layout()
    plt.show()

