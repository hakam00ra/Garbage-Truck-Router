import sys, os
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMessageBox, QWidget, QLabel, QVBoxLayout, QProgressBar, QPushButton
from PyQt5.QtCore import *
from time import sleep
from openpyxl import Workbook
import matplotlib.pyplot as plt
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication,
    QPushButton,
    QWidget,
)
import io
import folium
import requests
import json
import webbrowser
import polyline
import geopy.distance
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
from time import sleep




def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class WorkerSignals(QObject):
    mapReady = pyqtSignal(int)   
    show = pyqtSignal(int) 


class Window(QLabel):
    def __init__(self):
        super().__init__()
        self.threadpool = QThreadPool()
        self.setAlignment(Qt.AlignCenter)
        self.map = QWebEngineView()
        self.map.hide()


    def showMap(self, maps):
        self.map.show()
        self.hide()
        self.map.setHtml(open('map.html').read())

    def showDrop(self):
        self.show()
        self.map.hide()
        
        
        

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.threadpool = QThreadPool()
        self.signals = WorkerSignals()
        self.setWindowIcon(QtGui.QIcon(resource_path("trash.ico")))
        self.setWindowTitle("Garbage Truck Router")
        self.resize(400, 400)
        mainLayout = QVBoxLayout()
        self.setLayout(mainLayout)
        self.ctrl = {'break': False}
        self.setAcceptDrops(True)
        self.mapViewer = Window()
        mainLayout.addWidget(self.mapViewer)
        mainLayout.addWidget(self.mapViewer.map)
        self.signals.mapReady.connect(self.mapViewer.showMap)
        self.signals.show.connect(self.mapViewer.showDrop)
        
    
    def dragEnterEvent(self, event):
        self.signals.show.emit(1)
        if event.mimeData().hasText:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):   
        self.signals.show.emit(1)     
        if event.mimeData().hasText:            
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):               
        event.setDropAction(Qt.CopyAction)    
        global fileDir        
        fileDir = event.mimeData().urls()[0].toLocalFile()        
        print(fileDir)    
        with open(f'{fileDir}', 'r') as file:
            content = file.read()

        lines = content.splitlines()

        coordinates = []
        for line in lines:
            lat, lon = line.split(', ')
            coordinates.append((float(lat), float(lon)))   
                     
        self.map_route(coordinates)
        

        

    def load_map(self):
        self.mapViewer.setUrl(QUrl.fromLocalFile(os.path.abspath("map.html")))

    def map_route(self, coordinates):
        map = folium.Map(location=coordinates[0], zoom_start=13)

        route = self.get_route(coordinates)

        folium.PolyLine(route, color="red", weight=2.5, opacity=1).add_to(map)

        for coord in coordinates:
            folium.Marker(coord).add_to(map)

        map.save("map.html")
        #webbrowser.open("map.html")
        self.signals.mapReady.emit(1)
        print("Map saved as 'map.html'.")
        return map 
        

    def get_route(self, coordinates):
        coords = ";".join(f"{coord[1]},{coord[0]}" for coord in coordinates)
        url = f"https://router.project-osrm.org/route/v1/driving/{coords}"
        response = requests.get(url)
        res = response.json()
        poly = polyline.decode(res['routes'][0]['geometry'])
        print(poly)
        print(res['routes'][0]['distance'])
        if response.status_code == 200:
            data = json.loads(response.text)
            print("API response:", data)
        else:
            print(f"Request failed with status code: {response.status_code}")
            return []

        total_distance = 0
        for i in range(len(poly) - 1):
            coord1 = poly[i]
            coord2 = poly[i + 1]
            total_distance += geopy.distance.distance(coord1, coord2).km

        return poly




application = QApplication(sys.argv)
app = App()
app.show()
sys.exit(application.exec_())