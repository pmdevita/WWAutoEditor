import numpy
from PIL import Image
from moviepy.editor import *
from moviepy.video.fx.all import crop

videopath = "L:/originals/WindWakerT3P2.mpg"

#videopath = "C:/Users/Peter/Videos/Film/Wind Waker/AutoFade/testimage.mp4"

video = VideoFileClip(videopath)

#croppedvideo = crop(video, x1=28, y1=76, width=660, height=344)

lookahead = False
findingend = False
previouscutscene = False
lastframes = []
skip = 0

# Constants related to the video

framewidth = 720

# top line that is always black during cutscene
topstart = 184
topwidth = 520
# remember, pixels start at 0
topy = 50
# this is not as black as the first line due to artifacts. not as easy to trust
topy2 = 66

def ispixelblack(array1, blackarray):
    return numpy.all(numpy.less(array1, numpy.array(blackarray)))

def dumpframe(frame, filename="test.png"):
    print("Dumped frame")
    img = Image.fromarray(frame)
    try:
        img.save(filename)
    except PermissionError:
        pass


for frame in video.iter_frames(with_times=True):
    # frame[1][y][x] (from top left corner)
    if frame[0] < 3 * 60 + 0:
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

        lineavg = numpy.mean(frame[1][topy][topstart:topwidth], axis=0)
        if not ispixelblack(lineavg, [10, 10.2, 10.1]):
            print("1 Not a cutscene because pixel", "is not black:", lineavg)
            iscutscene = False
            # break
        else:
            print("1 Passed", lineavg)

        #Check closer line
        lineavg = numpy.mean(frame[1][topy2][topstart:topwidth], axis=0)
        if not ispixelblack(lineavg, [10, 10.1, 13.1]):
            print("2 Not a cutscene because pixel", "is not black:", lineavg)
            # if iscutscene:
            #     dumpframe(frame[1])
            #     null = input()
            iscutscene = False
            #break
        else:
            print("2 Passed", lineavg)



        # if we have found a new cutscene, find first frame, crossfade, then set flag to
        #   begin looking for outfade
        if iscutscene:
            if not skip:
                dumpframe(frame[1])
                previouscutscene = True
                # backtrack for first frame
                # for i in lastframes:
                #     print(i[0])
                skip = input()
                try:
                    skip = int(skip)
                except:
                    pass
            if type(skip) == int:
                skip -= 1
        elif previouscutscene:
            previouscutscene = False
            print("Did not detect cutscene")
            skip = 0
            newframe = numpy.copy(frame[1])
            for i in newframe[topy2][topstart:topwidth]:
                i[0] = 255
                i[1] = 255
                i[2] = 255
            dumpframe(newframe, "test2.png")
            dumpframe(frame[1])
            null = input()



    # Manage frame stack
    lastframes.insert(0, frame)
    if len(lastframes) > 20:
        lastframes.pop()