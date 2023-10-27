import discord
import math
import json
from services.combate import *
from services.define import *
from ficha import *
import pickle
from lista_e_dicionarios import *
from random import randint as random
import random
from discord.ext.commands.core import cooldown
from service import *
from discord import ui
from discord.ui import Select, View, Button
from discord.ext import commands
from discord import app_commands
from nextcord import Embed, Member, Intents, ButtonStyle

helpGuide = json.load(open('dados/help.json',encoding='utf8'))
id_do_servidor = 1163451326190080040  # Coloque aqui o ID do seu servidor

# ******************************* BOTs *******************************
TOKEN = open('token.txt').read()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="sudo ", intents=intents)
bot.remove_command("help")


# Bot para a criação das fichas
@bot.event
async def on_ready():
    # Sincronização para indentificar comandos de barra '/'
    await bot.tree.sync(guild=discord.Object(id=id_do_servidor))
    print("Bot is online")


# ******************************* BOTs *******************************


# **************************************************************
# FICHA
# **************************************************************


# FICHA
@bot.hybrid_command(name="criar", with_app_command=True, description="Cria uma ficha para o usuario")
@app_commands.guilds(discord.Object(id=id_do_servidor))
async def Criar_ficha(ctx, nome, armadura, vida, ref, inte, tec, cool, atr,
                      sort, mov, body, empatia):
    dic = dic_ficha()
    dic['nome'] = nome
    dic['armadura'] = armadura
    dic['vida'] = vida
    dic['ref'] = ref
    dic['inte'] = inte
    dic['tec'] = tec
    dic['cool'] = cool
    dic['atr'] = atr
    dic['sort'] = sort
    dic['mov'] = mov
    dic['body'] = body
    dic['empatia'] = empatia

    try:
        with open(f'dados/ficha/{ctx.message.author.id}.pickle', 'wb') as arquivo:
            pickle.dump(dic, arquivo)
        await ctx.reply('Informações Salvas com Sucesso!')
    except ():
        await ctx.reply('Erro ao criar a ficha. Porfavor tente novamente')


@bot.command(name='ficha')
async def Profile(ctx, member: discord.Member = None):
    if member == None:
        user = ctx.message.author

        id = user.id
    else:
        user = member
        id = user.id

    try:
        ficha = pega_ficha(id)

        nome = ficha['nome']
        armadura = ficha['armadura']
        vida = ficha['vida']

        ref = ficha['ref']
        inte = ficha['int']
        tec = ficha['tec']
        cool = ficha['cool']
        atr = ficha['atr']
        sort = ficha['sort']
        mov = ficha['mov']
        body = ficha['body']
        empatia = ficha['empatia']

        # Caso a arma não seja cadastrada retorna maos vazia
        try:
            arma_ativa = pega_arma_ativa(id)
            desc_arma = f'{arma_ativa["nome"]} / {arma_ativa["dado"]}'
        except:
            desc_arma = 'Mão vazia / 1d6'

        userData = {
            'Nome Jogador': user.mention,
            'Nome': nome,
            'Armadura': armadura,
            'Vida': vida,
            'Arma equipada': desc_arma,
            'Reflexo': ref,
            'Inteligencia': inte,
            'Tecnologia': tec,
            'Auto Controle': cool,
            'Atratividade': atr,
            'Sorte': sort,
            'Movimento': mov,
            'Tipo Corporal': body,
            'Empatia': empatia
        }
        embed = cartao_info_user(userData, user, nome)

        await ctx.channel.send(embed=embed)
    except ():
        await ctx.channel.send(
            "Voce ainda não tem uma Ficha. Porfavor crie uma usando a função 'ficha criar' ou use o Help para mais informações "
        )


@bot.hybrid_command(name="ficha-update", with_app_command=True, description="Atualiza um atributo escolhido na ficha")
@app_commands.guilds(discord.Object(id=id_do_servidor))
async def editar_ficha(ctx, nome_atributo: str = 'ref', novo_valor: str = ''):
    user = ctx.message.author

    id = user.id
    # Pega a ficha
    ficha = pega_ficha(id)
    ficha[nome_atributo] = novo_valor

    # Altera no arquivo o que foi escolhido
    with open(f'dados/ficha/{id}.pickle', 'wb') as arquivo:
        pickle.dump(ficha, arquivo)

    await ctx.reply('Ficha atualizada com Sucesso!!')


# FICHA


# ARMAS
@bot.hybrid_command(name="ficha-arma-add", with_app_command=True,
                    description="Adiciona uma nova arma para o personagem")
