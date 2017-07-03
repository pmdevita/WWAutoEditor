import numpy
from PIL import Image
from moviepy.editor import *
from moviepy.video.fx.all import crop

clip = ImageClip("testimage.png")
clip = clip.set_duration(10).set_fps(10)

clip.write_videofile("testimage.mp4")

