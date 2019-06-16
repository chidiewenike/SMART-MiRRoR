import os,sys
from PyQt5 import QtGui,QtWidgets,QtCore
from Small_Classes import Weather, Time, Quotes, Timer, NextMatch, Word_of_the_Day, News, Personal_Schedule,Tasks, Email
import datetime
import time
from time import sleep
import random

class Window:
    def __init__(self):
        self.update_vals = QtCore.pyqtSignal()        
        self.window = QtWidgets.QMainWindow()
        self.window.setGeometry(0,0,1280, 1024)
        self.pic = QtWidgets.QLabel(self.window)
        self.pic.setGeometry(0, 0, 1280, 1024)
        self.pic.setPixmap(QtGui.QPixmap("/home/pi/Smart Mirror/MiRRoR/Images/Background/background.jpg"))

        # Small_Classes instantiations
        self.weather = Weather()
        self.curr_time = Time()
        self.quote = Quotes()
        self.football = NextMatch()
        self.word = Word_of_the_Day()
        self.news = News()
        self.schedule = Personal_Schedule()
        self.task = Tasks()
        self.email = Email()
        self.football.Load_Match("Everton")
        self.football.Load_Match("LAFC")
        self.football.Load_Match("Finland")
        self.football.Load_Match("Nigeria")
        self.football.Load_Match("US")

        self.window.setWindowFlags(QtCore.Qt.FramelessWindowHint) 
        # Current Emails
        self.email_text = QtWidgets.QLabel(self.window)
        self.email_text.setGeometry(10, 710, 450, 210)
        self.email_text.setStyleSheet('color : white;')
        self.email_text.setFont(QtGui.QFont("SansSerif",14,QtGui.QFont.Bold))
        self.email_text.setAlignment(QtCore.Qt.AlignTop)        
        self.email_text.setWordWrap(True)

        # Current Schedule GUI Placements  
        self.schedule_text = QtWidgets.QLabel(self.window)
        self.schedule_text.setGeometry(10, 135, 475, 560)
        self.schedule_text.setStyleSheet('color : white;')
        self.schedule_text.setFont(QtGui.QFont("SansSerif",14,QtGui.QFont.Bold))
        self.schedule_text.setAlignment(QtCore.Qt.AlignTop)
        self.schedule_text.setWordWrap(True)
        

        # Current tasks GUI Placements  
        self.tasks = QtWidgets.QLabel(self.window)
        self.tasks.setGeometry(975, 310, 250, 700)
        self.tasks.setStyleSheet('color: white')
        self.tasks.setFont(QtGui.QFont("Times",14,QtGui.QFont.Bold))
        self.tasks.setAlignment(QtCore.Qt.AlignTop)
        self.tasks.setWordWrap(True)

        # Music GUI Placements        
        self.music_img = QtWidgets.QLabel(self.window)
        self.music_text = QtWidgets.QLabel(self.window)
        self.music_img.setGeometry(1015, 845, 60, 60)
        self.music_text.setGeometry(1030, 775, 255, 75)
        self.music_text.setStyleSheet('color: white')
        self.music_text.setFont(QtGui.QFont("SansSerif",8,QtGui.QFont.Bold))  
        self.music_time_text = QtWidgets.QLabel(self.window)
        self.music_time_text.setGeometry(1110, 845, 150, 75)
        self.music_time_text.setStyleSheet('color: white')
        self.music_time_text.setFont(QtGui.QFont("Times",8,QtGui.QFont.Bold))  

        # Current Time GUI Placements  
        self.curr_time_text = QtWidgets.QLabel(self.window)
        self.curr_time_text.setGeometry(0,0, 350, 75)
        self.curr_time_text.setStyleSheet('color: white')
        self.curr_time_text.setAlignment(QtCore.Qt.AlignCenter)
        self.curr_time_text.setFont(QtGui.QFont("SansSerif",65,QtGui.QFont.Bold))

        # Current Date GUI Placements
        self.curr_date_text = QtWidgets.QLabel(self.window)
        self.curr_date_text.setGeometry(10,80, 350, 40)
        self.curr_date_text.setStyleSheet('color: white')
        self.curr_date_text.setFont(QtGui.QFont("SansSerif",25,QtGui.QFont.Bold))

        # Current Weather GUI Placements        
        self.curr_weather = QtWidgets.QLabel(self.window)
        self.curr_weather_text = QtWidgets.QLabel(self.window)
        self.curr_weather.setGeometry(1025, 0, 224, 224)
        self.curr_weather_text.setGeometry(1205,10, 275, 100)
        self.curr_weather_text.setStyleSheet('color: white')
        self.curr_weather_text.setFont(QtGui.QFont("SansSerif",22,QtGui.QFont.Bold))  
        self.curr_weather_text.setAlignment(QtCore.Qt.AlignTop)

        scale = 70
        forecast_image_y = 210
        forecast_text_y = forecast_image_y + 50
        forecast_x = 975
        forecast_font = 14
        # Day 1 GUI Placements
        self.day_1_weather = QtWidgets.QLabel(self.window)
        self.day_1_weather_text = QtWidgets.QLabel(self.window)
        self.day_1_weather.setGeometry(forecast_x,forecast_image_y, scale, scale)
        self.day_1_weather_text.setGeometry(forecast_x,forecast_text_y, scale, scale)
        self.day_1_weather_text.setStyleSheet('color: white')
        self.day_1_weather_text.setFont(QtGui.QFont("SansSerif",forecast_font,QtGui.QFont.Bold))  
        self.day_1_weather_text.setAlignment(QtCore.Qt.AlignTop)


        # Day 2 GUI Placements
        self.day_2_weather = QtWidgets.QLabel(self.window)
        self.day_2_weather_text = QtWidgets.QLabel(self.window)
        self.day_2_weather.setGeometry(forecast_x + 60, forecast_image_y, scale, scale)
        self.day_2_weather_text.setGeometry(forecast_x + 60,forecast_text_y, scale, scale)
        self.day_2_weather_text.setStyleSheet('color: white')
        self.day_2_weather_text.setFont(QtGui.QFont("SansSerif",forecast_font,QtGui.QFont.Bold))  
        self.day_2_weather_text.setAlignment(QtCore.Qt.AlignTop)

        # Day 3 GUI Placements
        self.day_3_weather = QtWidgets.QLabel(self.window)
        self.day_3_weather_text = QtWidgets.QLabel(self.window)
        self.day_3_weather.setGeometry(forecast_x + 120, forecast_image_y, scale, scale)
        self.day_3_weather_text.setGeometry(forecast_x + 120,forecast_text_y, scale, scale)
        self.day_3_weather_text.setStyleSheet('color: white')
        self.day_3_weather_text.setFont(QtGui.QFont("SansSerif",forecast_font,QtGui.QFont.Bold))  
        self.day_3_weather_text.setAlignment(QtCore.Qt.AlignTop)

        # Day 4 GUI Placements
        self.day_4_weather = QtWidgets.QLabel(self.window)
        self.day_4_weather_text = QtWidgets.QLabel(self.window)
        self.day_4_weather.setGeometry(forecast_x + 180, forecast_image_y, scale, scale)
        self.day_4_weather_text.setGeometry(forecast_x + 180,forecast_text_y, scale, scale)
        self.day_4_weather_text.setStyleSheet('color: white')
        self.day_4_weather_text.setFont(QtGui.QFont("SansSerif",10,QtGui.QFont.Bold))  
        self.day_4_weather_text.setAlignment(QtCore.Qt.AlignTop)
        
        # Current Info Bar GUI Placements
        self.info_bar = QtWidgets.QLabel(self.window)
        self.info_bar.setWordWrap(True)
        self.info_bar.setGeometry(365, 30, 600, 225)     
        self.info_bar.setStyleSheet('color: white')
        self.info_bar.setFont(QtGui.QFont("SansSerif",12,QtGui.QFont.Bold))
        self.info_bar.setAlignment(QtCore.Qt.AlignTop)

        match_y = 50
        match_x = 975
        # Matches Placement
        self.matches = QtWidgets.QLabel(self.window)
        self.matches.setWordWrap(True)
        self.matches.setGeometry(match_x, match_y, 100, 100)     
        self.matches.setStyleSheet('color: white')
        self.matches.setFont(QtGui.QFont("Times",16,QtGui.QFont.Bold))
        
        # Matches Home
        self.home_team = QtWidgets.QLabel(self.window)
        self.home_team.setGeometry(match_x, match_y - 60, 110, 100)

        # Matches Away
        self.away_team = QtWidgets.QLabel(self.window)
        self.away_team.setGeometry(match_x, match_y + 60, 110, 100)

        # Current News GUI Placements
        self.news_text = QtWidgets.QLabel(self.window)
        self.news_text.setWordWrap(True)
        self.news_text.setGeometry(10, 924, 1270, 100)     
        self.news_text.setStyleSheet('color: white')
        self.news_text.setFont(QtGui.QFont("Times",16,QtGui.QFont.Bold))
        
    def Email_Manager(self, emails):
        self.email_text.setText(emails)

        
    def Music_Manager(self,img,curr_song,time_rem):
        #self.music.next_song()
        mus_pic = QtGui.QPixmap(img)
        mus_pic = mus_pic.scaled(65, 65, QtCore.Qt.KeepAspectRatio)        
        self.music_img.setPixmap(mus_pic)
        self.music_text.setText(curr_song)        
        self.music_time_text.setText(time_rem)

    def News_Manager(self,source,curr_title,curr_desc):
        if not((curr_title == None) or (curr_desc == None)):
            self.news_text.setText(source + ": " + curr_title + "\n" + curr_desc)
        else:
            self.news_text.setText(" " + ": " + " " + "\n" + " ")
    def Time_Manager(self):
        self.curr_time_date = self.curr_time.Find_Time()
        
        self.curr_date_text.setText(self.curr_time_date[0])
        self.curr_time_text.setText(self.curr_time_date[1])
        
    def Forecast_Weather_Manager(self):
        self.weather.Obtain_Five_Day_Forecast()

        scale = 40
        font = 12
        day_1_pix = QtGui.QPixmap(self.weather.Get_Weather_Forecast_Image("0"))
        day_1_pix = day_1_pix.scaled(scale, scale, QtCore.Qt.KeepAspectRatio)
        self.day_1_weather.setPixmap(day_1_pix)
        self.day_1_weather_text.setText(self.weather.Get_Weather_Forecast_Text("0"))
        self.day_1_weather_text.setStyleSheet('color: white')
        self.day_1_weather_text.setFont(QtGui.QFont("Times",font,QtGui.QFont.Bold))

        day_2_pix = QtGui.QPixmap(self.weather.Get_Weather_Forecast_Image("1"))
        day_2_pix = day_2_pix.scaled(scale, scale, QtCore.Qt.KeepAspectRatio)
        self.day_2_weather.setPixmap(QtGui.QPixmap(day_2_pix))
        self.day_2_weather_text.setText(self.weather.Get_Weather_Forecast_Text("1"))
        self.day_2_weather_text.setStyleSheet('color: white')
        self.day_2_weather_text.setFont(QtGui.QFont("Times",font,QtGui.QFont.Bold))

        day_3_pix = QtGui.QPixmap(self.weather.Get_Weather_Forecast_Image("2"))
        day_3_pix = day_3_pix.scaled(scale, scale, QtCore.Qt.KeepAspectRatio)
        self.day_3_weather.setPixmap(QtGui.QPixmap(day_3_pix))
        self.day_3_weather_text.setText(self.weather.Get_Weather_Forecast_Text("2"))
        self.day_3_weather_text.setStyleSheet('color: white')
        self.day_3_weather_text.setFont(QtGui.QFont("Times",font,QtGui.QFont.Bold))

        day_4_pix = QtGui.QPixmap(self.weather.Get_Weather_Forecast_Image("3"))
        day_4_pix = day_4_pix.scaled(scale, scale, QtCore.Qt.KeepAspectRatio)
        self.day_4_weather.setPixmap(QtGui.QPixmap(day_4_pix))
        self.day_4_weather_text.setText(self.weather.Get_Weather_Forecast_Text("3"))
        self.day_4_weather_text.setStyleSheet('color: white')
        self.day_4_weather_text.setFont(QtGui.QFont("Times",font,QtGui.QFont.Bold))
        
    def Current_Weather_Manager(self):
        self.weather.Obtain_Current_Weather()
        self.curr_weather.setPixmap(QtGui.QPixmap(self.weather.Get_Weather_Curr_Image()))
        self.curr_weather_text.setText(self.weather.Get_Weather_Curr_Text())

    def Quote_Manager(self,new_quote):
        if (new_quote == True):
            self.quote.New_Quote()
        self.info_bar.setText("\"" + self.quote.Get_Quote() + "\" - " + self.quote.Get_Author())
        return False

    def Word_Manager(self,new_word):
        if (new_word == True):
            self.word.New_Word()
        self.info_bar.setText("Word of the Day: " + self.word.word + " (" + self.word.type + ")\n" + self.word.definition)
        return False

    def Match_Manager(self,team):         
        teams = self.football.Match_In_Progress(team)
        self.matches.setText(self.football.Get_Teams()[team].date[0] + "/" + self.football.Get_Teams()[team].date[1] + "\n" + self.football.Get_Teams()[team].time[0] + ":" + self.football.Get_Teams()[team].time[1])
        scale = 55
        home_pic = QtGui.QPixmap(teams[0] + ".png")
        home_pic = home_pic.scaled(scale,scale , QtCore.Qt.KeepAspectRatio)

        away_pic = QtGui.QPixmap(teams[1] + ".png")
        away_pic = away_pic.scaled(scale, scale, QtCore.Qt.KeepAspectRatio)

        self.home_team.setPixmap(home_pic)
        self.away_team.setPixmap(away_pic)

    def Schedule_Manager(self,events):
        self.schedule_text.setText(events)
        
        
    def Tasks_Manager(self,tasks):
        self.tasks.setText(tasks)
        