@app_commands.guilds(discord.Object(id=id_do_servidor))
async def add_arma(ctx, nome, dado_dano, descricao: str = ''):
    id = ctx.message.author.id

    try:
        with open(f'dados/arma/{id}.pickle', 'rb') as arquivo:
            list_arma = pickle.load(arquivo)
    except:
        list_arma = []

    dic = {
        'nome': nome,
        'dado': dado_dano,
        'descricao': descricao,
        'ativa': False
    }

    list_arma.append(dic)

    update_arma(id, list_arma)

    await ctx.reply("Arma adicionada com Sucesso")


@bot.command(name='ficha-arma')
async def seleciona_arma(ctx):
    id = ctx.message.author.id

    list_arma = pega_armas(id)

    # Informações do usuario
    userData = {
        'Nome Jogador': ctx.message.author.mention,
    }
    embed = cartao_info_user(userData, ctx.message.author, 'Armas')

    # Lista de armas
    view = View()
    option = []
    for a in list_arma:
        option += [
            discord.SelectOption(label=a['nome'], emoji='🔫', description=a['dado'])
        ]

    # Coloca no select todas as armas
    select = Select(placeholder='Armas', options=option)
    view.add_item(select)

    # Seleciona uma arma tornara ela ativa
    async def my_callback(interaction):
        nome_arma = select.values[0]
        ativa_arma(nome_arma, id)
        await interaction.response.send_message(f'Arma {nome_arma} ativa.')

    select.callback = my_callback

    await ctx.channel.send(embed=embed, view=view)


# ARMAS

# **************************************************************
# FICHA
# **************************************************************


# ******************************* SISTEMAS *******************************


# **************************************************************
# DIFICULDADE
# **************************************************************


# MOSTRA DIFICULDADE
@bot.command(name='difficulty')
async def pega_dificultade(ctx):
    d = pega_dificuldade()
    await ctx.channel.send(f'Dificuldade = {d}')


# DEFINIR DIFICULDADE
@bot.command(name='define-difficulty')
async def definir_dificuldade(ctx, dificuldade):
    with open(f'dados/dificuldade.pickle', 'wb') as arquivo:
        pickle.dump(dificuldade, arquivo)

    await ctx.channel.send(f'Dificuldade alterada para {dificuldade}')


def pega_dificuldade():
    try:
        ar = 0
        with open(f'dados/dificuldade.pickle', 'rb') as arquivo:
            ar = pickle.load(arquivo)
    except:
        return 'Dificuldade não cadastrada'

    return int(ar)


# **************************************************************
# DIFICULDADE
# **************************************************************

# **************************************************************
# PROFICIENCIA
# **************************************************************

@bot.command(name='define-proficiency-attack')
async def definir_proficiencia_ataque(ctx, proficiencia: int = 0):
    id = ctx.message.author.id
    nome = 'attack'
    # Se o arquivo não existir ele cria o arquivo
    try:
        with open(f'dados/proficiencia/{id}.pickle', 'rb') as arquivo:
            a = pickle.load(arquivo)
            a[nome] = proficiencia
            pickle.dump(a, arquivo)
    except:
        dic = {nome: proficiencia}
        with open(f'dados/proficiencia/{id}.pickle', 'wb') as arquivo:
            pickle.dump(dic, arquivo)

    await ctx.send("Proficiencia Definida com Sucesso!")


# **************************************************************
# PROFICIENCIA
# **************************************************************


# **************************************************************
# DEFINIR
# **************************************************************

@bot.hybrid_command(name="define-url-attack", with_app_command=True,
                    description="Adiciona um gif na rolagem de attack caso acerte")
@app_commands.guilds(discord.Object(id=id_do_servidor))
async def definir_url_attack(ctx, url: str = ''):
    adiciona_gif_usuario(ctx.message.author.id, url)

    await ctx.defer(ephemeral=True)
    await ctx.reply("Url definida com Sucesso!")


@bot.hybrid_command(name="delete-url-attack", with_app_command=True, description="Deleta uma das urls de attack")
@app_commands.guilds(discord.Object(id=id_do_servidor))
async def deleta_url_attack(ctx):
    id = ctx.message.author.id
    view = View()
    # embed
    userData = {
        'Nome Jogador': ctx.message.author.mention,
    }
    embed = cartao_info_user(userData, ctx.message.author, 'URLs')

    lista = pega_gif_acertou_usuario(id)
    option = []
    for a in lista:
        option += [
            discord.SelectOption(label=a)
        ]

    # Coloca no select todas as armas
    select = Select(placeholder='URLs', options=option)
    view.add_item(select)

    # Seleciona uma arma tornara ela ativa
    async def my_callback(interaction):
        url = select.values[0]
        # deleta url
        if deleta_url(url, lista, id):
            await interaction.response.send_message(f'Url Deleta com Sucesso!', ephemeral=True)

    select.callback = my_callback

    await ctx.channel.send(embed=embed, view=view)


# **************************************************************
# DEFINIR
# **************************************************************

# **************************************************************
# COMBATE
# **************************************************************

