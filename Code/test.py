
# function for generating manual coordinates
# direction: one of 8 directions => N,S,E,W,NE,NW,SE,SW
def get_coordinates_manual(start_lat=35.703129, start_long=51.351671, direction='N', step=0.001):
    curr_latitude = start_lat
    curr_longitude = start_long

    if direction == 'N':
        curr_latitude += step
    elif direction == 'S':
        curr_latitude -= step
    elif direction == 'E':
        curr_longitude += step
    elif direction == 'W':
        curr_longitude -= step
    elif direction == "NE":
        curr_latitude += step
        curr_longitude += step
    elif direction == "NW":
        curr_latitude += step
        curr_longitude -= step
    elif direction == "SE":
        curr_latitude -= step
        curr_longitude += step
    else:
        curr_latitude -= step
        curr_longitude -= step

    return start_lat, start_long, curr_latitude, curr_longitude





