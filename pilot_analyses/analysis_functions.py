import math
import numpy as np

# function for calculating speed
speed = lambda x,y,z: math.sqrt(x*x + y*y + z*z)

# function to map steering inputs/angle
map_to_steering_angle = lambda input,input_start,input_end,output_start,output_end: output_start + ((output_end - output_start) / (input_end - input_start)) * (input - input_start)

# use for main experiment -- useless for pilot data :(
def get_speed_per_frame(driving_vars_df):
    velocity_x = list(driving_vars_df["velocity_x"])
    velocity_y = list(driving_vars_df["velocity_y"])
    velocity_z = list(driving_vars_df["velocity_z"])

    speed_array = []
    
    for i in range(0,len(velocity_x)):
        x,y,z = velocity_x[i],velocity_y[i],velocity_z[i]
        current_speed = speed(x,y,z)
        speed_array.append(current_speed)
    
    driving_vars_df['speed'] = speed_array
    return(driving_vars_df)

# use solely for pilot data/power analysis!
def get_speed_via_pos(cam_position_df):
    pos_x_list = list(cam_position_df["pos_x"])
    pos_y_list = list(cam_position_df["pos_y"])
    pos_z_list = list(cam_position_df["pos_z"])

    speed_array = []

    #for i in range(0,len(pos_x_list)):
    for i in range(0,len(pos_x_list)):
        t1_pos_x,t1_pos_y,t1_pos_z = pos_x_list[i],pos_y_list[i],pos_z_list[i]
        t1 = cam_position_df.iloc[i]["time"]

        if i == 0:
            t0_pos_x,t0_pos_y,t0_pos_z = t1_pos_x,t1_pos_y,t1_pos_z
            t0 = t1
        else:
            t0_pos_x,t0_pos_y,t0_pos_z = pos_x_list[i-1],pos_y_list[i-1],pos_z_list[i-1]
            t0 = cam_position_df.iloc[i-1]["time"]

        delta_t = 1/30 # simulation is constrained to 30HZ
        x_component = abs(t1_pos_x - t0_pos_x)/delta_t
        y_component = abs(t1_pos_y - t0_pos_y)/delta_t
        z_component = abs(t1_pos_z - t0_pos_z)/delta_t
        current_speed = speed(x_component,y_component,z_component)
        speed_array.append(current_speed)
    
    cam_position_df['speed'] = speed_array
    return(cam_position_df)


def replace_over_30(data):
    for i, value in enumerate(data):
        if value > 30:
            data[i] = 30
    return data


def replace_if_diff_greater_than_10(data):
    for i in range(1, len(data)):
        prev = data[i-1] 
        current = data[i]
        diff = current - prev
        
        if abs(diff) > 5:
            data[i] = prev
            
    return data

def convert_steering_value(driving_vars_df):
    input_start, input_end = -1,1
    output_start,output_end = -35,35
    # take steering input and convert from -1 to 1 --> 0 --> 35 degrees
    steering_array = driving_vars_df['steering_angle']
    steering_angle_array = []
    for i in range(0,len(steering_array)):
        current_steering_input = steering_array[i]
        steering_angle = round(map_to_steering_angle(current_steering_input,input_start,input_end,output_start,output_end),3)
        steering_angle_array.append(steering_angle)
    driving_vars_df['steering_angle_transformed'] = steering_angle_array
    return(driving_vars_df)