@bot.hybrid_command(name="initiative", with_app_command=True, description="Gera a iniciativa para todos")
@app_commands.guilds(discord.Object(id=id_do_servidor))
async def iniciativa(ctx):
    id_master = ctx.message.author.id

    id_master_static = 208419266607710210
    # Caso seja o id do mestre no caso EU ai a iniciativa irar funcionar
    if id_master == id_master_static:

        valores = []
        iniciativa = {}

        lista_ficha = todas_fichas()

        for i in lista_ficha:
            if i == f'{id_master_static}.pickle':
                lista_ficha.remove(i)
                break

        for i in lista_ficha:
            with open(f'dados/ficha/{i}', 'rb') as arquivo:
                a = pickle.load(arquivo)

            ref = a['ref']
            dado = random.randint(1, 10)
            resultado = int(ref) + dado
            iniciativa['nome'] = a['nome']
            iniciativa['iniciativa'] = resultado
            valores.append(iniciativa)
            iniciativa = {}

        valores_order = sorted(valores, key=lambda x: x['iniciativa'])

        embed = discord.Embed(
            title="Iniciativa"
        )
        for i in valores_order:
            # Mostra dados
            embed.add_field(name=f"{i['nome']}", value=f"{i['iniciativa']}", inline=False)

        await ctx.reply(embed=embed)
    else:
        await ctx.reply("Voce não é o Mester!!")


# ATAQUE
@bot.hybrid_command(name="attack", with_app_command=True, description="Executa um ataque contra um npc")
@app_commands.guilds(discord.Object(id=id_do_servidor))
async def ataca(ctx,
                qnt_tiros: int = 1,
                proficiencia_: int = -1,
                dado_dano: str = '',
                bonus: int = 0,
                red=True):
    # ID usuario
    id = ctx.message.author.id

    # Variaveis
    view = ''
    view_inimigo = ''
    r_dado_inimigo = 0
    tiros_acertados = 0
    resultado = 0
    print_tiros = 'Tiros Acertados'
    red = True
    errou = False

    # Dificuldade
    dificuldade = 0
    dificuldade = pega_dificuldade()
    if red: dificuldade += random.randint(1, 10)

    proficiencia = 0
    try:
        # Se a proficiencia não existir usa a que foi passada
        if proficiencia_ == -1:
            proficiencia = pega_proficiencia(id)['attack']

        # Se o dado não for especificado ele pega o dado que esta na ficha
        if dado_dano == '': dado_dano = pega_arma_ativa(id)['dado']
    except Exception as e:
        pass

    # Pega informações da ficha
    ficha = pega_ficha(id)
    ref = ficha['ref']

    proficiencia_mais_atributo = int(ref) + proficiencia

    # Cyberpunk Red
    if red:
        r_dado_inimigo += random.randint(1, 10)
        if r_dado_inimigo == 10:
            r_dado_inimigo, view_inimigo, _ = mostrar_critico(r_dado_inimigo, view)

        dificuldade += r_dado_inimigo

    # Rola dado
    r_adicional = 0
    r_dado = random.randint(1, 10)
    resultado = proficiencia_mais_atributo + r_dado + bonus
    if r_dado == 10:
        r_adicional = random.randint(1, 10)
    # Tiros
    resultado, tiros_acertados, errou = verificar_tiros_acertados(qnt_tiros, resultado, dificuldade)

    embed = embed_ataque(id, errou, resultado, ref, r_dado, proficiencia, r_adicional, tiros_acertados, dado_dano)

    await ctx.reply(embed=embed)


# ATAQUE
@bot.hybrid_command(name="attack-master", with_app_command=True,
                    description="Executa a ação de ataque contra um jogador")
@app_commands.guilds(discord.Object(id=id_do_servidor))
async def ataca_mestre(ctx,
                       qnt_tiros: int = 1,
                       ref: int = 2,
                       proficiencia: int = 0,
                       dificuldade: int = 0,
                       dado_dano: str = '1d6'):
    # Variaveis
    view = ''
    view_inimigo = ''
    r_dado_inimigo = 0
    tiros_acertados = 0
    resultado = 0
    print_tiros = 'Tiros Acertados'
    red = True
    info_mestre = True

    proficiencia_mais_atributo = ref + proficiencia

    # Cyberpunk Red
    if red:
        r_dado_inimigo += random.randint(1, 10)
        if info_mestre:
            view += f"**Resultado do Dado Inimigo**: {r_dado_inimigo}\n\n"
        if r_dado_inimigo == 10:
            r_dado_inimigo, view_inimigo = mostrar_critico(r_dado_inimigo, view)

        dificuldade += r_dado_inimigo
        if info_mestre: view += view_inimigo

    # Rola dado
    r_dado = random.randint(1, 10)
    view += f"**Resultado do Dado**: {r_dado}\n\n"
    # Critico
    if r_dado == 10:
        r_dado, view = mostrar_critico(r_dado, view)

    if r_dado == 1:
        view += '**FALHA CRITICA**'

    resultado = proficiencia_mais_atributo + r_dado

    # Tiros
    if qnt_tiros == 1:
        if resultado >= dificuldade:
            tiros_acertados = 1
            view += f"{print_tiros}: 1"
        else:
            view += f"Errou"
    elif qnt_tiros == 3:
        resultado += 3
        if resultado >= dificuldade:
            tiros_acertados = math.ceil((random.randint(1, 6)) / 2)
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

    view += mostrar_sistema_dano(dado_dano, tiros_acertados)

    await ctx.defer(ephemeral=True)
    await ctx.reply(view)


