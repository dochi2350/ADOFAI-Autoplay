from io import BufferedRandom
from pynput.keyboard import Key, Controller
import time, json

class ADOFAI:
    def __init__(self, bpm = 0, pathdata = 'RRRRRRRR', offset = 0, bpmdata = {}, twirldata = {}):
        self.kb = Controller()
        self.bpm = bpm
        key = list("RWHQGqUoTEJpRAMCBYDVFZNxL")
        self.tileInfo = {key[i] : 15*i for i in range(len(key))}
        self.pathdata = self.tileanalyze(pathdata)
        self.bpmdata = bpmdata
        self.twirldata = twirldata
        self.sec = 60/bpm
        self.offset = offset/1000
        self.length = len(self.pathdata)
        self.twirled = 0
        print("init")

    def tileanalyze(self, pathdata):
        processed = []
        for i in range(len(pathdata)-1):
            nowtile  = self.tileInfo[pathdata[i]]
            nexttile = self.tileInfo[pathdata[i+1]]
            #### TODO : 실험 안해봄 ####
            angle = 180 - nowtile + nexttile
            #### TODO : 실험 안해봄 ####
            processed.append(angle)
        #TODO : Processing Midspin Tile
        return processed + [self.tileInfo[pathdata[-1]]]
    
    def startMacro(self):
        print(self.bpmdata)
        print(self.twirldata)
        #print(self.tileInfo)
        #print(self.pathdata)
        
        print("[Start] BPM : " + str(self.bpm))
        self.kb.press('p')
        self.kb.release('p')
        time.sleep(self.offset + 3 * self.sec + 1.25)
        
        tile = 0
        while tile < self.length:
            self.kb.press('k')
            self.kb.release('k')
            
            bpmcheck = self.bpmdata.get(tile, None)
            twirlcheck = self.twirldata.get(tile, None)
            if isinstance(bpmcheck, int):
                print("[ChangeBPM] BPM : " + str(self.bpm) + "=>" + str(bpmcheck) + "(" + str(tile + 1) + ")")
                self.bpm = bpmcheck
                self.sec = 60/bpmcheck
            if isinstance(twirlcheck, str):
                print("tile twirl")
                self.twirled = 1 - self.twirled
            
            tile += 1
            
            self.wait(tile)
            print(self.pathdata[tile], (360*self.twirled + (-2*self.twirled+1) * self.pathdata[tile]) / 180 * self.sec)

    def wait(self, tile):
        delay = (360*self.twirled + ((-2)*self.twirled+1) * self.pathdata[tile]) / 180
        time.sleep(delay*self.sec)
