import os,sys
from PyQt5 import QtGui,QtWidgets
from Small_Classes import Weather, Time

app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QMainWindow()
window.setGeometry(0,0,1280, 1024)

pic = QtWidgets.QLabel(window)
pic.setGeometry(0, 0, 1280, 1024)
# self.setWindowFlags(QtCore.Qt.CustomizeWindowHint)    

curr_time = Time()

curr_weather = QtWidgets.QLabel(window)
curr_weather.setGeometry(0, 0, 224, 224)

curr_weather_text = QtWidgets.QLabel(window)
curr_weather_text.setGeometry(0,200, 200, 100)

curr_time_text = QtWidgets.QLabel(window)
curr_time_text.setGeometry(1080,0, 200, 35)

curr_date_text = QtWidgets.QLabel(window)
curr_date_text.setGeometry(1080,35, 200, 20)

weather = Weather()
weather.Obtain_Current_Weather()

#use full ABSOLUTE path to the image, not relative
pic.setPixmap(QtGui.QPixmap("background.jpg"))

curr_weather.setPixmap(QtGui.QPixmap(weather.Get_Weather_Image()))

curr_weather_text.setText(weather.Get_Weather_Text())
curr_weather_text.setStyleSheet('color: white')
curr_weather_text.setFont(QtGui.QFont("Times",6,QtGui.QFont.Bold))

curr_time_date = curr_time.Find_Time()

curr_date_text.setText(curr_time_date[0])
curr_date_text.setStyleSheet('color: white')
curr_date_text.setFont(QtGui.QFont("Times",8,QtGui.QFont.Bold))

curr_time_date = curr_time.Find_Time()

curr_time_text.setText(curr_time_date[1])
curr_time_text.setStyleSheet('color: white')
curr_time_text.setFont(QtGui.QFont("Times",15,QtGui.QFont.Bold))
window.show()
# QtWidgets.QApplication.processEvents() #update gui for pyqt

#window.show()

sys.exit(app.exec_())

