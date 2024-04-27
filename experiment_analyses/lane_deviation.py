import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from scipy.interpolate import CubicSpline,CubicHermiteSpline,UnivariateSpline,PchipInterpolator
from numpy import diff
import numpy as np
import scipy
import parse_path_center_csv

left_turn_short_df = parse_path_center_csv.left_turn_short_df

def get_track_piece_indices(track_piece,center_of_road_map1):
    indices_for_track_piece = list(center_of_road_map1.index[center_of_road_map1['Road_Name'].str.contains(track_piece)])
    track_piece_center_of_road_map1 = center_of_road_map1[center_of_road_map1['Road_Name'].str.contains(track_piece)]
    return(indices_for_track_piece,track_piece_center_of_road_map1)

def get_center_of_lane_per_track_piece(center_of_road_map1):
    track_pieces = sorted((list(set(center_of_road_map1["Road_Name"]))))
    dict_of_track_piece_dfs = {}
    for i in range(0,len(track_pieces)):
        indices_for_track_piece,track_piece_center_of_road_map1 = get_track_piece_indices(track_pieces[i],center_of_road_map1)
        dict_of_track_piece_dfs[track_pieces[i]] = {"map_1":track_piece_center_of_road_map1}
    return(track_pieces,dict_of_track_piece_dfs)

def fit_smoothing_spline(x, z, dzdx):
    #orig_xz = (x,z)
    #indx = np.argsort(x)
    #x = x[indx]
    #z = z[indx]

    # spline = UnivariateSpline(x, z)
    # spline = CubicHermiteSpline(x, z, dzdx)
    # spline = PchipInterpolator(x, z)
    #spline = CubicSpline(x, z)
    #xs = np.linspace(x.min(), x.max(), 1000)
    #print("YO BITCH")
    #print(type(spline))

    #x = x.sort()
    #z = z.sort()
    #from IPython import embed; embed()
    #spline = PchipInterpolator(x,z)
    #from IPython import embed; embed()
    #zs = spline[1]
    #print(xs)
    #print(zs)
    from IPython import embed; embed()
    splines = scipy.interpolate.splrep(x,z,k=3)
    #return xs, zs


x = left_turn_short_df["x"].to_numpy()
z = left_turn_short_df["z"].to_numpy()
x = x.astype(float)
z = z.astype(float)

# resolution = 1000  # Number of points to generate
# x_new = np.linspace(x.min(), x.max(), resolution)
# z_new = np.interp(x_new, x, z)

# dzdx = diff(z)/diff(x)
# dzdx= np.insert(dzdx,0,0)

dzdx = np.gradient(x, z) 
# u_turn_log_df['der'] = dzdx
# u_turn_log_df['der'] = u_turn_log_df['der'].rolling(window=2).mean()
# dzdx = u_turn_log_df["der"].to_numpy()
# dzdx = np.nan_to_num(dzdx)

xs, zs = fit_smoothing_spline(x, z, dzdx)

plt.plot(x, z, c = "red")
#plt.plot(x_new, z_new, c = "green")
plt.plot(xs, zs, c = "blue")
plt.show()