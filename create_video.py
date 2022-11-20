from moviepy import editor
from moviepy.video.io.VideoFileClip import VideoFileClip
import os.path as op
import glob

# ref: https://python-climbing.com/moviepy-subtitle/

"""以下2行はwindowsユーザは書かないとおそらくエラーが出ます"""
from moviepy.config import change_settings
change_settings({"IMAGEMAGICK_BINARY": r"D:/PRO/ImageMagick/ImageMagick-7.1.0-Q16-HDRI/magick.exe"})

file_path = glob.glob("./*.mp4")[0]#字幕を付けたい動画のパス

"""字幕の設定関数"""
def annotate(clip, txt, txt_color='black', fontsize=50, font='Xolonium-Bold'):
    #Writes a text at the bottom of the clip. 
    txtclip = editor.TextClip(txt, fontsize=fontsize, font=font, color=txt_color)
    cvc = editor.CompositeVideoClip([clip, txtclip.set_pos(('center', 'bottom'))])
    return cvc.set_duration(clip.duration)

video = VideoFileClip(file_path)

#subs・・・字幕を入れる時刻と文字列のタプル。(開始時刻,終了時刻),'表示したい文字'
subs = [((0, 4), 'subs1'),
        ((5, 10), 'subs2'),
        ((10, 12), 'subs3'),
        ((12, 20), 'subs4')]#動画の長さまで字幕を設定する。途中で切られる。表示したくないときは空文字''で

annotated_clips = [annotate(video.subclip(from_t, to_t), txt) for (from_t, to_t), txt in subs]#動画と字幕を繋げる処理
final_clip = editor.concatenate_videoclips(annotated_clips)
final_clip.write_videofile("movie_withSubtitle.mp4")