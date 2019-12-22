import os, subprocess, re, json
from tkinter import messagebox

class CFGfile(object):

    def __init__(self, path, episodeList):
        
        self.isExpection = False
        self.path = path
        self.episodeNumbers = set({})
        self.episodeList = episodeList
        self.episodeInfoList = []
        self.exe = os.getcwd() + os.sep + 'exiftool' + os.sep + 'exiftool.exe'

        print(self.exe)
    
    def getEpisodesNnumbers(self):

        for number in self.episodeList:
            x = re.findall('\\d+', number[:-1])
            if x:
                self.episodeNumbers.add(int(''.join(x)))

    def getEpisodeInfo(self, names, season):

        for number, name in enumerate(names, 1):
            
            if number in self.episodeNumbers:

                input_file = self.path + 'episodio-' + str(number) + '.mp4'
                
                process = subprocess.Popen([self.exe, input_file], shell = True, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.STDOUT, universal_newlines = True)
                    
                info = {}

                for output in process.stdout:

                    if output == 'The system cannot find the path specified.\n':
                        raise FileNotFoundError(self.exe + ' não encontrado')

                    if re.search(('(Media Duration|Source Image Height)'), output):
                        string = re.split(':', output, maxsplit = 1)
                        info[string[0].strip()] = string[1].strip()

                episodeData = {'temporada' : season + 1, 'episodio' : number, 'nome' : name, 'duracao' : info['Media Duration'][2:], 'thumb' : 'thumb-' + str(number) + '.png', 'qualidade' : info['Source Image Height'] + 'p' }
                self.episodeInfoList.append(episodeData)

    def getEpisodeInfoList(self):

        return self.episodeInfoList

    def setCfgFile(self, path, jsonList):
        
        with open(path + 'config.cfg', 'w', encoding = 'utf-8') as cfg:

            for info in jsonList:
                cfg.write(json.dumps(info, ensure_ascii = False))
                cfg.write('\n')
    
    def epsodeNameVerify(self):

        return all([re.search('\\bepisodio-\\d+[.]mp4\\b', j) for j in self.episodeList])