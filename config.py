################################################################
# Declares global variables to be used for data analysis on
# Google Takeout location data
#
# ---Change theses variables to run analysis on your own data
# ---You will need to download your own location data from
#    Google Takeout at https://takeout.google.com/
# ---See locdatalib.py for the definition of the Place class
#################################################################
from locdatalib import Place
from datetime import datetime


def init():
    """
    This function is called to initialize values of global config variables.
    """

    #----------------------------------------
    # Google Takeout location service files
    #----------------------------------------
    
    global LOC_FILEPATH; LOC_FILEPATH = '/home/tyguy1122/google_location_data/google_location_data_at_2020-09/Takeout/Location History/Location History.json'

    #----------------------------------------
    # Places
    #----------------------------------------

    global MY_PLACES
    MY_PLACES = [
    Place('Hob Nob', 407726090, -1119122010, .1),
    Place('Engineering Complex U of U', 407680590, -1118455290, .2),
    Place('Marriott Library', 407623600, -11184612320, .2),
    Place("Jackson McDonald's", 407717700, -1119185740, .05),
    Place('Porch Financial', 405698320, -1118944310, .5)
    ]

    #-----------------------------------------
    # Time interval of concern
    #-----------------------------------------

    global START_TIME; START_TIME = datetime(2019, 11, 18)
    global END_TIME; END_TIME = datetime(2019, 11, 22)