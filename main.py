import numpy
import math
from PIL import Image
from moviepy.editor import *
# from moviepy.video.fx.all import crop

videopath = "L:/originals/WindWakerT3P2.mpg"

#videopath = "C:/Users/Peter/Videos/Film/Wind Waker/AutoFade/testimage.mp4"

video = VideoFileClip(videopath)

#croppedvideo = crop(video, x1=28, y1=76, width=660, height=344)

lookahead = False
findingend = False
previouscutscene = False
lastframes = []
skip = 0
cutscenes = []
cutscene_frame_counter = 0
ingame_frame_counter = 0

# Constants related to the video

framewidth = 720

# top line that is always black during cutscene
topxstart = 184
topxend = 520
# remember, pixels start at 0
topy = 50
# this is not as black as the first line due to artifacts. not as easy to trust
topy2 = 66

# define r for first two checks
# use this formula: d >= sqrt(r^2 + g^2 + b^2)
d1 = 10
d2 = 12

def ispixelblack(array1, d):
    return d >= math.sqrt(array1[0]^2 + array1[1]^2 + array1[2]^2)

def dumpframe(frame, filename="test.png"):
    print("Dumped frame")
    img = Image.fromarray(frame)
    try:
        img.save(filename)
    except PermissionError:
        pass


for frame in video.iter_frames(with_times=True):
    #frame[0] - timestamp, frame[1] - pixel array
    # frame[1][y][x] (from top left corner)

    # skip to 3 minutes in
    if frame[0] < 6 * 60 + 10:
        continue
    # if frame[0] > 8 * 60 + 36:
    #     dumpframe(frame[1])
    #     null = input()

    if not lookahead or findingend:
        # print time of current frame
        print(str(int((frame[0] - frame[0]%60) / 60)) + ":" + str(frame[0]%60))

        # Check if current frame meets conditions for being in cutscene

        iscutscene = True

        # Check if frame has correct black bars

        avg = numpy.mean(frame[1][topy][topxstart:topxend], axis=0)
        if not ispixelblack(avg, d1):
            print("1 Not a cutscene because pixel", "is not black:", avg)
            iscutscene = False
            # break
        else:
            print("1 Passed", avg)

        #Check closer line
        avg = numpy.mean(frame[1][topy2][topxstart:topxend], axis=0)
        if not ispixelblack(avg, d2):
            print("2 Not a cutscene because pixel", "is not black:", avg)
            # if iscutscene:
            #     dumpframe(frame[1])
            #     null = input()
            iscutscene = False
            #break
        else:
            print("2 Passed", avg)



        # if frame is a cutscene frame, dump it
        if iscutscene:
            avg = numpy.mean(frame[1], axis=(0, 1))
            if ispixelblack(avg, d2):
                print("3 Not a cutscene because pixel", "is not black:", avg)
                iscutscene = False
            else:
                print("3 Passed", avg)

        # if frame is a cutscene frame
        if iscutscene:
            # check if last ingame frame was just a blip
            if cutscene_frame_counter == 0 and ingame_frame_counter <= 1 and len(cutscenes) > 0:
                print("Seems like last frame was a blip, added to cutscene")
                cutscene_frame_counter = cutscenes[len(cutscenes) - 1][2] + ingame_frame_counter
                ingame_frame_counter = 0
            elif cutscene_frame_counter == 0:
                cutscenes.append([frame[0], None, None])
                ingame_frame_counter = 0
                cutscene_frame_counter = 0
            cutscene_frame_counter += 1

            print("cutscene frame counter", cutscene_frame_counter)
            # you can type in a number and it will skip that many frames
            if not skip:
                dumpframe(frame[1])
                previouscutscene = True
                skip = input()
                try:
                    skip = int(skip)
                except:
                    pass
            if type(skip) == int:
                skip -= 1
        # if frame is ingame but last frame was cutscene
        elif previouscutscene:
            cutscenes[len(cutscenes) - 1][1] = frame[0]
            cutscenes[len(cutscenes) - 1][2] = cutscene_frame_counter
            previouscutscene = False
            print("Did not detect cutscene", "cutscene frame counter", cutscene_frame_counter)
            ingame_frame_counter = 1
            cutscene_frame_counter = 0

            skip = 0
            newframe = numpy.copy(frame[1])
            for i in newframe[topy][topxstart:topxend]:
                i[0] = 255
                i[1] = 255
                i[2] = 255
            for i in newframe[topy2][topxstart:topxend]:
                i[0] = 255
                i[1] = 255
                i[2] = 255
            dumpframe(newframe, "test2.png")
            dumpframe(frame[1])
            null = input()
        # if frame is ingame
        else:
            ingame_frame_counter += 1



    # Manage frame stack
    lastframes.insert(0, frame)
    if len(lastframes) > 20:
        lastframes.pop()