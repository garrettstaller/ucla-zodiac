# Below are pre-built functions ready to be called from any .ipynb for code cleanliness. 

# --------- Track Selector --------- #
# Grabs a dictionary of data for a specified track, specification made by date. 
# If the boat did not go out that date message will be prompted.
# User may make two logical choices: exclude marina data and exclude nans 

def select_track(date, dictionary, excludenans, excludemdr):
    import numpy as np
    
    # Try/except statment allows for error message regarding 
    # no zodiac data on specified date
    try: 
        specific_track = dictionary[date]
        lat = specific_track['location'][1]
        lon = specific_track['location'][0]
        SST = specific_track['SST']
        flu = specific_track['Flu']
        # Data is confined further to SMB as defined in methods
        lat_min = 33.55
        lat_max = 34.15
        lon_min = -118.85
        lon_max = -118.25
        # BOOLEANS
        SMB_lat = (lat >= lat_min) & (lat <= lat_max)
        SMB_lon = (lon >= lon_min) & (lon <= lon_max)
        # Apply them to location and SST Arrays
        lon = lon[SMB_lon]
        # First normalize the lat array to the present longitudes
        normalized_lat = lat[SMB_lon]
        # Now get proper lats of those with the right longitudes
        lat = normalized_lat[(normalized_lat >= lat_min) & (normalized_lat <= lat_max)]
        # To do spatial data, grab simply using lon
        SST = SST[SMB_lon]
        flu = flu[SMB_lon]
        
        # Remove nans (logical)
        if excludenans == True:
            rmv_nan = (np.isnan(SST) == 0) & (np.isnan(flu) == 0)
            lat = lat[rmv_nan]
            lon = lon[rmv_nan]
            SST = SST[rmv_nan]
            flu = flu[rmv_nan]
            
        # Remove data in marina (logical)
        if excludemdr == True:
            exclude_MDR = ~((lat < 33.983902) & (lat > 33.935) & (lon > -118.48) & (lon < -118.417))
            lat = lat[exclude_MDR]
            lon = lon[exclude_MDR]
            SST = SST[exclude_MDR]
            flu = flu[exclude_MDR]
        
    # If no data is not found for date
    except:
        nodata = dictionary[date]
        
    # returned arrays
    return lat, lon, SST, flu


# --------- General Functions --------- #

# Gradient
def gradient(x, y, lat, lon):
    # X - Distance, Y - distance-dependent DATA, lat & Lon - Respective Processed GPS Locations
    import numpy as np
    # Using the `diff` function, we take the difference between each point
    dy = np.diff(y)
    dx = np.diff(x)
    # Divide to obtain gradient
    gradient = np.abs(dy/dx)
    # Arrays to store values
    midpoint = []
    grad_lat = []
    grad_lon = []
    # The gradient array is n-1 to a length n array, so to graph we simply take the midpoint of the points
    for i in range(len(x) - 1):
        # 1-D track
        x_1 = x[i]  
        x_2 = x[i + 1]
        mid = (x_2 + x_1)/2
        midpoint = np.append(midpoint, mid)
        # Graphical
        lat_1, lat_2 = lat[i], lat[i+1]                                                                                 
        lon_1, lon_2 = lon[i], lon[i+1]
        grad_lat = np.append(grad_lat, (lat_1+lat_2)/2)
        grad_lon = np.append(grad_lon, (lon_1+lon_2)/2)
    return midpoint, gradient, grad_lat, grad_lon

# Distance functions
# find the distace between to geographical points
def distance_formula(x_1, x_2, y_1, y_2):
    import numpy as np
    diff_x = (x_2 - x_1)
    x_distance = diff_x*111.11 # 1 deg. lat = 111.11 km
    diff_y = (y_2 - y_1)
    y_distance = diff_y*92 # 1 deg. lon = 92 km, at this latitude
    result = np.sqrt((x_distance)**2 + (y_distance)**2)
    return result
# Utilize above function to create an array of distances from cruise coords
def calc_distance(lat, lon):
    import numpy as np
    distance = [0]
    for i in range(len(lat) - 1):
        x_1 = lat[i]
        x_2 = lat[i + 1]
        y_1 = lon[i]
        y_2 = lon[i + 1]
        r = distance_formula(x_1, x_2, y_1, y_2)
        cumulative = distance[i] + r
        distance = np.append(distance, cumulative)
    return distance