# **************************************************************
# COMBATE
# **************************************************************

# **************************************************************
# LEVA DANO
# **************************************************************

@bot.hybrid_command(name="damage", with_app_command=True, description="Calcula o dano")
@app_commands.guilds(discord.Object(id=id_do_servidor))
async def leva_dano(ctx, dano, armadura: str = ''):
    id = ctx.message.author.id

    lista_dano = dano.split(',')

    # Se a armadura não foi especificada entao use a armadura do usuario
    if armadura == '':
        armadura = pega_ficha(id)['armadura']

    armadura = armadura.split(',')

    dano_total = 0
    view = ''

    # Calculo do dano
    for i, a in enumerate(armadura):
        d = int(lista_dano[i])
        arm = int(a)
        if d > arm:
            dano = d - arm

            if locais_corpo()[i] == 'Cabeça': dano *= 2

            if dano >= 8:
                view += f'**{locais_corpo()[i]}** JÁ ERA *pof* 💀💥\n'

            dano_total += dano

    view += 'Dano = ' + str(dano_total)

    await ctx.reply(view)


# **************************************************************
# LEVA DANO
# **************************************************************

# ******************************* AÇÃO *******************************

@bot.hybrid_command(name="action", with_app_command=True, description="Faça uma ação")
@app_commands.guilds(discord.Object(id=id_do_servidor))
async def fazer_algo(ctx, atributo, proficiencia: int = 0):
    id = ctx.message.author.id
    info_mestre = False

    # Se ele se referencia a um atributo da ficha dele busca esse atributo na ficha
    if type(atributo) == type('str'):
        atributo = pega_ficha(id)[atributo]
    atributo = int(atributo)

    dificuldade = pega_dificuldade()
    view = ''
    dado = random.randint(1, 10)
    view += f'**Resultado dado**: {dado}\n'

    # Acerto critico
    if dado == 10:
        dado, view = mostrar_critico(dado, view)

    # Falha critica
    if dado == 1:
        view += "FALHA CRITICA!!\n"

    # Resultado final
    resultado_final = dado + atributo + proficiencia
    view += f'**Resultado Completo** = {resultado_final}\n\n'
    if info_mestre:
        view += f'\n**Resultado Final**\nResultado {resultado_final} vs Dificuldade {dificuldade}\n'

    # Verificar se superou a dificuldade
    if resultado_final >= dificuldade:
        view += '**PASSOU!!** :D'
    else:
        view += '**NÃO PASSOU** :x'

    await ctx.reply(view)


# ******************************* AÇÃO *******************************

# ******************************* SISTEMAS *******************************

# ******************************* HELP *******************************


@bot.command(name="help")
async def Help(ctx):
    currentPage = 0

    # functionality for buttons
    async def next_callback(interaction):
        nonlocal currentPage, sent_msg
        currentPage += 1
        await sent_msg.edit(embed=createHelpEmbed(pageNum=currentPage),
                            view=myview)

    async def previous_callback(interaction):
        nonlocal currentPage, sent_msg
        currentPage -= 1
        await sent_msg.edit(embed=createHelpEmbed(pageNum=currentPage),
                            view=myview)

    # add buttons to embed

    # previousButton = Button(label="<", style=ButtonStyle.blurple)
    # nextButton = Button(label=">", style=ButtonStyle.blurple)
    # previousButton.callback = previous_callback
    # nextButton.callback =  next_callback

    myview = View(timeout=180)
    # myview.add_item(previousButton)
    # myview.add_item(nextButton)

    sent_msg = await ctx.send(embed=createHelpEmbed(currentPage), view=myview)


# create help embed using page number and helpGuide
def createHelpEmbed(pageNum=0, inline=False):
    pageNum = (pageNum) % len(list(helpGuide))
    pageTitle = list(helpGuide)[pageNum]
    embed = Embed(color=0x0080ff, title=pageTitle)
    for key, val in helpGuide[pageTitle].items():
        embed.add_field(name=bot.command_prefix + key, value=val, inline=inline)
        # embed.set_footer(text=f"Page {pageNum+1} of {len(list(helpGuide))}")
    return embed


bot.run(TOKEN)
