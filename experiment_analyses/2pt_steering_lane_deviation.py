import numpy as np
import matplotlib.pyplot as plt
import calculate_parallel_curves
import math

# GET NUMBER OF FRAMES FROM INPUT FILE (CAN'T JUST GRAB IT AUTOMATICALLY DUE TO CIRCULARITY)
number_of_frames = 120 # maybe new batch script can deal with this issue...

# All distances in meters ==============================================================================================
firstStraightPathLength = 6
arcLength = 76.6 # if trial is 6 seconds long, and speed is 13.8m/s, then arc length is 82.8m-6m
lastStraightPathLength = 20

roadWidth = 3
centerCircleRadius = 60 
insideCircleRadius = centerCircleRadius - (roadWidth/2) # 60 - 1.5m 
outsideCircleRadius = centerCircleRadius + (roadWidth/2) # 60 + 1.5m

arcLengthAngle = (arcLength * 360) / (2*np.pi*centerCircleRadius) # if r = 60 and s = 76.6, then theta = 73.148 degrees

# Road resolutions
firstStraightResolution,arcResolution,lastStraightResolution = calculate_parallel_curves.calculate_path_segment_resolution(firstStraightPathLength,arcLength,lastStraightPathLength,number_of_frames)

arcThetaArray = np.linspace(0,arcLength,arcResolution)

# ======================================================================================================================
# Utility Functions
  # Generate degree list (based on arc length) for functions to loop through
def calculate_xy_for_arc(theta_array,radius,roadWidth,path_side):
  x_array,y_array = [],[]
  for i in range(0,len(theta_array)):
    theta = np.radians(arcThetaArray[i])
    x = radius * np.sin(theta)
    y = (radius * np.cos(theta)) - radius
    x_array.append(x)
    y_array.append(y)
  
  halfWidth = roadWidth/2
  shift_down = lambda y,halfWidth: y - halfWidth
  shift_up = lambda y,halfWidth: y + halfWidth
  roadWidth_array = [halfWidth]*len(y_array) # map function needs an array to iterate through all function arguments

  if path_side == "outside":
    transformed_y_array = list(map(shift_up,y_array,roadWidth_array))
  elif path_side == "inside":
    transformed_y_array = list(map(shift_down,y_array,roadWidth_array))
  else:
    transformed_y_array = y_array
  return(x_array,transformed_y_array)

def calculate_endpoint_for_tangentLine(length_of_tangentLine,arcLast_x, arcLast_y, number_of_frames,y_function,tangentSlope,tangent_y_intercept):
    last_arc_coordinates = arcLast_x, arcLast_y
    x_array = np.linspace(last_arc_coordinates[0],number_of_frames,number_of_frames)
    x_values_near_distance = []
    for i in range(0,number_of_frames):
      current_x = x_array[i]
      current_y = y_function(tangentSlope,current_x,tangent_y_intercept)
      x_values_near_distance.append(current_x)

      current_coordinates = current_x, current_y
      distance_between_arc_and_last_tangent_coordinate = math.dist(last_arc_coordinates,current_coordinates)
      if distance_between_arc_and_last_tangent_coordinate > length_of_tangentLine:
        break

    endpoint_x = x_values_near_distance[-2]
    return(endpoint_x)

  # Generate x,y list for tangent line
def calculate_xy_for_line(arcLast_x,arcLast_y,tagentSlope,tangent_yIntercept,y_function,lastStraightResolution,path_side,number_of_frames):
  endpoint_x = int(calculate_endpoint_for_tangentLine(lastStraightPathLength,arcLast_x, arcLast_y,number_of_frames,y_function,tagentSlope,tangent_yIntercept)  )
  x_array = np.linspace(arcLast_x,endpoint_x,lastStraightResolution)

  y_array = []
  for i in range(0,len(x_array)):
    current_x = x_array[i]
    current_y = y_function(tagentSlope,current_x,tangent_yIntercept)
    y_array.append(current_y)

  return(x_array,y_array)

