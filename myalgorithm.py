from PIL import Image
import numpy as np
import time
import os

#Reading the data from Check.csv
my_data = np.genfromtxt('check.csv', delimiter=',',names=True)

#Get the total number of input files from folder
path, dirs, files = next(os.walk("input"))

#Initialise Output Data
outputList=[]

for index in range(0, len(files)):
    #Image is read
    inputFileName = f"input/ball_{index}.PNG"
    openedImage = Image.open(inputFileName)
    
    #Load Variables
    openedImagePixels = openedImage.load()
    (X, Y) = openedImage.size
    blackPixels=0
    startTimer = None
    endTimer = None

    #Calculation to find the diameter
    startTimer = time.time()
    #Loop to find out number of Black Pixels in the image
    for x in range(X):
        for y in range(Y):
            if openedImagePixels[(x, y)] == (0, 0, 0):
              blackPixels+=1

    #Total Pixel E.g. 640 X 480
    totalImagePixels = np.multiply(X,Y)

    #Perfectly circular objects, radius is equal to the square root of the area (i.e. number of pixels) divided by pi
    squareRootOfTotalColouredPixels = np.sqrt(np.subtract(totalImagePixels, blackPixels)/np.pi) 

    #Diameter is twice the radius
    diameter = int(round(squareRootOfTotalColouredPixels*2))

    #Check if Diameter is valid as expected
    for x in range(len(my_data)):
      if int(my_data[x][0]) == index:
        if int(my_data[x][1]) == diameter:
          print(f"Diameter: {diameter} for index: {index} verified!")
        else:
          print(f"Invalid Diameter: {diameter} for index: {index}")
    
    
    endTimer = time.time()
    timeTaken = int(round((endTimer - startTimer) * 1000))

    print(f"Algorithm Execution Time for Image {index} is {timeTaken} ms \n")
    outputList.append((index, diameter, timeTaken))


#Sorting the Output file from biggest to smallest diameter
sortedOutPutListBasedOnDiameter = sorted(outputList, key = lambda x: (x[1]), reverse=True)
#Saving this as an output CSV file
np.savetxt("output.csv", np.row_stack(sortedOutPutListBasedOnDiameter), delimiter=",", fmt='%s', header="image,diameter,time")
