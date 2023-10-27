from lista_e_dicionarios import deleta_gif_acertou_usuario

def deleta_url(url,lista_url, id):

  aux_lista = lista_url
  for i in aux_lista:
    if i == url:
      lista_url.remove(url)
      deleta_gif_acertou_usuario(id, lista_url)
      return True
      
  return False  