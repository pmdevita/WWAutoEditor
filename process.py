from moviepy.editor import *
from moviepy.video.fx.all import crop

def crossfade(clip1, clip2, duration):
    """
    Merges clips into one clip with a crossfade of the specified duration (seconds)
    :param clip1:
    :param clip2:
    :return: MoviePy clip
    """
    if clip1.fps != clip2.fps:
        if round(clip1.fps) == round(clip2.fps):
            fps = round(clip1.fps)
        return CompositeVideoClip([clip1.set_fps(fps), clip2.set_fps(fps).set_start(clip1.end - duration).crossfadein(duration)])
    print(clip1.fps, clip2.fps)
    return CompositeVideoClip([clip1, clip2.set_start(clip1.end - duration).crossfadein(duration)])



vid1 = VideoFileClip("yee.mp4")
vid2 = VideoFileClip("shot.mp4")

crossfade(vid1, vid2, 3).write_videofile("fade.mp4")