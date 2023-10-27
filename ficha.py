import pickle
from lista_e_dicionarios import pega_armas ,update_arma
from nextcord import Embed, Member, Intents

def pega_arma_ativa(id_user):
  la = pega_armas(id_user)

  for i in la:
    if i['ativa']:
      return i
  return la[0]

def ativa_arma(nome_arma, id_user):
  la = pega_armas(id_user)

  #Ativa a arma escolhida
  for i in la:
    if i['nome'] == nome_arma:
      i['ativa'] = True
    else:
      i['ativa'] = False
      
  update_arma(id_user, la)


def cartao_info_user(userData, user,titulo):
  inline = True
  embed = Embed(title=titulo, color=0x0080ff)
  for [fieldName, fieldVal] in userData.items():
    embed.add_field(name=fieldName + ':', value=fieldVal, inline=inline)
  embed.set_footer(text=f'id: {user.id}')

  embed.set_thumbnail(user.display_avatar)

  return embed
  



