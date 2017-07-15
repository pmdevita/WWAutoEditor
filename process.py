import json
import subprocess

videopath = "L:/originals/WindWakerT3P2.mpg"
output = "test.mp4"

command = ["ffmpeg", "-i", videopath, "-threads:v:0", "4", "-filter_complex"]
header_command = "[0:v] split [pmain][pcs];[pmain] pad=960:ih:(ow-iw)/2:(oh-ih)/2 [main];[pcs] crop=660:352:30:68,scale=900:480,split="
split_command = ""
fade_command = ""
overlay_command = ""


fade_length = 6


with open("cutscenes.json", "r") as f:
    cutscene_data = json.load(f)

fade_counter = -1
for i in cutscene_data:
    if i[2] >=40:
        fade_counter += 1
        # fade in
        split_command = split_command + "[cs" + str(fade_counter) + "]"
        fade_command = fade_command + "[cs" + str(fade_counter) + "]"
        fade_command = fade_command + \
                         "fade=in:" + str(i[0] - fade_length) + ":" + \
                       str(fade_length) + ":alpha=1, "
        # fade out
        fade_command = fade_command + \
                         "fade=out:" + str(i[1]) + ":" + \
                       str(fade_length) + ":alpha=1 "
        fade_command = fade_command + "[fcs" + str(fade_counter) + "];"
split_command = header_command + str(fade_counter + 1) + " " + split_command + ";"

if fade_counter == 0:
    overlay_command = "[main][fcs0] overlay=0:0"
else:
    overlay_command = "[fcs0][fcs1] overlay=0:0 [ocs0];"
    for i in range(fade_counter - 1):
        overlay_command = overlay_command + "[ocs" + str(i) + "][fcs" + str(i + 2) + "] overlay=0:0 [ocs" + str(i + 1) + "];"
    overlay_command = overlay_command + "[main][ocs" + str(fade_counter - 1) + "] overlay=(W-w)/2:0"


final_filter_command = split_command + fade_command + overlay_command
#fade_command = fade_command + "crop=660:440:29:20 [csfade]; [main][csfade] overlay=0:0"
print(final_filter_command)
command.append(final_filter_command)
command.append(output)

commandstr = ""
for i in command:
    commandstr = commandstr + i + " "

print(commandstr)