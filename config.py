from locdatalib import Place


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

    global JACKSON_AVE; JACKSON_AVE = Place('Hob Nob', 407726090, -1119122010, .1)
    global UOFU_ENGINEERING; UOFU_ENGINEERING = Place('Engineering Complex U of U', 407680590, -1118455290, .2)
    global MARRIOTT_LIBRARY; MARRIOTT_LIBRARY = Place('Marriott Library', 407623600, -11184612320, .2)
    global JACKSON_MCDONALDS; JACKSON_MCDONALDS = Place("Jackson McDonald's", 407717700, -1119185740, .05)
    global PORCH_FINANCIAL; PORCH_FINANCIAL = Place('Porch Financial', 405698320, -1118944310, .5)