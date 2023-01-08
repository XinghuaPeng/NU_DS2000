""" Xinghua Peng
    DS 2000: Intro to Programming with Data
    Homework 7
    Nov 4, 2022
    File: bluebikes.py
    Description: A program to analyze blue bikes in the city of Boston ranging
    from Sept 23-30th: visualize the distribution of distances and speeds for
    the trips; maps day of the week to the count of trips associated with that
    day of the week regarding those ending station at NEU/"Forsyth St. at Huntington Ave".
    
    Program Output: 
    Number of trips ending at Forsyth st at Huntington Ave:
    Friday: 481
    Saturday: 230
    Sunday: 219
    Monday: 250
    Tuesday: 314
    Wednesday: 296
    Thursday: 277
        

"""
# Import package as needed
# I directly use the code from dataproc.py as stated in Piazza instead of importing
import matplotlib.pyplot as plt
import math

# Define constants
# in miles
EARTH_RADIUS = 3959

# Define constant to make it easier if I need to switch filename for testing purposes
BLUE_BIKES_FILE = "trips.csv"
STATIONS_FILE = "stations.csv"
NEU_STATION = "Forsyth St at Huntington Ave"

# Define a collection of functions & Code in a modular style
def read_data(trips_filename, stations_filename):
    """ Reads blue bikes trips data into a list of dictionaries
    and reads blue bikes stations data into a seperate dictionary. 
    trips_filename - datafile that contains all blue bikes trips in the last week of September
    stations_filename - datafile that maps stations names to the GPS coordinates (latitude, longitude)
    return - a list of dictionaries & a seperate dictionary according to the prompt
    *key: column headers & values: values for the corresponding row
    """
    # Load the trips file
    trips = []
    coltypes = [int, int, str, str, str, int]

    with open(trips_filename, "r") as infile:

        # Read the header
        header = infile.readline().strip().split(",")

        # read remaining lines
        for line in infile:
            rowdict = {}

            # parse the values
            vals = line.strip().split(",")

            # store the key-value pairs
            for i in range(len(vals)):
                key = header[i]
                value = vals[i]
                if value != "":  # value is not missing
                    value = coltypes[i](value)
                rowdict[key] = value

            trips.append(rowdict)

    # Read the stations file
    stations = {}

    with open(stations_filename, "r") as infile:

        # Read the header
        infile.readline()

        # read remaining lines
        for line in infile:
            # parse the values
            vals = line.strip().split(',')

            # store the key-value pairs
            key = vals[0]
            value = [float(vals[1]), float(vals[2])]
            stations[key] = value

    return trips, stations


def extract_column(data, column):
    """ Extracts a column of data from a table
    data - list of lists / full dataset as a 2d list
    column - column index/column name to be extracted
    return - list of values for all rows for the target column
    """
    col = []
    for row in data:
        col.append(row[column])

    return col


