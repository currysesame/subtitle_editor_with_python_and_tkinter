import tkinter as tk
import cv2
import time
from PIL import Image, ImageTk
from tkinter import filedialog as fd
import glob
import moviepy.editor as mp

from ttkthemes import themed_tk
from tkinter import ttk
from mutagen.mp3 import MP3
import os
import pygame

class App:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)

        videosources = glob.glob('./*.mp4')
        self.video_source = videosources[0]
        print()
        # open video source (by default this will try to open the computer webcam)
        self.my_cap = MyVideoCapture(self.video_source)
        self.total_frame_num = self.my_cap.get_total_frame_num()
        audiofile = glob.glob('./*.mp3')
        if len(audiofile) == 0:
            self.fps = self.my_cap.get_fps()
            self.durationSecond = round(self.total_frame_num / self.fps)

            clip = mp.VideoFileClip(self.video_source).subclip(0,self.durationSecond)
            clip.audio.write_audiofile(self.video_source[2:-4] + ".mp3")


        # Create a canvas that can fit the above video source size
        # self.canvas = tkinter.Canvas(window, width = self.my_cap.width, height = self.my_cap.height)
        self.canvas = tk.Canvas(window, width = 960, height = 540)
        self.canvas.pack()

        self.btn_pause_start=tk.Button(window, text="pause/start", width=50, command=self.pause_start)
        self.btn_pause_start.pack(anchor=tk.CENTER, expand=True)

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 10

        self.textWidget = tk.Text(window, height = 5, width = 52)
        self.textWidget.pack()

        self.btn_SaveSubtitle=tk.Button(window, text="save subtitle", width=50, command=self.saveSubtitle)
        self.btn_SaveSubtitle.pack(anchor=tk.CENTER, expand=True)

        
        self.processBar = tk.Scale(window, from_=0, to=self.total_frame_num,length=600,tickinterval=int(self.total_frame_num/10), orient=tk.HORIZONTAL)
        self.subtitleBar = tk.Scale(window, from_=0, to=self.total_frame_num,length=600,tickinterval=int(self.total_frame_num/10), orient=tk.HORIZONTAL)
        
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
        self.processBar.pack()
        self.subtitleBar.pack()
        self.count = 0
        self.count10 = 0
        self.start = 1
        self.update()

        self.window.mainloop()

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
    # def snapshot(self):
    #     # Get a frame from the video source
    #     ret, frame = self.my_cap.get_frame()
 
    #     if ret:
    #         cv2.imwrite("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

    def update(self):
        # Get a frame from the video source
        ret, frame = self.my_cap.get_frame()

        if ret:
            self.count10 +=1
            if(self.start == 1):
                self.count += 1
            if(self.count10 % 5 == 0):
                self.count = self.processBar.get()
            self.processBar.set(self.count)
            self.photo = ImageTk.PhotoImage(image = Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tk.NW)
            self.my_cap.set_frame_in_video(self.count)
        self.window.after(self.delay, self.update)



class MyVideoCapture:
    def __init__(self, video_source=0):
        # Open the video source
        
        self.vid = cv2.VideoCapture(video_source)
        frame_num = int(self.vid.get(cv2.CAP_PROP_FRAME_COUNT))
        print('frame_num', frame_num)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        # Get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

        self.dsize_width = 960
        self.dsize_height = 540

    def get_frame(self):
        if self.vid.isOpened():
            #self.vid.set(1,300)
            ret, frame = self.vid.read()
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return (ret, cv2.resize(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), (self.dsize_width, self.dsize_height)))
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

# import glob

# # ref: https://github.com/ritik48/Music-Player-Tutorial-Codes

# import tkinter as tk
# from ttkthemes import themed_tk
# from tkinter import ttk
# from PIL import Image, ImageTk
# from tkinter import filedialog
# from mutagen.mp3 import MP3
# import os
# import time
# import pygame


# class MediaPlayer:
#     def __init__(self, window):

#         style = ttk.Style()
#         style.theme_use("breeze")

#         background = "grey"

#         style.configure("TScale",background = background)

#         self.root = window

#         self.root.configure(bg="black")

#         self.play_icon = Image.open('images/play.png')
#         self.play_icon = self.play_icon.resize((90, 90), Image.ANTIALIAS)
#         self.play_icon = ImageTk.PhotoImage(self.play_icon)

