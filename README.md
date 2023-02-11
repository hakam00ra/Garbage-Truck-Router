# Garbage Truck Router
![image](https://www.rd.com/wp-content/uploads/2018/05/garbage-finds-ft.jpg?resize=700,467)

This is a Garbage Truck Route simulator. Drag and drop a .txt file containing a list of coordinates like coordinates.txt:
```c
40.7278, -73.9964
40.7284, -73.9962
40.7291, -73.9960
40.7298, -73.9958
40.7305, -73.9956
40.7312, -73.9954
40.7319, -73.9952
40.7326, -73.9950
```

This app will get the directions for that route and visualize the driving route inside the app's window.

![image](https://user-images.githubusercontent.com/50047346/218276694-62feee76-01f3-4600-961a-477b7f78a40f.png)

## Inner Workings
An [OSRM](https://github.com/Project-OSRM/osrm-backend) request is made with the coordinates obtained from the drag and dropped .txt file. The polyline from the response containing the route is used to create a [folium](https://github.com/python-visualization/folium) map with markers showing the distance between each dumpster. Last dumpster also shows total driving distance.
