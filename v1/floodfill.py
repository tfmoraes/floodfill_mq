# Pinta uma regiao delimitada de uma imagem.
# Modulo - FloodFill
#
# 21/02/2011

from scipy.misc import imread, imsave
import numpy
import multiprocessing
import sys
from multiprocessing.managers import BaseManager 

def pega_matrizes(queue):
  while 1:
  ### while not queue.empty():
    a = queue.get()
    f, arqs, yo, xo = a
    print '[pega_matrizes]', arqs
    yield a


def push(pilha, el):
  pilha.append(el)


def pop(pilha):
  return pilha.pop()


def flood_fill_horiz(fatia, arq_saida, yo, xo):
  
  branco = 255
  cinza = 128
  preto = 0
  fator = 255

  print '[flood_fill_horiz]', arq_saida
  
  altura = fatia.shape[0]
  largura = fatia.shape[1]
  if fatia.max() == 1:
    fatia *= fator # Para corrigir imagens em que o branco tem valor 1. Como as imagens em {fatias_560x616}.
  # Empilha o pixel semente.
  if fatia[yo,xo] == branco:
    semente = [yo,xo]
    pilha = [semente] # push(pilha, semente)
  else:
    print 'fatia[' + str(yo) + ',' + str(xo) + ']: ' + str(fatia[yo,xo])
    
  while pilha:
    pixel = pop(pilha)
    
    xi = pixel[1]
    while xi > 0 and fatia[pixel[0],xi] == branco: # Varre os pixels 'a esquerda de [pixel[0],pixel[1]].
      if pixel[0]-1 > 0 and fatia[pixel[0]-1,xi] == branco:
        push(pilha, [pixel[0]-1,xi]) # Empilha os pixels da linha anterior.
      if pixel[0]+1 < altura and fatia[pixel[0]+1,xi] == branco:
        push(pilha, [pixel[0]+1,xi]) # Empilha os pixels da linha posterior.
      xi -= 1  
    xi += 1 # Leu pixel preto ou chegou ao inicio da linha (borda).
    
    xf = pixel[1]+1
    while xf < largura and fatia[pixel[0],xf] == branco: # Varre os pixels 'a direita de [pixel[0],pixel[1]].
      if pixel[0]-1 > 0 and fatia[pixel[0]-1,xf] == branco:
        push(pilha, [pixel[0]-1,xf]) # Empilha os pixels da linha anterior.
      if pixel[0]+1 < altura and fatia[pixel[0]+1,xf] == branco:
        push(pilha, [pixel[0]+1,xf]) # Empilha os pixels da linha posterior.    
      xf += 1
    xf -= 1 # Leu pixel preto ou chegou ao final da linha (borda).

    fatia[pixel[0], xi:xf+1] = preto # Pinta o intervalo [xi:xf], que ja inclui o pixel desempilhado.
    
  return fatia, arq_saida


class QueueManager(BaseManager):
  pass


def main():
  address = sys.argv[1]
  port = int(sys.argv[2])

  QueueManager.register('get_queue')
  QueueManager.register('salva_imagem')
  m = QueueManager(address=(address, port), authkey='abc')
  m.connect()
  
  queue = m.get_queue()
  print 'Tamanho da fila:', queue.qsize()

  # Processa {maxtasksperchild} tarefas e morre, liberando recursos e
  # permitindo a criacao de um processo substituto.
  pool = multiprocessing.Pool(maxtasksperchild=1, processes=6)

  iteravel = pega_matrizes(queue)
  ### for i in pool.imap(flood_fill_horiz, iteravel):
  iterador = pool.imap(flood_fill_horiz, iteravel)
  for i in iterador:
    fatia, arq_s = i
    print 'Salvando', arq_s
    m.salva_imagem(fatia, arq_s)
  
    
if __name__ == '__main__':
  main()
