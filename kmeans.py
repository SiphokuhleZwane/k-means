import csv
import matplotlib.pyplot as plt
from random import sample
from math import sqrt, floor

# lists storing data from CSV file
countries = [] 
birthRates = [] 
lifeExpect = [] 

# lists storing cluster means
birthClustMeans = [] 
lifeClustMeans = []

# euclidean distance formula 
def distance(xi, yi, xj, yj):
    euclDis = sqrt((xj - xi)**2 + (yj - yi)**2) 
    return euclDis

# Reading data from the csv files
def csvFile():
    with open("data2008.csv", 'r') as file:
        reader = csv.reader(file)
        count = 0
        for i in reader:
            if count!=0:
                # appending data to lists
                countries.append(i[0]) 
                birthRates.append(float(i[1]))
                lifeExpect.append(float(i[2]))
            count+=1
        return count-1 # returning length of data

# initial means for each cluster
def initialMeans(n, k):
    for i in range(k):
        # formulas for initial allocation of clusters
        begIndex = floor((n/k)*i) 
        endIndex = floor((n/k)*(i+1))
        clusterLen = endIndex - begIndex
        # calculating mean by taking samples 
        birthMean = sum(sample(birthRates, clusterLen))/clusterLen
        lifeMean = sum(sample(lifeExpect, clusterLen))/clusterLen

        birthClustMeans.append(birthMean)
        lifeClustMeans.append(lifeMean)

# calculating each cluster mean
def clustMeanCalc(k):
    # clearing means for each loop interation
    birthClustMeans.clear()
    lifeClustMeans.clear()
    
    for i in range(k):
        # cannot divide by zero
        if len(birthClust[i]) != 0:
            birthMean = sum(birthClust[i])/len(birthClust[i])
            lifeMean = sum(lifeClust[i])/len(lifeClust[i])

            birthClustMeans.append(birthMean)
            lifeClustMeans.append(lifeMean)
        else:
            birthClustMeans.append(0)
            lifeClustMeans.append(0)

        # clearing clusters for each interation  
        countryClust[i].clear()      
        birthClust[i].clear()
        lifeClust[i].clear()

# user input 
k = int(input("Enter the number of clusters: "))
n = csvFile()

# lists storing all cluster data
countryClust = [[] for i in range(k)]
birthClust = [[] for i in range(k)]
lifeClust = [[] for i in range(k)]

prevTotal = 0
while True:  # k-means algorithm
    
    if prevTotal == 0: 
        initialMeans(n, k) 
    else: 
        clustMeanCalc(k)
    
    sumTotal = 0  
    for i in range(n):
        # finding nearest cluster 
        shortDis = distance(birthRates[i], lifeExpect[i], birthClustMeans[0], lifeClustMeans[0])
        cluster = 0
        for j in range(1, k):
            euclDis = distance(birthRates[i], lifeExpect[i], birthClustMeans[j], lifeClustMeans[j])
            if euclDis <= shortDis:
                cluster = j
                shortDis = euclDis
        sumTotal += shortDis
        # assigning to nearest cluster
        countryClust[cluster].append(countries[i])
        birthClust[cluster].append(birthRates[i])
        lifeClust[cluster].append(lifeExpect[i])
    # monotoring convergence
    if sumTotal == prevTotal:
        break # sumTotal converged 
    else:
        prevTotal = sumTotal
    
# Print out the results
colours = ['red', 'blue', 'orange', 'green', 'purple'] # colours for clusters
for i in range(k):
    print("Cluster", i+1)
    print("Number of countries:", len(countryClust[i]))
    print("Countries:")
    print(countryClust[i])
    print("Mean Birth Rate: {:.2f}".format(birthClustMeans[i]))
    print("Mean Life Expectancy: {:.2f}".format(lifeClustMeans[i]))
    plt.scatter(birthClustMeans[i], lifeClustMeans[i], s = 250, c = 'black', marker = '+', label = 'Cluster {} Mean'.format(i+1))
    plt.scatter(birthClust[i], lifeClust[i], c=colours[i], alpha=0.7)
    print()

# plotting country names 
for i, j in enumerate(countries):
    plt.annotate(j, (birthRates[i], lifeExpect[i]), size = 6)

# plot labels
plt.title("K-means Clustering on birth rates and life expectancy of various countries", fontsize = 'x-large')
plt.xlabel("Birth Rates", fontsize = 'x-large')
plt.ylabel("Life Expectancy", fontsize = 'x-large')
plt.legend(loc='upper right', fontsize = 'small')
plt.grid('True')
plt.show()