# Beaing functions 
# Create array of boat heading w/ distance 
def bearing(lat, lon):
    import math
    import numpy as np
    bearings = [0]
    for i in range(len(lat)-1):
        lat1, long1, lat2, long2 = lat[i], lon[i], lat[i+1], lon[i+1]
        # Convert latitude and longitude to radians
        lat1 = math.radians(lat1)
        long1 = math.radians(long1)
        lat2 = math.radians(lat2)
        long2 = math.radians(long2)
        # Calculate the bearing
        bearing = math.atan2(math.sin(long2 - long1) * math.cos(lat2),
                             math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(long2 - long1))
        # Convert the bearing to degrees
        bearing = math.degrees(bearing)
        # Make sure the bearing is positive
        bearing = (bearing + 360) % 360
        bearing = int(bearing)
        # add to array...
        bearings = np.append(bearings, bearing)
    return bearings

# Subset Function
# Takes in data and compares it to an existing array to check for duplicates

# --------- Data Processing --------- #

def data_processing(lat, lon, c, window): # change c and windowsize accordingly - recommended window size for sst = 10 
    import numpy as np
    distance = calc_distance(lat, lon) # Calls upon distance function from ZF.py file
    failed_series = []
    # First segment our distance array so that we have a point every 10 meters from the start to the end
    dist_spaced = np.arange(min(distance), max(distance), .01)
    # The windowsize will determine the number of points we span in our running average, mutliply this by the 10 meters 
    # to understand our window in terms of distance, and not just the number of points.
    window_size = window
    # Start will be used for indexing in our loop, its initial value is 0, and is thus set to that prior to loop
    start = 0
    # The following are arrays that will hold our evenly spaced and smoothed data, as well as some of its stats. 
    c_processed, dist_processed = [], []
    # Loop will run from start of our data set to just a window size below it, otherwise we will get a run time error in indexing
    for i in range(len(dist_spaced) - window_size):
        try:
            # set up latter bound of index
            end = start + window_size
            # Index from start, 0 at i = 1 or x based on ith, to the end, start plus our window
            distance_bounds = dist_spaced[start:end+1] # we add 1 as indexing is naturally non-inclusive
            start = i+1 # Just add one to our index so that we shift the moving average by 1 pt. or 10 meters each time 
            # With C DATA of the desired window selected, take all within these bounds 
            C_bounds = (c[(distance > distance_bounds[0]) & (distance < distance_bounds[-1])])
            # With ONLY the C DATA within selected bounds, take average and add it as processed data 
            c_processed = np.append(c_processed, sum(C_bounds)/len(C_bounds))
            # We will take the median, or center, of this data to be the corresponding distance point 
            dist_processed = np.append(dist_processed, np.median(distance_bounds))
        except:
            failed_series = np.append(failed_series, distance_bounds)
        continue
    return dist_processed, c_processed

def running_avg_filter(window_size, lat, lon, c_processed, dist_processed):
    import numpy as np
    distance = calc_distance(lat, lon)
    failed_series = []
    # The windowsize will determine the number of points we span in our running average, mutliply this by the 10 meters 
    # to understand our window in terms of distance, and not just the number of points.
    # Start will be used for indexing in our loop, its initial value is 0, and is thus set to that prior to loop
    start = 0
    # The following are arrays that will hold our evenly spaced and smoothed data, as well as some of its stats. 
    c_filtered, dist_filtered = [], []
    # Loop will run from start of our data set to just a window size below it, otherwise we will get a run time error in indexing
    for i in range(len(dist_processed) - window_size):
        try:
            # set up latter bound of index
            end = start + window_size
            # Index from start, 0 at i = 1 or x based on ith, to the end, start plus our window
            distance_bounds = dist_processed[start:end+1] # we add 1 as indexing is naturally non-inclusive
            start = i+1 # Just add one to our index so that we shift the moving average by 1 pt. or 10 meters each time 
            # With C DATA  of the desired window selected, take all within these bounds 
            C_bounds = c_processed[start:end+1]
            c_filtered = np.append(c_filtered, sum(C_bounds)/len(C_bounds))
            dist_filtered = np.append(dist_filtered, np.median(distance_bounds))
        except:
            failed_series = np.append(failed_series, distance_bounds)
        continue
    interpolated_lat, interpolated_lon = np.interp(dist_filtered, distance, lat), np.interp(dist_filtered, distance, lon)
    ### Now we calculate the Gradients ###
    grad_dist, grad_mag, grad_lat, grad_lon = gradient(dist_filtered, c_filtered, interpolated_lat, interpolated_lon)
    return grad_dist, grad_mag, interpolated_lat, interpolated_lon, c_filtered, dist_filtered
