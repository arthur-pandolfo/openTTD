#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import numpy as np

x_size,y_size = 1024,512

# actual map size
x_size -= 2
y_size -= 2

with open("coordinates.json",'r') as f:
    raw_city_data = json.load(f)

with open("centering.txt",'r',newline='\n') as f:
    city1_line = f.readline()
    city2_line = f.readline()
    
# two cities for centering - other locations are interpolated
center1_str,center1_x,center1_y = city1_line.split(',')
center1_x = int(center1_x)
center1_y = int(center1_y)

center2_str,center2_x,center2_y = city2_line.split(',')
center2_x = int(center2_x)
center2_y = int(center2_y)

center1_found = False
center2_found = False
for city_dic in raw_city_data:
    if city_dic["nome"] == center1_str:
        center1_dic = city_dic
        center1_lat = center1_dic["latitude"]
        center1_long = center1_dic["longitude"]
        center1_found = True
    if city_dic["nome"] == center2_str:
        center2_dic = city_dic
        center2_lat = center2_dic["latitude"]
        center2_long = center2_dic["longitude"]
        center2_found = True
    if center1_found and center2_found:
        break
else:
    raise ValueError("Centering failed")
    
def geo_to_tile_gen(x1,y1,x2,y2):
    ratio = (y2-y1)/(x2-x1)
    def geo_to_tile(x):
        return int(np.round_(y1 + (x-x1)*ratio))
    return geo_to_tile

lat_to_y = geo_to_tile_gen(center1_lat,center1_y,center2_lat,center2_y)
long_to_x = geo_to_tile_gen(center1_long,center1_x,center2_long,center2_x)

geo_data = []
for city_dic in raw_city_data:
    x_tile = long_to_x(city_dic["longitude"])
    y_tile = lat_to_y(city_dic["latitude"])
    
    if x_tile < 1 or x_tile > x_size or y_tile < 1 or y_tile > y_size:
        continue
    
    geo_data.append((city_dic["nome"],x_tile,y_tile))
    
output = ["city,x,y\n"]
for data in geo_data:    
    output.append(','.join(str(val) for val in data)+'\n')

with open("generated_city_locations.csv",'w') as f:
    f.writelines(output)
