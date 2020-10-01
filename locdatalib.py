#############################################################################
# A set of functions used for data analysis on Google Takout location data
#############################################################################
import json

def miles_to_degrees(miles):
    '''
    Returns miles in degrees latitude/longitude e7

    miles -- (int) miles
    '''
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


def get_locations(filepath):
    '''
    Returns a list of a list of dictionaries that represents Google Takeout location data

    filepath -- (string) the path of the JSON file containing Google Takeout location data 
    '''
    with open(filepath) as f:
        return json.load(f)['locations']

def is_within_location_range(loc_lat, loc_long, latitude_e7, longitude_e7, epsilon):
    '''
    Returns True if the given desired location is within epsilon of the actual location

    loc_lat -- (float) the desired latitude in e7
    loc_long -- (float) the desired longitude in e7
    latitude_e7 -- (float) the actual latitude in e7
    longitude_e7 -- (float) the actual longitude in e7
    epsilon -- (float) degrees of freedom in degrees latitude/longitude e7
    '''
    return abs(loc_lat - latitude_e7) <= epsilon and abs(loc_long - longitude_e7) <= epsilon

def len_of_time_with_epsilon_of_coord_on_time_interval(place, start_time, end_time, location_entries):
    '''
    Returns a float representing the number of hours spent at the specified place on the closed interval [start_time, end_time].

    # TODO: change epsilon to calculating within a radius instead of a square

    place -- (Place) represents a place
    start_time -- (datetime) The start time of the interval
    end_time -- (datetime) The end time of the interval. Structure defined by google location data.
    '''
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

    return convert_ms_to_hours(float(sum_time_at_location))

def calc_hours_from_list_of_places(places, start_time, end_time, location_entries):
    '''
    Returns a list of the times (floats) spents in each place of interest

    places -- (list of Places) places of interest
    start_time -- (datetime) the start time of the interval
    end_time -- (datetime) the end time of the interval
    location_entries -- (list of a list of dictionaries) represents Google Takeout location data
    '''
    return [len_of_time_with_epsilon_of_coord_on_time_interval(elem, start_time, end_time, location_entries) for elem in places]

def convert_ms_to_hours(ms):
    '''
    Return ms in hours

    ms -- (float) time in miliseconds
    '''
    return ((ms / 1000) / 60) / 60

def calc_other_and_unsure_time(time_spent_in_places_of_interest, location_entries, start_time, end_time):
    '''
    Returns the total time that is unnaccounted for by time_spent_in_places_of_interest

    time_spent_in_places_of_interest -- (list of floats) times spent in places of interest
    location_entries -- (list of a list of dictionaries) represents Google Takeout location data
    start_time -- (datetime) the start time of the interval
    end_time -- (datetime) the end time of the interval
    '''
    other_time = get_total_time_on_interval(start_time, end_time)
    for time in time_spent_in_places_of_interest:  # Subtract times for places of interest from other_time
        other_time = other_time - time
    return other_time

def get_total_time_on_interval(start_time, end_time):
    '''
    Returns a float representing the total amount of time on the interval

    start_time -- (datetime) the start time of the interval
    end_time -- (datetime) the end time of the interval
    '''
    last_time = end_time.timestamp() * 1000
    first_time = start_time.timestamp() * 1000
    return ((((last_time - first_time) / 1000) / 60) / 60)