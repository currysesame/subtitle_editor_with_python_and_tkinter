import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import time
from tkinter import filedialog as fd
import glob
import moviepy.editor as mp



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
        self.canvas = tkinter.Canvas(window, width = 960, height = 540)
        self.canvas.pack()

        self.btn_pause_start=tkinter.Button(window, text="pause/start", width=50, command=self.pause_start)
        self.btn_pause_start.pack(anchor=tkinter.CENTER, expand=True)

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 10

        self.textWidget = tkinter.Text(window, height = 5, width = 52)
        self.textWidget.pack()

        self.btn_SaveSubtitle=tkinter.Button(window, text="save subtitle", width=50, command=self.saveSubtitle)
        self.btn_SaveSubtitle.pack(anchor=tkinter.CENTER, expand=True)

        
        self.processBar = tkinter.Scale(window, from_=0, to=self.total_frame_num,length=600,tickinterval=int(self.total_frame_num/10), orient=tkinter.HORIZONTAL)
        self.subtitleBar = tkinter.Scale(window, from_=0, to=self.total_frame_num,length=600,tickinterval=int(self.total_frame_num/10), orient=tkinter.HORIZONTAL)
        
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
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)
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
App(tkinter.Tk(), "Subtitle editor")




