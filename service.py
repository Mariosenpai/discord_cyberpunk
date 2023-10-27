import random
import re

def dic_local_tiros():
  return {'Cabeça': 0, 'Torso': 0, 'Braço direito': 0, 'Braço esquerdo': 0, 'Perna direita': 0,
          'Perna esquerda': 0, }

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


def calcular_dado(dado):
  dano = 0

  dado_de_mult = int(dado[0])
  dado_de_dano = int(dado[2:])

  for i in range(dado_de_mult):
      dano += random.randint(1, dado_de_dano)

  return dano

def sistema_dano(dado , qnt_tiros):
  dic = dic_local_tiros()
  qnt_tiros_local = dic_local_tiros()
  
  for i in range(0,qnt_tiros):
    local = local_corpo_aleatorio()
    dic[local] += rolar_dados(dado)
    qnt_tiros_local[local] += 1
    
  return dic , qnt_tiros_local


def rolar_dados(entrada):
  # Use uma expressão regular para analisar a entrada
  padrao = r'(\d+)d(\d+)([+-]\d+)?'
  match = re.match(padrao, entrada)

  if match:
      num_vezes = int(match.group(1))
      num_faces = int(match.group(2))
      modificador = match.group(3)

      resultado = 0

      for _ in range(num_vezes):
          resultado += random.randint(1, num_faces)

      if modificador:
          modificador = int(modificador)
          resultado += modificador

      return int(resultado)

  else:
      #Dado invalido
      return 0




def mostrar_dano(dic, titulo):
  view = f'-------- {titulo} ---------\n'
  for i in dic:
    view += f'{i}: {dic[i]} \n'

  return view

def mostrar_sistema_dano(dado_dano,tiros_acertados):
  view = ''
  view_dano, view_qnt_tiros = sistema_dano(dado_dano, tiros_acertados)
  view += '\n'+ mostrar_dano(view_dano,'DANO')
  view += '\n'+ mostrar_dano(view_qnt_tiros,'TIROS') +'\n'

  #Serve para copia e colar na função takes_damage
  cont = 1
  for i in view_dano:
    if cont == len(view_dano):
      view += f'{view_dano[i]}'
      break
    view += f'{view_dano[i]},'
    cont+=1
  return view

def mostrar_critico(dado, view):
  view += f"ACERTO CRITICO!\n"
  r_adicional = random.randint(1,10)
  view += f'Resultado do dado adicional: {r_adicional}\n'
  dado += r_adicional
  return dado, view,r_adicional

def gif_aleatorio(lista_gif):
  gif = random.randint(0,len(lista_gif)-1)
  return lista_gif[gif]