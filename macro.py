from pynput.keyboard import Key, Controller
from adofai import ADOFAI
import time, json

def autoplay(levelpath):
    print("autoplay start")
    with open(levelpath, encoding='utf-8-sig') as f:
        ctx = json.loads(f.read())
    settings = ctx['settings']
    bpm = settings['bpm']
    offset = settings['offset']
    pathdata = ctx['pathData']
    action = ctx['actions']
    bpmdata = {}
    twirldata = {}
    #print(action)

    for i in range(len(action)):
        act = action[i]
        event = act['eventType']
        if event == 'SetSpeed':
            bpmdata[act['floor'] - 1] = act['beatsPerMinute']
        if event == 'Twirl':
            twirldata[act['floor'] - 1] = 'Twirl'
    
    macro = ADOFAI(bpm, pathdata, offset, bpmdata, twirldata)
    macro.startMacro()