#         self.pause_icon = Image.open('images/pause.png')
#         self.pause_icon = self.pause_icon.resize((90, 90), Image.ANTIALIAS)
#         self.pause_icon = ImageTk.PhotoImage(self.pause_icon)

#         tk.Label(self.root, text="",background=background,height=7,width=120).place(x=5,y=400)

#         self.songs_list = tk.Listbox(self.root, width=30, height=18, bg="black", fg="blue", relief="flat",
#                                      selectbackground="grey")
#         self.songs_list.place(x=520, y=60)

#         self.time_elapsed_label = tk.Label(self.root,text="00:00", fg="black",background=background,
#                                            activebackground=background,padx=5)
#         self.time_elapsed_label.place(x=10,y=400)

#         self.music_duration_label = tk.Label(self.root,text="00:00",fg="black",background=background,
#                                              activebackground=background,padx=15)
#         self.music_duration_label.place(x=460,y=400)

#         self.progress_scale = ttk.Scale(self.root,orient="horizontal",style='TScale',from_=0,length=380,
#                                         command=self.progress_scale_moved,cursor='hand2')
#         self.progress_scale.place(x=80,y=400)

#         self.play_button = tk.Button(self.root,image=self.play_icon,command=self.check_play_pause,cursor='hand2',bd=0,
#                                      background=background,activebackground=background)
#         self.play_button.place(x=146,y=425)


#         self.status = tk.Label(self.root,text="Playing : ---------- Song : 0 of 0",fg="black",anchor="w",background="grey",
#                                font="lucida 9 bold",bd=5,relief="ridge")
#         self.status.place(x=5,y=520,relwidth=1)

#         self.menu = tk.Menu(self.root)
#         self.root.configure(menu=self.menu)

#         m1 = tk.Menu(self.menu,background="grey",tearoff=False,bd=0,activebackground="black")
#         self.menu.add_cascade(label="Actions",menu=m1)

#         m2 = tk.Menu(self.menu, background="grey", tearoff=False, bd=0, activebackground="black")
#         self.menu.add_cascade(label="Delete", menu=m2)

#         self.directory_list = []
#         self.pause=False
#         self.played = False
#         self.songs_to_play=[]

#     def check_play_pause(self):
#         if not self.played:
#             self.play_song()
#         else:
#             self.pause_unpause()

#     def pause_unpause(self):
#         if not self.pause:
#             self.root.after_cancel(self.updater)
#             self.play_button.config(image=self.play_icon)
#             self.pause=True
#             pygame.mixer.music.pause()
#         else:
#             self.pause=False
#             self.play_button.config(image=self.pause_icon)
#             pygame.mixer.music.unpause()
#             self.scale_update()

#     def play_song(self):
#         self.progress_scale['value'] = 0
#         self.time_elapsed_label['text'] = "00:00"
#         self.song_with_path = glob.glob('./*.mp3')[0]
#         music_data = MP3(self.song_with_path)
#         self.music_length = int(music_data.info.length)
#         self.music_duration_label['text'] = time.strftime('%M:%S', time.gmtime(self.music_length))

#         self.progress_scale['to'] = self.music_length
#         self.play_button.config(image=self.pause_icon)
#         pygame.mixer.music.load(self.song_with_path)
#         pygame.mixer.music.play()
#         self.played = True
#         self.scale_update()

#     def progress_scale_moved(self,x):
#         self.root.after_cancel(self.updater)
#         scale_at=self.progress_scale.get()

#         pygame.mixer.music.load(self.song_with_path)
#         pygame.mixer.music.play(0,scale_at)
#         self.scale_update()

#     def scale_update(self):
#         if self.progress_scale['value'] < self.music_length:
#             self.progress_scale['value'] += 1
#             self.time_elapsed_label['text'] = time.strftime('%M:%S', time.gmtime(self.progress_scale.get()))
#             self.updater = self.root.after(1000, self.scale_update)
#         else:
#             self.progress_scale['value'] = 0
#             self.time_elapsed_label['text'] = "00:00"
#             self.play_button.config(image=self.play_icon)
#             self.songs_to_play=[]

# if __name__ == '__main__':
#     window = themed_tk.ThemedTk()
#     pygame.init()

#     window.title("Music Player")
#     window.wm_iconbitmap('images/music.ico')
#     window.maxsize(width=750,height=550)
#     window.minsize(width=540,height=550)

#     x = MediaPlayer(window)
#     window.mainloop()