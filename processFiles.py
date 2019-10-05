#!/usr/bin/python

import os
import sys
import csv

directory_path = sys.argv[1]
num_files = int(sys.argv[2])

all_files = []
client_info = {}
for root, dirs, files in os.walk(directory_path):
    for filename in files:
        if "map_stats_all_clients" in filename:
            all_files.append(directory_path + filename)
        if len(all_files) == num_files:
            break
if len(all_files) != num_files:
    print "Not enough files"
    exit(0)

for filename in all_files:
    print "Started processing file " + filename
    with open(filename,'rb') as input_file:
        reader = csv.reader(input_file)
        next(reader, None)
        for row in reader:
            IP = row[0]
            #Meena's changes to take into account min number of measurements
            #Assuming a polling interval of 20 minutes, at least 72 measurements
            #should have been recorded
            s2c_size = int(row[1])
            c2s_size = max(int(row[2]), int(row[3]))
            #if client has fewer than 72 measurements the ignore it
            if(s2c_size < 72 and c2s_size < 72):
                continue
            tier = row[4]
            if IP not in client_info:
                client_info[IP] = {}
                client_info[IP][filename] = tier
            else:
                client_info[IP][filename] = tier                
    print "Finished processing file " + filename

count = 0
for IP in client_info:
    if len(client_info[IP]) > 1:
        count += 1
        print IP,
        for filename in client_info[IP]:
            #print filename,client_info[IP][filename],
            print client_info[IP][filename],
        print
print "Number of unique IPs: " + str(len(client_info))
print "Number of repeated IPs: " + str(count)