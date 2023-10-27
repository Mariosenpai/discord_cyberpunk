import math
import discord
from service import gif_aleatorio, sistema_dano
from lista_e_dicionarios import lista_gifs_acerto,lista_gifs_errou,pega_gif_acertou_usuario

def verificar_tiros_acertados(qnt_tiros:int, resultado:int,dificuldade:int):
  
  print_tiros = 'Tiros Acertados'
  errou = False
  tiros_acertados = 0
  
  if qnt_tiros == 1:
    if resultado >= dificuldade:
      tiros_acertados = 1
    else:
      errou = True
  elif qnt_tiros == 3:
    resultado += 3
    if resultado >= dificuldade:
      tiros_acertados = math.ceil((random(1, 6)) / 2)
    else:
      errou = True
  else:
  
    if resultado >= dificuldade:
  
      tiros_acertados = resultado - dificuldade
  
      if tiros_acertados == 0: tiros_acertados = 1
  
    else:
      errou = True
      
  return resultado, tiros_acertados, errou

def embed_ataque(id,errou:bool,resultado:int,ref:int, r_dado:int, proficiencia:int,
                 r_adicional:int,tiros_acertados:int,dado_dano:str ):
  
  embed = discord.Embed(
    title = "Sistema de dano"
  )
  #Mostra dados
  embed.add_field(name ="# Info Gerais",value ="",inline=False)

  #Info user
  embed.add_field(name ="Reflexo",value =f"{ref}",inline=True)
  embed.add_field(name ="Proficiencia",value =f"{proficiencia}",inline=True)

  embed.add_field(name ="Resultado Dado",value =f"{r_dado}",inline=True)
  if r_dado == 1:
    embed.add_field(name ="# FALHA CRITICA",value ="",inline=False)
  if r_dado == 10:
    embed.add_field(name ="# ACERTO CRITICO",value ='',inline=False)
    embed.add_field(name ="Rolagem Adicional",value =f"{r_adicional}",inline=True)

  embed.add_field(name ="Resultado Final",value =f"{resultado}",inline=False)
  #Mostra dados

  if not errou:
    view_dano, view_qnt_tiros = sistema_dano(dado_dano, tiros_acertados)

    # Mostra dano
    embed.add_field(name ="# Distribuição Dano ",value ="",inline=False)
    userData = {}
    for i in view_dano: 
      userData[i] = view_dano[i]

    for [fieldName, fieldVal] in userData.items():
      embed.add_field(name=fieldName, value=fieldVal, inline=True)

    embed.add_field(name ="---------------------------------------------",value ="",inline=False)
    #Locais dano
    embed.add_field(name ="# Locais do Dano",value ="",inline=False)
    userData = {}
    for i in view_qnt_tiros: 
      userData[i] = view_qnt_tiros[i]

    for [fieldName, fieldVal] in userData.items():
      embed.add_field(name=fieldName, value=fieldVal, inline=True)

    #Codigo armadura
    cont = 1
    armadura_dano = ''
    for i in view_dano:
      if cont == len(view_dano):
        armadura_dano += f'{view_dano[i]}'
        break
      armadura_dano += f'{view_dano[i]},'
      cont+=1
    #Caso o usuario ja tenha gifs cadastrados
    try:
      
      lista_gif = pega_gif_acertou_usuario(id)
      #Verificar se a lista de gif do usuario esta vazia
      #Caso esteje pega os gif padrão
      if lista_gif != []:
        embed.set_image(url= gif_aleatorio(lista_gif))
      else:
        embed.set_image(url= gif_aleatorio(lista_gifs_acerto()))
        
    except Exception as e:
      embed.set_image(url= gif_aleatorio(lista_gifs_acerto()))

    embed.set_footer(text=armadura_dano)

  else:    
    embed.add_field(name ="**Voce Errou**",value ="",inline=False)
    embed.set_image(url = gif_aleatorio(lista_gifs_errou()))

  return embed