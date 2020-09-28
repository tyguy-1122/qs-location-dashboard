import json

def miles_to_degrees(miles):
    #TODO: reevaluate the precision of this operation (conversion varies with degrees latitude)
    return (miles / 69) * 1e7

class Place:
        def __init__(self, name, latitude, longitude, epsilon):
            '''
            name -- (string) name of the location
            latitude -- (int) degrees latitude at the center of the location * e7
            longitude -- (int) degree longitude at the center of the location * e7
            epsilon -- (int) margin of error in miles
            '''
            self.name = name
            self.latitude = latitude
            self.longitude = longitude
            self.epsilon = miles_to_degrees(epsilon)


def get_locations(filename):
    with open(filename) as f:
        return json.load(f)['locations']

def is_within_location_range(loc_lat, loc_long, latitude_e7, longitude_e7, epsilon):
    return abs(loc_lat - latitude_e7) <= epsilon and abs(loc_long - longitude_e7) <= epsilon

def len_of_time_with_epsilon_of_coord_on_time_interval(place, start_time, end_time, location_entries):
    """
    Returns a float representing the number of hours spent at the specified place on the closed interval [start_time, end_time].

    # TODO: change epsilon to calculating within a radius instead of a square

    place -- (Place) represents a place
    start_time -- (datetime) The start time of the interval
    end_time -- (datetime) The end time of the interval. Structure defined by google location data.
    """
    start_time_ms = start_time.timestamp() * 1000
    end_time_ms = end_time.timestamp() * 1000
    index_start_at_loc = None
    at_loc = False
    sum_time_at_location = 0

    for i in range(len(location_entries)):
        # We don't care about any data passed end_time
        if int(location_entries[i]['timestampMs']) >= end_time_ms:
            break
        # Works on data that is between start_time and end_time, summing up contiguous time periods spent at the desired location
        if int(location_entries[i]['timestampMs']) >= start_time_ms:

            if is_within_location_range(place.latitude, place.longitude, location_entries[i]['latitudeE7'],
             location_entries[i]['longitudeE7'], place.epsilon) and not at_loc:
                at_loc = True
                index_start_at_loc = i

            elif not is_within_location_range(place.latitude, place.longitude,location_entries[i]['latitudeE7'],
             location_entries[i]['longitudeE7'], place.epsilon) and at_loc: 
                at_loc = False
                sum_time_at_location += int(location_entries[i-1]['timestampMs']) - int(location_entries[index_start_at_loc]['timestampMs'])

    return ((float(sum_time_at_location) / 1000) / 60) / 60