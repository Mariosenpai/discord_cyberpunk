from random import randint as random
import pickle
import os

def dic_local_tiros():
  return {'Cabeça': 0, 'Torso': 0, 'Braço direito': 0, 'Braço esquerdo': 0, 'Perna direita': 0,
          'Perna esquerda': 0, }

def dic_ficha():
  return {"nome": '',
         "armadura": '',
         "vida": 0,
         "ref": 0,
         "int": 0,
         "tec": 0,
         "cool": 0,
         "atr": 0,
         "sort": 0,
         "mov": 0,
         "body": 0,
         "empatia": 0}

def locais_corpo():
  return ["Cabeça", "Torso", "Braço direito", "Braço esquerdo", "Perna direita", "Perna esquerda"]

def local_corpo_aleatorio():
  local = random.randint(1, 10)

  if local == 1:
      return locais_corpo()[0]
  elif local in [2, 3, 4]:
      return locais_corpo()[1]
  elif local == 5:
      return locais_corpo()[2]
  elif local == 6:
      return locais_corpo()[3]
  elif local in [7, 8]:
      return locais_corpo()[4]
  else:
      return locais_corpo()[5]

def update_arma(id_user, dic):
  with open(f'dados/arma/{id_user}.pickle', 'wb') as arquivo:
    pickle.dump(dic, arquivo)


def pega_armas(id_user):
  with open(f'dados/arma/{id_user}.pickle', 'rb') as arquivo:
    list_arma = pickle.load(arquivo)

  return list_arma

def pega_ficha(id_user):
  with open(f'dados/ficha/{id_user}.pickle', 'rb') as arquivo:
    a = pickle.load(arquivo)

  return a

def pega_proficiencia(id):
  with open(f'dados/proficiencia/{id}.pickle', 'rb')as arquivo:
    a = pickle.load(arquivo)
  return a

def lista_gifs_errou():
  lista = ''
  with open(f'dados/gifs/errou.txt','r') as arquivo:
    lista += arquivo.read()
  lista = lista.split('\n')
  return lista

def lista_gifs_acerto():
  lista = ''
  with open(f'dados/gifs/acertou.txt','r') as arquivo:
    lista += arquivo.read()
  lista = lista.split('\n')
  return lista

def adiciona_gif_usuario(id_user, url_gif):
  with open(f'dados/gifs/usuario/{id_user}.txt', 'w')as arquivo:
    arquivo.write(f'{url_gif}\n')

def deleta_gif_acertou_usuario(id_user,nova_lista):
  urls = ''
  if nova_lista != []:
    for i in nova_lista:
      urls += i + '\n'
      
  with open(f'dados/gifs/usuario/{id_user}.txt', 'w')as arquivo:
    arquivo.write(urls)

def pega_gif_acertou_usuario(id_user):
  lista = ''
  with open(f'dados/gifs/usuario/{id_user}.txt', 'r')as arquivo:
    lista += arquivo.read()
  lista = lista.split('\n')
  
  return remove_lista_vazia(lista)

def remove_lista_vazia(lista):
  aux_lista = lista
  for i in aux_lista:
    if i == '':
      lista.remove(i)
  return lista


def todas_fichas():
  pasta = 'dados/ficha'
  lista_arquivos = []
  # Verifique se o caminho da pasta é válido
  if os.path.exists(pasta):
      # Use o método listdir para obter uma lista de todos os arquivos na pasta
      arquivos = os.listdir(pasta)

      for arquivo in arquivos:
          # Verifique se o caminho completo do arquivo é um arquivo (não é um diretório)
          caminho_completo = os.path.join(pasta, arquivo)
          if os.path.isfile(caminho_completo):
            lista_arquivos.append(arquivo)
  return lista_arquivos
