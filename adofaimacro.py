from adofai import ADOFAI
import json
import keyboard
import time
import sys

def autoplay(levelpath):
    with open(levelpath, 'r') as f:
        ctx = json.load(f)
    settings = ctx['settings']
    bpm = settings['bpm']
    offset = settings['offset']
    pathdata = ctx['pathData']
    realdata = []
    
    action = ctx['actions']
    speedData = {}
    twirlData = {}

    for act in action:
        event = act['eventType']
        floor = act['floor']
        if event == 'SetSpeed':
            speedData[floor] = act['beatsPerMinute']
        elif event == 'Twirl':
            twirlData[floor] = 'Twirl'

    key = list("RWHQGqUoTEJpRAMCBYDVFZNxL")
    tileInfo = {key[i] : 15*i for i in range(len(key))}

    print(speedData, twirlData)

    idx = 0
    before = 180
    twirl = False
    isMidspin = False
    isNextOf = False
    while idx < len(pathdata):
        event = twirlData.get(idx, None)
        if not event is None: twirl = not twirl

        isMidspin = False
        if idx != len(pathdata)-1:
            isMidspin = pathdata[idx+1] == '!'
        if isNextOf: idx += 1

        angle = 0
        prev = tileInfo[pathdata[idx]]
        if isNextOf:
            angle = (prev-before)%360
        else:
            angle = (180-before+prev)%360
        realangle = angle if not twirl else 360-angle
        realdata.append(realangle)
        
        before = prev
        isNextOf = isMidspin
        idx += 1

    print(realdata)
    
    macro = ADOFAI(bpm, realdata, offset, speedData)
    macro.startMacro()

while True:
    try:
        if keyboard.is_pressed('p'):
            print("p")
            #time.sleep(0.4)
            autoplay('C:/Users/82105/Downloads/autoplay/ADOFAI-Autoplayer-main/MPP Renew.adofai')
            time.sleep(0.1)
        elif keyboard.is_pressed('esc'):
            sys.exit()
    except:
        pass
