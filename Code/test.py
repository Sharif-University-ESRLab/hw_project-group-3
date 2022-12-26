
def get_coordinates_manual(start_lat=35.703129, start_long=51.351671, direction='N'):
    curr_latitude = start_lat
    curr_longitude = start_long

    step = 0.001

    if direction == 'N':
        curr_latitude += step
    elif direction == 'S':
        curr_latitude -= step
    elif direction == 'E':
        curr_longitude += step
    else:
        curr_longitude -= step

    return start_lat, start_long, curr_latitude, curr_longitude

        


if __name__ == "__main__":
    while True:
        coordinates = get_coordinates_manual()
        for c in coordinates:
            new_latitude, new_longitude = c[0], c[1]
            print(new_latitude, new_longitude)




