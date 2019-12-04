import bs4 as bs
import urllib.request
import re
import json
import os
import subprocess

url = 'https://www.crunchyroll.com/pt-br/my-hero-academia'
diretorio_anime = 'C:\\Users\\lucas\\Desktop\\GUARDA_TRECO(L)\\rouba_info\\asobi_teste\\'
exe = 'C:\\Users\\lucas\\Desktop\\GUARDA_TRECO(L)\\rouba_info\\exiftool\\exiftool.exe'
AbaEscolhida = 0 # crunchyroll fudendo o batalhão, valor: 0 as abas estão corretas no site
TemporadaReal = 1

configCFG = open(diretorio_anime +'episodios.cfg', 'w', encoding='utf-8')
sauce = urllib.request.urlopen(url).read()
soup = bs.BeautifulSoup(sauce, 'lxml')

listaArquivos = os.listdir(diretorio_anime)
pattern = "\\bepisodio+-\\d+[.]mp4\\b"
listaEpisodios = [i for i in listaArquivos if re.search(pattern, i)]
NumeroEpisodios = set({})

for string in listaEpisodios:
    x = re.findall('\\d+', string[:-1])
    if x:
        NumeroEpisodios.add(int(''.join(x)))

NumeroEpisodios
print(NumeroEpisodios) # Lista de Episodios no diretorio

temporadas = soup.find_all('li', class_='season') # lista de temporadas
temporadas = temporadas[::-1] # deixa temporadas em ordem crescente

if AbaEscolhida == 0:
    AbaEscolhida = TemporadaReal

for idy, temporada in enumerate(temporadas): #vare temporadas

    if AbaEscolhida - 1 == idy: # Se temporada atual é == a temporada escolhida, então pege as infos dos episodios

        divs = temporada.find_all('div', class_='wrapper container-shadow hover-classes')
        ignore = 'Episódio SP'
        for div in divs: #Remove Episodios Especias da Lista de Episódios
            spans = div.find_all('span', class_='block')
            for span in spans:
                if ignore in span.string:
                    div.a.decompose()

        nomes = temporada.find_all('img') #pega nomes dos episodios
        nomes = nomes[::-1] #deixa episodios em ordem crescente
        for episodio, nome in enumerate(nomes):
            if episodio + 1 in NumeroEpisodios: # Se o episodio atual é um episodio que foi baixado, pega as infos
                print(TemporadaReal,'-', episodio + 1, nome.get('alt'))
                input_file = diretorio_anime + 'episodio-' + str(episodio + 1) +'.mp4'
                process = subprocess.Popen([exe, input_file], stdout = subprocess.PIPE, stderr = subprocess.STDOUT, universal_newlines = True)
                for idx, output in enumerate(process.stdout):
                    if idx == 18 or idx == 36:
                        meta = str(output)
                        if idx == 18: #metadado referente à duração do video
                            duracao = meta[36:-1]
                        else: #metadado referente à qualidade do video
                            qualidade = meta[34:-1]

                dados_ep = {'temporada' : TemporadaReal, 'episodio' : episodio + 1, 'nome' : str(nome.get('alt')), 'duracao' : duracao,  'thumb' : 'thumb-'+ str(episodio+1) + '.png', 'qualidade' : qualidade + 'p' }
                dados_like_json = json.dumps(dados_ep, ensure_ascii=False).encode('utf8')
                configCFG.write(dados_like_json.decode())
                configCFG.write('\n')

configCFG.close()