def haversine_distance(start, end):
    """ Calculates the distance in miles between two points on the earth's surface
    described by latitude and longitude.
    start - list of two floats—latitude and longitude
    end - list of two floats—latitude and longitude
    return - float - distance in miles between the two points
    """
    lat1 = start[0]
    long1 = start[1]
    lat2 = end[0]
    long2 = end[1]
    lat1 = math.radians(lat1)
    long1 = math.radians(long1)
    lat2 = math.radians(lat2)
    long2 = math.radians(long2)
    delta_lat = lat2 - lat1
    delta_long = long2 - long1
    # the earth's radius is a constant value
    a = math.sin(delta_lat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(delta_long / 2)**2
    haversine = EARTH_RADIUS * 2 * math.asin(math.sqrt(a))
    
    return haversine


def calculate_the_distance_and_speed(trips, stations):
    """ Uses the haversine distance function to calculate the distances between stations
    and filll in a special value "None" for stations in certain trips
    trips - a list of dictionaries with the trips dataset
    stations - a seperate dictionary with the stations dataset
    return - an updated list of dictionaries with the trips dataset
    """
    for t in trips:

        start = ''
        end = ''
        start_station = t['start_station']
        end_station = t['end_station']

        if start_station in stations:
            start = stations[t['start_station']]
        if end_station in stations:
            end = stations[t['end_station']]
        # Filling in a special value "None" if the trips assocaited with stations are not in the file
        if start != '' and end != '':
            dist = haversine_distance(start, end)
            mph = dist / (t['duration'] / 3600)
        else:
            dist = None
            mph = None

        t['dist'] = dist
        t['mph'] = mph

    return trips


def distance_and_speed_visualize(data):
    """ Creates two well-labeled histograms for distribution of distances and 
    speeds for the trips
    data - an updated/cleaned list of dictionaries with the trips dataset
    return - nothing
    """
    clean_data = []
    # Filter data 
    for i in data:
        if i["dist"] != None and i["mph"] != None:
            clean_data.append(i)

    # Retrieve the data
    distances = extract_column(clean_data, "dist")
    speeds = extract_column(clean_data, "mph")

    # Visualize the distance for the trips
    plt.hist(distances, bins=100, color='yellowgreen', edgecolor='palegreen', alpha=0.8)

    # Label the axes and set the title
    plt.title("Distribution of Distances for Trips")
    plt.xlabel("Distance")
    plt.ylabel("Frequency")
    plt.savefig("distances.pdf")
    plt.show()

    # Visualize the speed for the trips
    plt.hist(speeds, bins=100, color='steelblue', edgecolor='steelblue', alpha=0.8)
    # Label the axes and set the title
    plt.title("Distribution of Speeds for Trips")
    plt.xlabel("Speed (mph)")
    plt.ylabel("Frequency")
    plt.savefig("speeds.pdf")
    plt.show()


def count_of_trips(data, end):
    """ Creates a dictinary that maps day of the week to the count of trips associated
    with that day of the week & print a report displaying these counts
    data - an updated/cleaned list of dictionaries with the trips dataset
    end - 
    """
    output = {}
    for i in data:
        if i['end_station'] == end:
            day = i['start_day_name']
            if day in output:
                output[day] = output[day] + 1
            else:
                output[day] = 1

    # Print the report
    print("Number of trips ending at Forsyth st at Huntington Ave:")
    for key in output:
        print(key + ':', output[key])


def visualization(trips, stations, bike_id=2010):
    """ Depicts the voyage of a single bike (at least 50 trips) throughout 
    late Sept 2022 including the physical locations of each start/end station
    trips - a list of dictionaries with the trips dataset
    stations - a seperate dictionary with the stations dataset
    bike_id - identification number for the corresponding blue bike to analyze
    """

    # Create a canvas and set the size and title
    plt.figure(figsize=(12,8), dpi = 500)
    plt.title("The Voyage of Blue Bike " + str(bike_id) + 
              " throughout the Course of Late September 2022")

    # Find bike data
    count = 0  # Record number of trips
    allstation = {}  # Coordinates of the experienced station
    voyage = {}  # Daily itinerary
    for i in trips:
        if i['bike_id'] == bike_id:
            start = ''
            end = ''
            start_station = i['start_station']
            end_station = i['end_station']
            if start_station in stations:
                start = stations[i['start_station']]
            if end_station in stations:
                end = stations[i['end_station']]
            if start != '' and end != '':
                count = count + 1
                if start_station not in allstation:
                    allstation[start_station] = start
                if end_station not in allstation:
                    allstation[end_station] = end
                if i['start_day'] not in voyage:
                    voyage[i['start_day']] = [i]
                else:
                    voyage[i['start_day']].append(i)

    # Make sure to choose a bike that went on at least 50 trips in your trip data.
    if count >= 50:
        # Plot geographic points
        for i in allstation:
            plt.scatter(allstation[i][0], allstation[i][1], color='r', marker='v', s=100)
            plt.text(allstation[i][0], allstation[i][1], i, ha="left", fontsize=5, wrap=True)

        # Depict the voyage and show the physical locations of each start/end station
        for i in voyage:
            # Record voyage corrdinates
            x = []
            y = []
            for t in voyage[i]:
                start_station = allstation[t['start_station']]
                end_station = allstation[t['end_station']]
                x.append(start_station[0])
                y.append(start_station[1])
                x.append(end_station[0])
                y.append(end_station[1])
            # Plot the voyage of a single bike
            plt.plot(x, y, marker='>', markersize=3, linestyle='dashed', 
                     label=str(i) + " " + voyage[i][0]['start_day_name'])
        plt.plot(42.341814,-71.090179, "X", color="fuchsia", label="Northeastern")
        plt.plot(42.34652004,-71.08065777, "*", color="orange", label="Prudential Center")
        plt.axis('equal')
        plt.legend()
        plt.savefig("singlebike.pdf")
        plt.show()


def main():
    # Read the data
    trips, stations = read_data(BLUE_BIKES_FILE, STATIONS_FILE)
    # Calculate the distance and speed of each trip
    new_trips = calculate_the_distance_and_speed(trips, stations)
    # Visualize the distribution of distances and speeds for the trips
    distance_and_speed_visualize(new_trips)
    # Maps day of the week to the count of trips associated with that day of the week
    # Use only trips thaty end at station "Forsyth St at Huntington Ave"
    count_of_trips(new_trips, NEU_STATION)
    # EC - The voyage of bike 2010 throughout the course of late September 2022
    visualization(trips, stations, 2010)
    

if __name__ == "__main__":
    main()    
