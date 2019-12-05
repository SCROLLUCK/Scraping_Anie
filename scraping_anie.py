import bs4 as bs
import urllib.request, re, json, os, subprocess

url = 'https://www.crunchyroll.com/pt-br/my-hero-academia'
# diretorio_anime = 'C:\\Users\\lucas\\Desktop\\GUARDA_TRECO(L)\\rouba_info\\asobi_teste\\'
# exe = 'C:\\Users\\lucas\\Desktop\\GUARDA_TRECO(L)\\rouba_info\\exiftool\\exiftool.exe'
diretorio_anime = 'F:\\Documentos\\AnieZillaProject\\videoTests\\'
exe = 'F:\\Documentos\\AnieZillaProject\\exiftool\\exiftool.exe'

AbaEscolhida = 0 # crunchyroll fudendo o batalhão, valor: 0 as abas estão corretas no site
TemporadaReal = 1

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

temporadas = soup.find_all('li', class_ = 'season')[::-1] # lista de temporadas

if AbaEscolhida == 0:
    AbaEscolhida = TemporadaReal

temporadas = temporadas[AbaEscolhida - 1]

divs = temporadas.find_all('div', class_ = 'wrapper container-shadow hover-classes')
for div in divs: #Remove Episodios Especias da Lista de Episódios
    spans = div.find_all('span', class_ = 'block')
    if any([i for i in spans if re.search('\\bEpisódio (SP|\\d+.\\d+)\\b', str(i))]):
        div.a.decompose()

nomes = temporadas.find_all('img')[::-1] #pega nomes dos episodios e deixa em ordem crescente

with open(diretorio_anime + 'episodios.cfg', 'w', encoding = 'utf-8') as cfg:

    for episodio, nome in enumerate(nomes, 1):

        if episodio in NumeroEpisodios: # Se o episodio atual é um episodio que foi baixado, pega as 
            
            print(TemporadaReal,'-', episodio, nome.get('alt'))

            input_file = diretorio_anime + 'episodio-' + str(episodio) + '.mp4'
            process = subprocess.Popen([exe, input_file], stdout = subprocess.PIPE, stderr = subprocess.STDOUT, universal_newlines = True)
            
            info = {}
            for output in process.stdout:

                if re.search(('(Media Duration|Source Image Height)'), output):
                    string = re.split(':', output, maxsplit = 1)
                    info[string[0].strip()] = string[1].strip()

            dados_ep = {'temporada' : TemporadaReal, 'episodio' : episodio, 'nome' : str(nome.get('alt')), 'duracao' : info['Media Duration'][2:], 'thumb' : 'thumb-'+ str(episodio) + '.png', 'qualidade' : info['Source Image Height'] + 'p' }
            dados_like_json = json.dumps(dados_ep, ensure_ascii = False).encode('utf8')
            cfg.write(dados_like_json.decode())
            cfg.write('\n')