class Thread(QtCore.QThread):

    def __init__(self,window,thread_type):
        QtCore.QThread.__init__(self)
        self.window = window
        self.thread_type = thread_type

        self.curr_time = Time()
        self.timer = Timer()

        self.curr_timer = self.timer.Calc_Timer()
        self.time = self.curr_time.Find_Time()[1]

    def __del__(self):
        self.wait()

    def run(self):

        if (self.thread_type == "Current Weather"):

            while True:

                self.curr_timer = self.timer.Calc_Timer()

                if (self.curr_timer >= 1800):

                    window.Current_Weather_Manager()
                    self.timer.Reset_Timer()

        elif (self.thread_type == "Forecast"):
            while True:
                window.Forecast_Weather_Manager()
                sleep(5000)

        elif (self.thread_type == "Time"):
            while True:
                window.Time_Manager()
                sleep(0.5)

        elif (self.thread_type == "News"):
            count = 0
            cycle_count = 0
            curr_news_timer = Timer()
            update_news_timer = Timer()

            while True:

                if (count == 1):
                    self.window.News_Manager("NY Times",self.window.news.ny_times_title,self.window.news.ny_times_description)
                elif (count == 0):
                    self.window.News_Manager("BBC News",self.window.news.bbc_news_title,self.window.news.bbc_news_description)                    
                elif (count == 2):
                    self.window.News_Manager("Four Four Two",self.window.news.fft_title,self.window.news.fft_description)
                elif (count == 3):
                    self.window.News_Manager("The Scientist",self.window.news.scientist_title,self.window.news.scientist_description)
                else:
                    self.window.News_Manager("Engadget",self.window.news.engadget_title,self.window.news.engadget_description) 

                if (curr_news_timer.Calc_Timer() > 30):
                    count = (count + 1) % 10

                    if (count == 0):
                        cycle_count = (cycle_count + 1) % 3                        
                        self.window.news.Cycle_News(cycle_count)
                        cycle_count = (cycle_count + 1) % 3

                    curr_news_timer.Reset_Timer()


                if (update_news_timer.Calc_Timer() > 3600):
                    self.window.news.Reload_News()
                    update_news_timer.Reset_Timer()
                sleep(1)
        elif (self.thread_type == "Info Change"):
            count = 0
            new_quote = False
            new_words = False
            while True:   

                if (self.time != "00:00:00"):  
                    change = True  
                self.curr_timer = self.timer.Calc_Timer()
                if (self.curr_timer >= 15):
                    self.timer.Reset_Timer()
                    count = (count + 1) % 2

                # display quote
                if (count == 0):
                    new_quote = window.Quote_Manager(new_quote)

                # display word of the day
                elif (count == 1):
                    new_words = window.Word_Manager(new_words)
                    
                self.time = self.curr_time.Find_Time()[1]

                if ((self.time == "00:00:00") and (change)): 
                    new_quote = True
                    new_words = True
                    curr_sel = ""
                    change = False
                    new_quote = window.Quote_Manager(new_quote)
                    new_words = window.Word_Manager(new_words)
                sleep(1)
        elif (self.thread_type == "Matches"):
            foot_count = 0
            team = "Everton"
            foot_timer = Timer()

            while True:
                if (foot_timer.Calc_Timer() >= 10):
                    foot_timer.Reset_Timer()
                    foot_count = (foot_count + 1) % 5
                    window.Match_Manager(team)

                if(foot_count == 0):
                    team = "Everton"
                elif(foot_count == 1):
                    team = "LAFC"
                elif(foot_count == 2):
                    team = "Nigeria"
                elif(foot_count == 3):
                    team = "Finland"
                else:
                    team = "US"    
                sleep(1)
        elif (self.thread_type == "Schedule"):
            while True:
                sched_list = self.window.schedule.List_Events()
                print(sched_list)
                self.window.Schedule_Manager(sched_list[0])
                sleep(30)
                self.window.Schedule_Manager(sched_list[1])   
                sleep(30)
                
        elif (self.thread_type == "Tasks"):
            task_list = self.window.task.Return_Tasks()

            timer = Timer()
            while True:
                curr_timer = timer.Calc_Timer()
                
                if (curr_timer >= 60):
                    timer.Reset_Timer()
                    task_list = self.window.task.Return_Tasks()

                for i in range(len(task_list)):
                    self.window.Tasks_Manager(task_list[i])
                    sleep(5)
                
        
        elif (self.thread_type == "Email"):
            while True:
                emails = self.window.email.check_email()
                for i in range(len(emails)):
                    self.window.Email_Manager(emails[i])
                    sleep(5)

        '''
        elif (self.thread_type == "Music"):
            #music_timer = Timer()
            while True:
                if window.music.mode == 0:
                    self.window.Music_Manager("play.png",self.window.music.Get_Artist()+"\n"+self.window.music.Get_Song(),"00:00")
                elif window.music.mode == 1:
                    self.window.Music_Manager("pause.png",self.window.music.Get_Artist()+"\n"+self.window.music.Get_Song(),"00:00")
                else: 
                    self.window.Music_Manager("play.png",self.window.music.Get_Artist()+"\n"+self.window.music.Get_Song(),"00:00")
        '''
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.Current_Weather_Manager()
    window.Quote_Manager(True)
    window.Time_Manager()
    #window.Match_Manager("Everton")
    window.news.Reload_News()
    window.news.Cycle_News(0)
    window.News_Manager("BBC News",window.news.bbc_news_title,window.news.bbc_news_description)
    window.Schedule_Manager("")
    window.Tasks_Manager("")
    window.Email_Manager("")
    
    #foot_thread = Thread(window, "Matches")
    news_thread = Thread(window,"News")
    time_thread = Thread(window,"Time")
    info_change_thread = Thread(window,"Info Change")
    curr_weather_thread = Thread(window,"Current Weather")
    schedule_thread = Thread(window, "Schedule")
    forecast_weather_thread = Thread(window, "Forecast")
    task_thread = Thread(window,"Tasks")
    email_thread = Thread(window,"Email")
    night_thread = Thread(window,"Night")

    schedule_thread.start()
    news_thread.start()
    time_thread.start()
    info_change_thread.start()
    curr_weather_thread.start()
    #foot_thread.start()
    forecast_weather_thread.start()
    task_thread.start()    
    email_thread.start()

    window.window.show()
    sys.exit(app.exec_())
