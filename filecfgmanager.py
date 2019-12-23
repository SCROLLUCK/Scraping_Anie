import os, re, json
from cv2 import VideoCapture
from tinytag import TinyTag

class CFGfile(object):

    def __init__(self, path, episodeList):
        
        self.isExpection = False
        self.path = path
        self.episodeNumbers = set({})
        self.episodeList = episodeList
        self.episodeInfoList = []
        self.videoCaptureObject = None
        self.tagObject = None
    
    def getEpisodesNnumbers(self):

        for number in self.episodeList:
            x = re.findall('\\d+', number[:-1])
            if x:
                self.episodeNumbers.add(int(''.join(x)))

    def getEpisodeInfo(self, names, season):

        for number, name in enumerate(names, 1):
            
            if number in self.episodeNumbers:

                input_file = self.path + 'episodio-' + str(number) + '.mp4'

                self.videoCaptureObject = VideoCapture(input_file)
                self.tagObject = TinyTag.get(input_file)
                self.tagObject._get_parser_for_filename('mp4')

                duration = self.getCorretDuration()
                quality = self.videoCaptureObject.get(4)

                episodeData = {'temporada' : season + 1, 'episodio' : number, 'nome' : name, 'duracao' : duration, 'thumb' : 'thumb-' + str(number) + '.png', 'qualidade' : str(quality)[:-2] + 'p' }
                self.episodeInfoList.append(episodeData)

    def getCorretDuration(self):
        
        h = int(self.tagObject.duration / 3600)
        m = int(self.tagObject.duration % 3600 / 60)
        s = int(self.tagObject.duration % 3600 % 60)

        if h > 0:
            if h <= 9:
                return '0' + str(h) + ':' + str(m) + ':' + str(s)
        else:
            if m <= 9:
                m = '0' + str(m)
            if s <= 9:
                s = '0' + str(s)

            if not isinstance(m, str):
                m = str(m)
            if not isinstance(s, str):
                s = str(s)

            return m + ':' + s

    def getEpisodeInfoList(self):

        return self.episodeInfoList

    def setCfgFile(self, path, jsonList):
        
        with open(path + 'config.cfg', 'w', encoding = 'utf-8') as cfg:

            for info in jsonList:
                cfg.write(json.dumps(info, ensure_ascii = False))
                cfg.write('\n')
    
    def epsodeNameVerify(self):

        return all([re.search('\\bepisodio-\\d+[.]mp4\\b', j) for j in self.episodeList])