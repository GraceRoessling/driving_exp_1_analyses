# Preprocess the dataframes for analysis 


# Acquire the following metrics ========================================================================

## Lap Time
get_lap_time <- function(df){
  first_time <- df$time[1]
  last_time <- df$time[length(df$time)]
  total_lap_time_sec <- last_time - first_time
  return(total_lap_time_sec)
}

## Speed, speed variance
get_speed_mean <- function(df){
  data_column <- df$smooth_speed
  smooth_speed_mean <- mean(data_column)
  return(smooth_speed_mean)
}

get_speed_variance <- function(df){
  data_column <- df$smooth_speed
  smooth_speed_var <- var(data_column)
  return(smooth_speed_var)
}

## Steering, steering variance
get_steering_mean <- function(df){
  data_column <- df$steering_angle_transformed
  steering_mean <- mean(data_column)
  return(steering_mean)
}

get_steering_variance <- function(df){
  data_column <- df$steering_angle_transformed
  steering_var <- var(data_column)
  return(steering_var)
}

get_min_speed <- function(df){
  data_column <- df$smooth_speed
  speed_min <- min(data_column)
  return(speed_min)
  
}

get_max_speed <- function(df){
  data_column <- df$smooth_speed
  speed_max <- max(data_column)
  return(speed_max)
  
}

get_min_steering <- function(df){
  data_column <- df$steering_angle_transformed
  steering_min <- min(data_column)
  return(steering_min)
  
}

get_max_steering <- function(df){
  data_column <- df$steering_angle_transformed
  steering_max <- max(data_column)
  return(steering_max)
  
}

get_statistics_per_subject <- function(cam_pos,drive_vars){
  # lap time
  total_time = get_lap_time(drive_vars)
  
  # speed mean/variance
  smooth_speed_mean = get_speed_mean(cam_pos)
  smooth_speed_variance = get_speed_variance(cam_pos)
  
  # speed min/max
  max_speed = get_max_speed(cam_pos)
  min_speed = get_min_speed(cam_pos)
  
  # steering mean/variance
  steering_mean = get_steering_mean(drive_vars)
  steering_variance = get_steering_variance(drive_vars)
  
  # steering angle min/max
  max_steering = get_max_steering(drive_vars)
  min_steering = get_min_steering(drive_vars)
  
  # Report results
  print(paste("Total Time:",total_time))
  
  print(paste("Mean & Variance of Speed (meters/sec) :",smooth_speed_mean,smooth_speed_variance))
  print(paste("Min & Max Speed (meters/sec) :", min_speed,max_speed))
  
  print(paste("Mean & Variance of Steering Angle (degrees)",steering_mean,steering_variance))
  print(paste("Min & Max Steering Angle (degrees) :", min_steering,max_steering))
}

## Visualize trajectories without nodes (simply use location) -- color coded with speed


## acquire mean position and calculate deviation relative to mean to get FISB!


# =======================================================================================================

