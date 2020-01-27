from constants import *
from threading import Thread
import os, re, json, subprocess
class CFGfile(object):

    def __init__(self, path, episodeList):
        
        self.quality = None
        self.duration = None
        self.isExpection = False
        self.path = path
        self.episodeNumbers = set({})
        self.episodeList = episodeList
        self.episodeInfoList = []
    
    def getEpisodesNumbers(self):

        for number in self.episodeList:
            x = re.findall('\\d+', number[:-1])
            if x:
                self.episodeNumbers.add(int(''.join(x)))

    def getEpisodeInfo(self, names, season):

        for number, name in enumerate(names, 1):
            
            if number in self.episodeNumbers:

                input_file = self.path + 'episodio-' + str(number) + '.mp4'
                
                t1 = Thread(target = self.getCorretDuration, args = (input_file, ))
                t2 = Thread(target = self.getCorretQuality, args = (input_file, ))

                t1.start()
                t2.start()

                t1.join()
                t2.join()
                
                episodeData = {'temporada' : season + 1, 'episodio' : number, 'nome' : name, 'duracao' : self.duration, 'thumb' : 'thumb-' + str(number) + '.png', 'qualidade' : str(self.quality) + 'p' }
                self.episodeInfoList.append(episodeData)

    def getCorretQuality(self, fileName):

        quality = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                                "stream=height", "-of",
                                "default=noprint_wrappers=1:nokey=1", fileName],
                                stdout = subprocess.PIPE,
                                stderr = subprocess.STDOUT, 
                                stdin = subprocess.PIPE, 
                                universal_newlines = True, shell = True)
        
        self.quality = re.split('\n', quality.stdout)[0]

    def getCorretDuration(self, fileName):

        duration = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                                "format=duration", "-of",
                                "default=noprint_wrappers=1:nokey=1", fileName],
                                stdout = subprocess.PIPE,
                                stderr = subprocess.STDOUT, 
                                stdin = subprocess.PIPE, 
                                shell = True)

        duration = float(duration.stdout)

        h = int(duration / 3600)
        m = int(duration % 3600 / 60)
        s = int(duration % 3600 % 60)
        
        if m <=9: m = '0'+str(m)
        if s <=9: s = '0'+str(s)
        time = str(m)+':'+str(s)
        
        if h > 0:
            if h <=9: h = '0' + str(h)
            time = h+':'+time
        
        return time

        if m <= 9: 
            m = '0' + str(m)
        if s <= 9: 
            s = '0' + str(s)

        duration = str(m) + ':' + str(s)

        if 0 < h <= 9: 
            duration = '0' + str(h) + ':' + duration
        
        self.duration = duration

    def getEpisodeInfoList(self):

        return self.episodeInfoList

    def setCfgFile(self, path, jsonList):
        
        with open(path + 'config.cfg', 'w', encoding = 'utf-8') as cfg:

            for info in jsonList:
                cfg.write(json.dumps(info, ensure_ascii = False))
                cfg.write('\n')
    
    def epsodeNameVerify(self):

        return all([re.search(EPISODE_NAME, j) for j in self.episodeList])