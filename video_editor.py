import tkinter as tk
import cv2
import time
from PIL import Image, ImageTk
from tkinter import filedialog as fd
import glob
import moviepy.editor as mp
from tkinter import ttk
from mutagen.mp3 import MP3
import os
import pygame

class App:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)

        windowWidth = 768
        windowHeight = 432

        videosources = glob.glob('./*.mp4')
        self.video_source = videosources[0]
        print()
        # open video source (by default this will try to open the computer webcam)
        self.my_cap = MyVideoCapture(self.video_source, windowWidth, windowHeight)
        self.total_frame_num = self.my_cap.get_total_frame_num()
        audiofile = glob.glob('./*.mp3')
        if len(audiofile) == 0:
            self.fps = self.my_cap.get_fps()
            self.durationSecond = round(self.total_frame_num / self.fps)

            clip = mp.VideoFileClip(self.video_source).subclip(0,self.durationSecond)
            clip.audio.write_audiofile(self.video_source[2:-4] + ".mp3")


        # Create a canvas that can fit the above video source size
        self.canvas = tk.Canvas(self.window, width = windowWidth, height = windowHeight)
        self.canvas.pack()

        self.btn_pause_start=tk.Button(self.window, text="pause/start", width=50, command=self.pause_start)
        self.btn_pause_start.pack(anchor=tk.CENTER, expand=True)

        

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 10

        self.textWidget = tk.Text(self.window, height = 5, width = 52)
        self.textWidget.pack()

        self.btn_SaveSubtitle=tk.Button(self.window, text="save subtitle", width=50, command=self.saveSubtitle)
        self.btn_SaveSubtitle.pack(anchor=tk.CENTER, expand=True)
        self.btn_writeCurrentSecond=tk.Button(self.window, text="end of this subtitle (sec)", width=50, command=self.writeCurrentSecond)
        self.btn_writeCurrentSecond.pack(anchor=tk.CENTER, expand=True)
        
        self.processBar = tk.Scale(self.window, from_=0, to=self.total_frame_num,length=600,tickinterval=int(self.total_frame_num/10), orient=tk.HORIZONTAL)
        self.processBar.pack()
        self.label = tk.Label(self.window, text='0')
        self.label.pack(anchor=tk.CENTER, expand=True)
        self.subtitleBar = tk.Scale(self.window, from_=0, to=self.total_frame_num,length=600,tickinterval=int(self.total_frame_num/10), orient=tk.HORIZONTAL)
        self.subtitleBar.pack()

        self.play_icon = Image.open('images/play.png')
        self.play_icon = self.play_icon.resize((80, 80), Image.ANTIALIAS)
        self.play_icon = ImageTk.PhotoImage(self.play_icon)

        self.pause_icon = Image.open('images/pause.png')
        self.pause_icon = self.pause_icon.resize((80, 80), Image.ANTIALIAS)
        self.pause_icon = ImageTk.PhotoImage(self.pause_icon)

        self.time_elapsed_label=tk.Label(self.window, text="00:00", width=50, padx=5)
        self.time_elapsed_label.pack(anchor=tk.CENTER, expand=True)

        self.music_duration_label = tk.Label(self.window,text="00:00",fg="black",padx=15)
        self.music_duration_label.pack(anchor=tk.CENTER, expand=True)


        self.progress_scale = ttk.Scale(self.window,orient="horizontal",style='TScale',from_=0,length=400,
                                        command=self.progress_scale_moved,cursor='hand2')
        self.progress_scale.pack(anchor=tk.CENTER, expand=True)

        self.play_button = tk.Button(self.window,image=self.play_icon,command=self.check_play_pause,cursor='hand2',bd=0)
        self.play_button.pack(anchor=tk.CENTER, expand=True)

        self.pause=False
        self.played = False


        # read text
        textfile = glob.glob('./*.txt')
        if len(textfile) == 0:
            with open(self.video_source[2:-4] + '.txt', 'w') as f:
                f.write('Create a new text file!')
                f.close()
        else:
            counterLine = 0
            f = open(self.video_source[2:-4] + '.txt', "r")
            for line in f:
                counterLine += 1
                self.textWidget.insert(str(counterLine) +'.0', line)
            counterLine = 0
            f.close()

        print(self.processBar.get())
        
        self.count = 0
        self.count10 = 0
        self.start = 1
        self.update()

        self.window.mainloop()

    def writeCurrentSecond(self):
        counterLine = 0
        f = open(self.video_source[2:-4] + '.txt', "r")
        for line in f:
            counterLine += 1
        self.textWidget.insert(str(counterLine+1) +'.0', ' ' + str(round(self.processBar.get()/24.0, 2)) + ' sub \n')
        f.close()
        self.saveSubtitle()
    def pause_start(self):
        self.my_cap.get_frame_num()
        if(self.start == 1):
            self.start = 0
            return
        if(self.start == 0):
            self.start = 1
            return
    def saveSubtitle(self):
        textContent = self.textWidget.get(1.0, "end-1c")
        with open(self.video_source[2:-4] + '.txt', 'w') as f:
            f.write(textContent)
            f.close()

    def update(self):
        # Get a frame from the video source
        ret, frame = self.my_cap.get_frame()
        self.label.config(text = 'sec: ' + str(round(self.processBar.get()/24.0, 2)))
        if ret:
            self.count10 +=1
            if(self.start == 1):
                self.count += 1
            if(self.count10 % 5 == 0):
                self.count = self.processBar.get()
                self.count10 = 0
            self.processBar.set(self.count)
            self.photo = []
            self.photo = ImageTk.PhotoImage(image = Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tk.NW)
            self.my_cap.set_frame_in_video(self.count)
        self.window.after(self.delay, self.update)

    def check_play_pause(self):
        if not self.played:
            self.play_song()
        else:
            self.pause_unpause()

    def pause_unpause(self):
        if not self.pause:
            self.window.after_cancel(self.updater)
            self.play_button.config(image=self.play_icon)
            self.pause=True
            pygame.mixer.music.pause()
        else:
            self.pause=False
            self.play_button.config(image=self.pause_icon)
            pygame.mixer.music.unpause()
            self.scale_update()

    def play_song(self):
        self.progress_scale['value'] = 0
        self.time_elapsed_label['text'] = "00:00"
        self.song_with_path = glob.glob('./*.mp3')[0]
        music_data = MP3(self.song_with_path)
        self.music_length = int(music_data.info.length)
        self.music_duration_label['text'] = time.strftime('%M:%S', time.gmtime(self.music_length))

        self.progress_scale['to'] = self.music_length
        self.play_button.config(image=self.pause_icon)
        pygame.mixer.music.load(self.song_with_path)
        pygame.mixer.music.play()
        self.played = True
        self.scale_update()

    def progress_scale_moved(self,x):
        self.window.after_cancel(self.updater)
        scale_at=self.progress_scale.get()

        pygame.mixer.music.load(self.song_with_path)
        pygame.mixer.music.play(0,scale_at)
        self.scale_update()

    def scale_update(self):
        if self.progress_scale['value'] < self.music_length:
            self.progress_scale['value'] += 1
            self.time_elapsed_label['text'] = time.strftime('%M:%S', time.gmtime(self.progress_scale.get()))
            self.updater = self.window.after(1000, self.scale_update)
        else:
            self.progress_scale['value'] = 0
            self.time_elapsed_label['text'] = "00:00"
            self.play_button.config(image=self.play_icon)

class MyVideoCapture:
    def __init__(self, video_source, windowWidth, windowHeight):
        # Open the video source
        
        self.windowWidth = windowWidth
        self.windowHeight = windowHeight

        self.vid = cv2.VideoCapture(video_source)
        frame_num = int(self.vid.get(cv2.CAP_PROP_FRAME_COUNT))
        print('frame_num', frame_num)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        # Get video source width and height
        # self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        # self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
        if self.vid.isOpened():
            #self.vid.set(1,300)
            ret, frame = self.vid.read()
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return (ret, cv2.resize(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), (self.windowWidth, self.windowHeight)))
            else:
                return (ret, None)
        else:
            return (ret, None)

    def get_frame_num(self):
        print(int(self.vid.get(cv2.CAP_PROP_POS_FRAMES)))
    def get_total_frame_num(self):
        return int(self.vid.get(cv2.CAP_PROP_FRAME_COUNT))
    def set_frame_in_video(self, number):
        self.vid.set(1, number)
    def get_fps(self):
        return self.vid.get(cv2.CAP_PROP_FPS)
    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

    


# Create a window and pass it to the Application object
App(tk.Tk(), "Subtitle editor")
pygame.init()

# # ref: https://github.com/ritik48/Music-Player-Tutorial-Codes