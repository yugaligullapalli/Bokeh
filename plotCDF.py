import sys
import os
import numpy as np
import matplotlib.pyplot as plt
     
'''
Function to plot CDF given the following input:
title for the graph (will be reused for plot file name)
data array
folder where the plot will be saved
x-axis label
''' 
def plotCDF(title, allDistArr, folder, x_label, plt_labels):
    #Compute the values for the CDF
    xVals = []
    yVals = []

    for val in allDistArr:
        x, y = calculateCDF(val)
        xVals.append(x)
        yVals.append(y)

    #Two plots one for Precision Trucation and another for other methods
    plt.grid(linestyle='dotted')
    plt.ylabel('CDF', size = 12)
    plt.xlabel(x_label, size = 12)
    plt.plot(xVals[2], yVals[2], label = plt_labels[2], color='k', linestyle=":", lw = 2)
    plt.plot(xVals[3], yVals[3], label = plt_labels[3], color='r', linestyle="--", lw = 2)
    plt.plot(xVals[4], yVals[4], label = plt_labels[4], color='g', linestyle="-.", lw = 2)
    plt.legend(loc = "lower right")
    plt.savefig(folder + "/" + title + "_1.eps", format = 'eps', dpi = 600)
    plt.clf()

    #Two plots one for Precision Trucation and another for other methods
    plt.grid(linestyle='dotted')
    plt.ylabel('CDF', size = 12)
    plt.xlabel(x_label, size = 12)
    plt.plot(xVals[0], yVals[0], label = plt_labels[0], color='r', linestyle="--", lw = 2)
    plt.plot(xVals[1], yVals[1], label = plt_labels[1], color='g', linestyle="-.", lw = 2)
    plt.legend(loc = "lower right")
    plt.savefig(folder + "/" + title + "_2.eps", format = 'eps', dpi = 600)
    plt.clf()
    

'''
Function that computes the CDF values, given an input array
'''
def calculateCDF(data):
    sorted_data = np.sort(np.asarray(data))
    x1 = []
    y1 = []
    y = 0
    for x in sorted_data:
        x1.extend([x, x])
        y1.append(y)
        y += 1.0 / len(data)
        y1.append(y)

    return x1, y1

'''
Read input file of the format:

distance1
distance2
...
distancen
'''

def readInputFile(inFile):

    distArr = []
    with open(inFile, "r") as FH:
        for line in FH:
            line = line.strip()
            distance = float(line)
            distArr.append(distance)

    return distArr
            
if __name__ == "__main__":
    outFolder = sys.argv[1]
    title = sys.argv[2]

    #Input files with distances from each of the Tier 1 methods for the 3 networks
    inFile1 = "final_plot_data/cl_geocentric_fuzzing.csv"
    inFile2 = "final_plot_data/cl_accuracy_fuzzing.csv"
    inFile3 = "final_plot_data/cl_precision_trucation.txt"
    inFile4 = "final_plot_data/layer_42_precision_truncation.txt"
    inFile5 = "final_plot_data/aurora_precision_trucation.txt"
    
    plt_labels = ["CenturyLink Geocentric Fuzzing", "CenturyLink Accuracy Fuzzing", "CenturyLink Precision Truncation", "Layer 42 Precision Truncation", "Aurora Precision Truncation", "Distance moved (m)"]
    x_label = "Distance moved (m)"

    #Read input files
    distArr1 = readInputFile(inFile1)
    distArr2 = readInputFile(inFile2)
    distArr3 = readInputFile(inFile3)
    distArr4 = readInputFile(inFile4)
    distArr5 = readInputFile(inFile5)

    allDistArr = []
    allDistArr.append(distArr1)
    allDistArr.append(distArr2)
    allDistArr.append(distArr3)
    allDistArr.append(distArr4)
    allDistArr.append(distArr5)

    
    plotCDF(title, allDistArr, outFolder, x_label, plt_labels)
