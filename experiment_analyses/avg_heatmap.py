import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist
from collections import defaultdict

def find_closest_trajectory_point(driver_positions, road_point):
    """
    Find the closest point in a driver's trajectory to a road centerline point.
    
    Args:
        driver_positions (np.array): Nx2 array of [x, y] positions over time
        road_point (tuple): (x, y) coordinates of road centerline point
        
    Returns:
        int: Index of closest trajectory point
    """
    distances = cdist([road_point], driver_positions)[0]
    return np.argmin(distances)

def process_single_driver(driver_positions, driver_speeds, road_centerline_df):
    """
    Process a single driver's data to create speed-position associations.
    
    Args:
        driver_positions (np.array): Nx2 array of [x, y] positions over time
        driver_speeds (np.array): N-length array of speeds over time
        road_centerline_df (pd.DataFrame): DataFrame with 'x' and 'y' columns
        
    Returns:
        list: List of tuples [(road_point_idx, speed), ...]
    """
    driver_speed_list = []
    
    for road_idx, row in road_centerline_df.iterrows():
        road_point = (row['x'], row['y'])
        
        # Find closest trajectory point
        closest_traj_idx = find_closest_trajectory_point(driver_positions, road_point)
        
        # Get speed at that time (with bounds checking)
        if 0 <= closest_traj_idx < len(driver_speeds):
            speed = driver_speeds[closest_traj_idx]
        else:
            speed = 0.0
        
        driver_speed_list.append((road_idx, speed))
    
    return driver_speed_list

def calculate_mean_speeds_along_road(drivers_data, road_centerline_df):
    """
    Calculate mean speeds across all drivers for each road point.
    
    Args:
        drivers_data (list): List of dictionaries, each containing:
                           {'positions': np.array, 'speeds': np.array}
        road_centerline_df (pd.DataFrame): DataFrame with 'x' and 'y' columns
        
    Returns:
        list: List of tuples [(road_point_idx, mean_speed), ...]
    """
    # Process each driver to get their speed associations
    all_driver_speed_lists = []
    
    for driver_data in drivers_data:
        driver_positions = driver_data['positions']
        driver_speeds = driver_data['speeds']
        
        driver_speed_list = process_single_driver(
            driver_positions, driver_speeds, road_centerline_df
        )
        all_driver_speed_lists.append(driver_speed_list)
    
    # Collect speeds for each road point across all drivers
    road_point_speeds = defaultdict(list)
    
    for driver_speed_list in all_driver_speed_lists:
        for road_idx, speed in driver_speed_list:
            road_point_speeds[road_idx].append(speed)
    
    # Calculate mean speeds
    mean_speed_list = []
    for road_idx in sorted(road_point_speeds.keys()):
        speeds = road_point_speeds[road_idx]
        mean_speed = np.mean(speeds)
        mean_speed_list.append((road_idx, mean_speed))
    
    return mean_speed_list

# Example usage:
"""
# Your data structure should look like:
drivers_data = [
    {
        'positions': np.array([[x1, y1], [x2, y2], ...]),  # Nx2 array
        'speeds': np.array([speed1, speed2, ...])          # N-length array
    },
    # ... for each of your 15 drivers
]

road_centerline_df = pd.DataFrame({
    'x': [x1, x2, x3, ...],
    'y': [y1, y2, y3, ...]
})

# Calculate mean speeds
mean_speeds = calculate_mean_speeds_along_road(drivers_data, road_centerline_df)

# Result: [(0, avg_speed_at_point_0), (1, avg_speed_at_point_1), ...]
"""