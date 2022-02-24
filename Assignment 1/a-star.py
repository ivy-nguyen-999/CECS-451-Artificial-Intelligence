# Import math Library
import math
# Import sys for reading input from the system
import sys

def parseNearbyCities():
    #Use with statement to close the file automatically
    with open('map.txt') as mapInput:
        #Save all the lines as a list of strings
        lines = mapInput.readlines()
    
    #Create a dictionary to contain the city as key
    #and list of nearby cities as value
    nearbyCities = {}
    
    for line in lines:
        #Split each line
        #Use strip() to remove '\n'
        temp = line.strip().split("-")
        city = temp[0].strip("''")
        #Create a list contains tuples of nearby cities
        listNearbyCities = []
        tempNearbyCities = temp[1].strip("''").split(",")
        #For each nearby city
        for nearbyCity in tempNearbyCities:
            tempCity = nearbyCity.strip("')'").split("(")
            tempTuple = (tempCity[0].strip("''"), float(tempCity[1].strip("''")))
            #Add the city to the list
            listNearbyCities.append(tempTuple)
        #Add the list of nearby cities to the dictionary
        nearbyCities[city] = listNearbyCities
    
    return nearbyCities

def parseCoordinates():
    #Use with statement to close the file automatically
    with open('coordinates.txt') as coordinateInput:
        #Save all the lines as a list of strings
        lines = coordinateInput.readlines()
    
    #Create a dictionary to contain all the coordinates with
    #the cities as key and longitude and latitude as value
    coordinates = {}
    
    #Loop through each line of the list
    for line in lines:
        #split into 'location' and '(latitude, longitude)'
        temp = line.strip().split(":")
        city = temp[0].strip("''")
        coordinate = temp[1].strip("()").split(",")
        latitude = float(coordinate[0].strip("''"))
        longitude = float(coordinate[1].strip("''"))
        coordinates[city] = [latitude, longitude]

    return coordinates

def findStraightLineDistance(coordinateList, cityA, cityB):
    #Radius of the earth
    RADIUS = 3958.8
    
    #Get longitude and latitude and convert to radian
    
    #First city
    latitudeA = coordinateList[cityA][0] * math.pi / 180
    longitudeA = coordinateList[cityA][1] * math.pi / 180
    
    #Second city
    latitudeB = coordinateList[cityB][0] * (math.pi / 180)
    longitudeB = coordinateList[cityB][1] * (math.pi / 180)
    
    #Find straight line distance
    avgLatitude = (latitudeB - latitudeA) / 2
    avgLongitude = (longitudeB - longitudeA) / 2
    sinSqAvgLatitude = math.sin(avgLatitude) ** 2
    sinSqAvgLongitude = math.sin(avgLongitude) ** 2
    insideSq = sinSqAvgLatitude + math.cos(latitudeA) * math.cos(latitudeB) * sinSqAvgLongitude
    distance = 2 * RADIUS * math.asin(math.sqrt(insideSq))
    return distance

def aStar(neighbors, coordinates, currentCity, dest):
        
    #Create a dictionary to store estimated cost {city:cost}
    estimatedCosts = {currentCity:findStraightLineDistance(coordinates, currentCity, dest)}
    
    #Create a dictionary to store currect cost {city:cost}
    actualCosts = {currentCity:0}
    
    #Create a dictionary to store the paths {current:prev}
    paths = {currentCity:'None'}
    
    while True:
        #Use the city that has mininum estimated cost
        currentCity = min(estimatedCosts, key = estimatedCosts.get)
        
        #If the city is the goal
        if (currentCity == dest):
            break
        
        #Search for neighbor cities
        for city in neighbors[currentCity]:
            #Calculate temp values
            #city=(name, cost)
            tempDist = findStraightLineDistance(coordinates, city[0], dest)
            tempActualCost = actualCosts[currentCity] + city[1]
            tempEstimateCost = tempActualCost + tempDist
            
            #If the city is not visited yet or has lower actual value
            if ((actualCosts.get(city[0]) is None) or (actualCosts[city[0]] > tempActualCost)):
                actualCosts[city[0]] = tempActualCost
                estimatedCosts[city[0]] = tempEstimateCost
                paths[city[0]] = currentCity
        
        #Delete the current city
        del estimatedCosts[currentCity]
    
    #Get the path
    pathList = []
    while (currentCity != 'None'):
        pathList.insert(0, currentCity)
        currentCity = paths[currentCity]
    
    #Print output and return
    print("From city:", pathList[0])
    print("To city:", pathList[-1])
    print("Best Route:", end = " ")
    print(*pathList, sep = " - ")
    print("Total distance:", f'{actualCosts[pathList[-1]]:.2f} mi')
    return

def main(firstCity, secondCity):
    mapCA = parseNearbyCities()
    cityCoordinates = parseCoordinates()
    
    aStar(mapCA, cityCoordinates, firstCity, secondCity)
    return

sysInput = sys.argv
#Get two cities
firstCity = str(sysInput[-2])
secondCity = str(sysInput[-1])
main(firstCity, secondCity)
