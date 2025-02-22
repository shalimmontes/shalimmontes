# This program was created by Shalim Montes for the DGAH 110 Midterm on February 20, 2025

## THIS PROGRAM WILL NOT WORK FOR ALL DATASETS ##
# The program will not work correctly with special characters, US locations that are formatted as follows (City, United States)
# because there are duplicate cities in the US, or old names for territories/countries
# Null entries must be specified as 'None' in the csv file

from geopy.geocoders import Nominatim
import time, csv

app = Nominatim(user_agent="Midterm")

def getlatitude(location):
    '''
    Arguments: location (dictionary)
    Returns: the latitude of a location
    This function simply takes in a dictionary containing information about a location and only returns the latitude
    '''
    return location['lat']

def getlongitude(location):
    '''
    Arguments: location (dictionary)
    Returns: the longitude of a location
    This function simply takes in a dictionary containing information about a location and only returns the longitude
    '''
    return location['lon']

def getcoordinatesbycity(city):
    '''
    Arguments: city (string)
    Returns: a tuple with the latitude and longitude of the location in that order
    This function takes in a location and geocodes it using the geopy library to return the latitude and longitude of the location
    '''
    # Part of geopy usage policy, unfortunately makes the program run much slower
    time.sleep(0.5)

    # Checks for strings that are not valid locations
    if (city.strip() == "None" or city.strip() == "placeOfBirth" or city.strip() == "placeOfDeath"):
        return "N/A"
    else:
        try:
            location = app.geocode(city).raw
            latitude = getlatitude(location)
            longitude = getlongitude(location)

            return latitude, longitude
        # In case of timeout error
        except:
            return getcoordinatesbycity(city)
    

def main():
    '''
    Arguments: none
    Returns: 0 to signify successful execution
    This function does all the processing of the original csv file and then writes the transformed data into a new csv file
    '''
    with open('BirthandDeathLocations.csv', mode='r') as file:
        csvfile = csv.reader(file)
        # Each entry of the list is a tuple
        coordinateslist = []
        for row in csvfile:
            birthplace = row[0]
            deathplace = row[1]
            coordsbirth = getcoordinatesbycity(birthplace)
            coordsdeath = getcoordinatesbycity(deathplace)
            coordinateslist.append((coordsbirth, coordsdeath))

    with open('Coordinates.csv', mode='w') as outfile:
        outfile.write("Latitude(Birth)" + ", " + "Longitude(Birth)" + ", " + "Latitude(Death)" + ", " + "Longitude(Death)" + "\n")
        for i in range(1, len(coordinateslist)):
            # Element is one entry of the list and will either have two tuples or one tuple and one string (N/A)
            element = coordinateslist[i]
            birthloc = element[0]
            deathloc = element[1]

            # Tuples can be casted to a list so that we can then cast that list to a string #

            # If both the birth and death locations are tuples i.e. ((43.66456, 65.7594), (45.31455, 96.20349))
            if (isinstance(birthloc, tuple) and isinstance(deathloc, tuple)):
                birthloclist = list(birthloc) # Goes from (43.66456, 65.7594) to [43.66456, 65.7594]
                birthlat = birthloclist[0]
                birthlon = birthloclist[1]
                deathloclist = list(deathloc)
                deathlat = deathloclist[0]
                deathlon = deathloclist[1]

                # Writes out the latitudes and longitudes separately
                outfile.write(str(birthlat) + ", " + str(birthlon) + ", " + str(deathlat) + ", " + str(deathlon) + "\n")

            # If only the birth location is a tuple i.e. ((43.66456, 65.7594), N/A)
            elif (isinstance(birthloc, tuple) and not isinstance(deathloc, tuple)):
                birthloclist = list(birthloc)
                birthlat = birthloclist[0]
                birthlon = birthloclist[1]
                
                # Writes out the latitude and longitude of the birth location separately and puts in place holders
                # for death location
                outfile.write(str(birthlat) + ", " + str(birthlon) + ", N/A, N/A\n")

            # If only the death location is a tuple i.e. (N/A, (43.66456, 65.7594))
            elif (not isinstance(birthloc, tuple) and isinstance(deathloc, tuple)):
                deathloclist = list(deathloc)
                deathlat = deathloclist[0]
                deathlon = deathloclist[1]

                # Writes out the latitude and longitude of the death location separately and puts in place holders
                # for birth location
                outfile.write("N/A, N/A, " + str(deathlat) + ", " + str(deathlon) + "\n")

    return 0

if __name__=="__main__":
    main()