from moviepy import editor
from moviepy.video.io.VideoFileClip import VideoFileClip
import os.path as op
import glob

# ref: https://python-climbing.com/moviepy-subtitle/

"""以下2行はwindowsユーザは書かないとおそらくエラーが出ます"""
from moviepy.config import change_settings
change_settings({"IMAGEMAGICK_BINARY": r"D:/PRO/ImageMagick/ImageMagick-7.1.0-Q16-HDRI/magick.exe"})

file_path = glob.glob("./*.mp4")[0]#字幕を付けたい動画のパス
text_path = glob.glob('./*.txt')[0]#字幕本体

"""字幕の設定関数"""
def annotate(clip, txt, txt_color='black', fontsize=50, font='Xolonium-Bold'):
    #Writes a text at the bottom of the clip. 
    txtclip = editor.TextClip(txt, fontsize=fontsize, font=font, color=txt_color)
    cvc = editor.CompositeVideoClip([clip, txtclip.set_pos(('center', 'bottom'))])
    return cvc.set_duration(clip.duration)

video = VideoFileClip(file_path)


text_file = open(text_path, "r")
lasttime = 0
subtitles = []
for line in text_file:
	linesegment = line.split()
	if len(linesegment) == 1:
		subtitles.append(((lasttime, float(linesegment[0])), ' '))
	else:
		subtitles.append(((lasttime, float(linesegment[0])), linesegment[1]))
	lasttime = float(linesegment[0])

annotated_clips = [annotate(video.subclip(from_t, to_t), txt) for (from_t, to_t), txt in subtitles]#動画と字幕を繋げる処理
final_clip = editor.concatenate_videoclips(annotated_clips)
final_clip.write_videofile("movie_withSubtitle.mp4")