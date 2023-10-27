import discord
import math
from ficha import *
import pickle
from lista_e_dicionarios import *
from random import randint as random
from discord.ext.commands.core import cooldown
from service import *
from discord.ui import Select, View
from discord.ext import commands
from discord import app_commands
from nextcord import Embed, Member, Intents

id_do_servidor = 1163451326190080040  #Coloque aqui o ID do seu servidor
TOKEN = 'MTE2MzQ1MTEyNzA5MDY1MTE2Ng.GEybw5.qss2qWLUgicKJGGlpI_Uuh-u8rn-eAY1PeuCDY'

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="sudo ", intents=intents)


class client(discord.Client):

  def __init__(self):
    super().__init__(intents=discord.Intents.default())
    self.synced = False  #Nós usamos isso para o bot não sincronizar os comandos mais de uma vez

  async def on_ready(self):
    await self.wait_until_ready()
    if not self.synced:  #Checar se os comandos slash foram sincronizados
      await tree.sync(
          guild=discord.Object(id=id_do_servidor)
      )  # Você também pode deixar o id do servidor em branco para aplicar em todos servidores, mas isso fará com que demore de 1~24 horas para funcionar.
      self.synced = True
    print(f"Entramos como {self.user}.")


aclient = client()
tree = app_commands.CommandTree(aclient)


@tree.command(guild=discord.Object(id=id_do_servidor),
              name='roll_damage',
              description='Roda dano')
async def roll_dano(interaction: discord.Interaction,
                    dado: str = None,
                    qnt_tiros: int = 1):

  await interaction.response.send_message(
      f"{mostrar_sistema_dano(dado,qnt_tiros)}")


@tree.command(
    guild=discord.Object(id=id_do_servidor),
    name='roll_attack',
    description=
    'Mostrar todas as etapas do ataque. Com o modo red ativo a dificuldade sera ( REF + Esquiva + 1d10 )'
)
async def roll_ataque(interaction: discord.Interaction,
                      dificuldade: int = 0,
                      proficiencia_mais_atributo: int = 0,
                      qnt_tiros: int = 1,
                      dado_dano: str = '1d6',
                      red: bool = True,
                      mostra_dano: bool = True,
                      info_mestre: bool = False):

  view = ''
  view_inimigo = ''
  r_dado_inimigo = 0
  tiros_acertados = 0
  print_tiros = 'Tiros Acertados'

  # Cyberpunk Red
  if red:
    r_dado_inimigo += random(1, 10)
    if info_mestre:
      view += f"**Resultado do Dado Inimigo**: {r_dado_inimigo}\n\n"
    if r_dado_inimigo == 10:
      r_dado_inimigo, view_inimigo = mostrar_critico(r_dado_inimigo, view)

    dificuldade += r_dado_inimigo
    if info_mestre: view += view_inimigo

  #Rola dado
  r_dado = random(1, 10)
  view += f"**Resultado do Dado**: {r_dado}\n\n"
  #Critico
  if r_dado == 10:
    r_dado, view = mostrar_critico(r_dado, view)

  if r_dado == 1:
    view += '**FALHA CRITICA**'

  resultado = proficiencia_mais_atributo + r_dado

  if qnt_tiros == 1:
    if resultado >= dificuldade:
      view += f"{print_tiros}: 1"
    else:
      view += f"Errou"
  elif qnt_tiros == 3:
    resultado += 3
    if resultado >= dificuldade:
      tiros_acertados = math.ceil((random(1, 6)) / 2)
      view += f"{print_tiros}: {tiros_acertados} "
    else:
      view += f"Errou"
  else:

    if resultado >= dificuldade:

      tiros_acertados = resultado - dificuldade

      if tiros_acertados == 0: tiros_acertados = 1

      view += f"{print_tiros}: {tiros_acertados}"
    else:
      view += f"Errou"

  if info_mestre:
    view += f'\n\n**Resultado Final**\nResultado {resultado} vs Dificuldade {dificuldade}\n'

  if mostra_dano == True:
    view += mostrar_sistema_dano(dado_dano, tiros_acertados)

  await interaction.response.send_message(view, ephemeral=info_mestre)


@tree.command(guild=discord.Object(id=id_do_servidor),
              name='roll_default_enemy',
              description='Rolagem de dado contram um inimigo')
async def roll_normal_vs_inimigo(interaction: discord.Interaction,
                                 dificuldade: int = 0,
                                 atributo: int = 2,
                                 proficiencia: int = 0,
                                 info_mestre: bool = False):
  view = ''
  view_inimigo = ''
  dado = random(1, 10)
  dado_inimigo = random(1, 10)
  view += f'**Resultado do Dado**: {dado}\n\n'
  if info_mestre: view += f'**Resultado inimigo**: {dado_inimigo}\n\n'

  if dado == 10:
    dado, view = mostrar_critico(dado, view)

  if dado_inimigo == 10:
    if info_mestre: view += f'**INIMIGO**\n'
    dado_inimigo, view_inimigo = mostrar_critico(dado_inimigo, view)
    if info_mestre: view += view_inimigo

  resultado_final = dado + proficiencia + atributo
  resultado_final_inimigo = dado_inimigo + dificuldade
  if info_mestre:
    view += f'**Resultado Final**\nResultado {resultado_final} vs Dificuldade {resultado_final_inimigo}\n'

  if resultado_final >= resultado_final_inimigo:
    view += '\n**PASSOU!!** :D'
  else:
    view += '\n**NÃO PASSOU** :x'

  await interaction.response.send_message(view, ephemeral=info_mestre)


@tree.command(guild=discord.Object(id=id_do_servidor),
              name='roll_default',
              description='Rolagem de dado para fazer algo.')
async def roll_normal(interaction: discord.Interaction,
                      dificuldade: int = 0,
                      atributo: int = 2,
                      proficiencia: int = 0,
                      info_mestre: bool = False):
  view = ''
  dado = random(1, 10)
  view += f'**Resultado dado**: {dado}\n\n'

  if dado == 10:
    dado, view = mostrar_critico(dado, view)
  resultado_final = dado + atributo + proficiencia
  if info_mestre:
    view += f'\n**Resultado Final**\nResultado {resultado_final} vs Dificuldade {dificuldade}\n'

  if resultado_final >= dificuldade:
    view += '\n**PASSOU!!** :D'
  else:
    view += '\n**NÃO PASSOU** :x'

  await interaction.response.send_message(view, ephemeral=info_mestre)


@tree.command(guild=discord.Object(id=id_do_servidor),
              name='takes_damage',
              description='Mostra quando de dano voce recebeu.')
async def roll_leva_dano(interaction: discord.Interaction,
                         armadura: str = '',
                         dano_localizado: str = ''):

  view = ''
  armadura_completa = armadura.split()
  dano_localizado = dano_localizado.split()

  dano_levado = 0

  for i, a in enumerate(armadura_completa):
    d = int(dano_localizado[i])
    arm = int(a)
    if d > arm:
      dano = d - arm

      if locais_corpo()[i] == 'Cabeça': dano *= 2

      if dano >= 8:
        view += f'**{locais_corpo()[i]}** JÁ ERA *pof* 💀💥\n'

      dano_levado += dano

  view += 'Dano = ' + str(dano_levado)

  await interaction.response.send_message(view)

aclient.run(TOKEN)