# ==============================================================================================================================
# Generate line 
def generate_path(arcThetaArray,arcRadius,path_side):
  # Calculate curved road
  center_x_array,center_y_array = calculate_xy_for_arc(arcThetaArray,arcRadius,roadWidth,path_side)

  # Calculate first straight 6 meters
  arcInitial_x, arcInitial_y = center_x_array[0],center_y_array[0]
  startingPoint_x, startingPoint_y = arcInitial_x - firstStraightPathLength, arcInitial_y

  initial_straight_x_array = np.linspace(startingPoint_x,arcInitial_x,firstStraightResolution)
  halfWidth = roadWidth/2

  if path_side == "outside":
    initial_straight_y_array = [halfWidth]*len(initial_straight_x_array)
  elif path_side == "inside":
    initial_straight_y_array = [-1*halfWidth]*len(initial_straight_x_array)
  elif path_side == "center":
    initial_straight_y_array = np.zeros(len(initial_straight_x_array))

  # Calculate last straight ~6 meters
  arcLast_x, arcLast_y = center_x_array[-1],center_y_array[-1]
  tagentSlope = -arcLast_x/(arcLast_y + arcRadius)
  tangent_yIntercept = arcLast_y - (tagentSlope*arcLast_x)

  y_function = lambda m,x,b: m*x+b
  last_straight_x_array,last_straight_y_array = calculate_xy_for_line(arcLast_x,arcLast_y,tagentSlope,tangent_yIntercept,y_function,lastStraightResolution,path_side, number_of_frames)

  return(initial_straight_x_array,initial_straight_y_array,center_x_array,center_y_array,last_straight_x_array,last_straight_y_array)

# ============================================================================================================================================
# Center path
center_initial_straight_x_array,center_initial_straight_y_array,center_curve_x_array,center_curve_y_array,center_last_straight_x_array,center_last_straight_y_array = generate_path(arcThetaArray,centerCircleRadius,"center")
center_x_array_separate_parts = center_initial_straight_x_array,center_curve_x_array,center_last_straight_x_array
center_y_array_seperat_parts = center_initial_straight_y_array,center_curve_y_array,center_last_straight_y_array

# Calculate segmented outside curves
first_straight_outside_x_array,first_straight_outside_y_array,first_straight_inside_x_array,first_straight_inside_y_array = calculate_parallel_curves.calc_parallel_curve(center_x_array_separate_parts[0],center_y_array_seperat_parts[0],roadWidth/2)
middle_curved_outside_x_array,middle_curved_outside_y_array,middle_curved_inside_x_array,middle_curved_inside_y_array = calculate_parallel_curves.calc_parallel_curve(center_x_array_separate_parts[1],center_y_array_seperat_parts[1],roadWidth/2)
last_straight_outside_x_array,last_straight_outside_y_array,last_straight_inside_x_array,last_straight_inside_y_array = calculate_parallel_curves.calc_parallel_curve(center_x_array_separate_parts[2],center_y_array_seperat_parts[2],roadWidth/2)

# Outside path
outside_x_array_seperate_parts = first_straight_outside_x_array,middle_curved_outside_x_array,last_straight_outside_x_array
outside_y_array_separate_parts = first_straight_outside_y_array,middle_curved_outside_y_array,last_straight_outside_y_array

# Inside path
inside_x_array_separate_parts = first_straight_inside_x_array,middle_curved_inside_x_array,last_straight_inside_x_array
inside_y_array_separate_parts = first_straight_inside_y_array,middle_curved_inside_y_array,last_straight_inside_y_array

#  stitch together all three arrays for single center line (to guide agent)
center_x_array = np.concatenate((center_initial_straight_x_array,center_curve_x_array,center_last_straight_x_array),axis=None)
center_y_array = np.concatenate((center_initial_straight_y_array,center_curve_y_array,center_last_straight_y_array),axis=None)
outside_x_array,outside_y_array,inside_x_array,inside_y_array = calculate_parallel_curves.calc_parallel_curve(center_x_array,center_y_array,roadWidth/2)


# center_arc = plt.plot(center_x_array,center_y_array,c='yellow',ls='--')

# # Outside path
# outside_last_straight = plt.plot(outside_x_array,outside_y_array,c='black')

# # Inside
# inside_last_straight = plt.plot(inside_x_array,inside_y_array,c='black')

# print(np.shape(center_x_arrays))
# print(center_x_arrays[0])
#print(center_y_arrays)_

