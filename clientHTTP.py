# -*- coding: utf-8 -*-

# Cliente para envio/recebimento de arquivos
# -----------------------------------------------------
# Entrada : Um nome de arquivo
# Saida : Um possivel arquivo
# Autora : Maria Emilia Bergo - mariaemilia.bergo@gmail.com (adaptado de f_Candido)

from socket import *
import sys
import os

#serverName = gethostname()
#serverPort = 12000

clientSocket = socket(AF_INET, SOCK_STREAM)

entrada = raw_input('navegador ')
entrada = entrada.split(' ')

url = entrada[0]
porta = entrada[1]

valida = True

while (valida):

	# WWW -> porta 80
	if url[0] == 'w':
		
		endereco = url.split('/') # endereco[0] -> url até a primeira /
		tam = len(endereco[0])
		caminho = url[tam:]

		serverName = endereco[0]
		serverPort = 80
		
		# Conecta como cliente a um servidor selecionado utilizando a porta especificada 
		clientSocket.connect((serverName,serverPort))

		valida = False

	# HTTP ou HTTPS
	elif url[0] == 'h':
		protocol = url.split(':')

		# HTTP -> porta 80
		if protocol[0] == 'http':
			
			dado = url.split('/') # dado[0] = protocolo -> 'http:'
			tam = len(dado[0])
			endereco = url[(tam+2):] # url a partir do //
			
			string = endereco.split('/')

			tam = len(string[0])
			caminho = endereco[(tam):] #url a partir do /

			# ------- ERRO EM ENDEREÇOS HTTP ---------
			# ------- NÃO ESTÁ FUNCIONANDO COM HTTP ---------
			#serverName = 'http://' + string[0]
			
			if endereco[0] == 'w':
				serverName = string[0]
				serverPort = 80
			else:
				serverName = 'www.' + string[0]
				serverPort = 80

			# Conecta como cliente a um servidor selecionado utilizando a porta especificada 
			clientSocket.connect((serverName,serverPort))

			valida = False

		# HTTPS -> porta 443
		elif protocol[0] == 'https':

			dado = url.split('/') # dado[0] = protocolo -> 'http:'
			tam = len(dado[0])
			endereco = url[(tam+2):] # url a partir do //

			string = endereco.split('/')

			tam = len(string[0])
			caminho = endereco[(tam):] #url a partir do /

			# ------- ERRO EM ENDEREÇOS HTTP ---------
			# ------- NÃO ESTÁ FUNCIONANDO COM HTTP ---------
			#serverName = 'http://' + string[0]
			
			'''if endereco[0] == 'w':
				serverName = string[0]
				serverPort = 80				
				#serverPort = 443
			else:
				serverName = 'www.' + string[0]
				serverPort = 80
				#serverPort = 443
			'''

			serverName = string[0]
			serverPort = 80

			#print serverName
			#print serverPort

			# Conecta como cliente a um servidor selecionado utilizando a porta especificada 
			clientSocket.connect((serverName,serverPort))

			valida = False

		else:
			print 'Não foi possovel identificar a url... Tente novamente.'
			valida = True

	else:
		print 'Não foi possovel identificar a url... Tente novamente.'
		valida = True

# -------- CONEXÃO ESTABELECIDA --------
print '\033[32m'+'\nConexao extabelecida com o endereco',serverName,'na porta',serverPort,'...'+'\033[0;0m\n'

# -------- Envio de requisicao via GET --------
clientSocket.send('GET ' + caminho + ' HTTP/1.0\n\n')

var = caminho.split('/')
fileName = var[len(var)-1]

while True:
    resp = clientSocket.recv(5120)
    if resp == '': print 'Nenhuma resposta retornada pelo servidor.' # break

    status = resp[9:12]

    # Retorno OK e o arquivo é salvo
    if status == '200': 
        print 'Status HTTP:'+'\033[32m'+' 200 OK'+'\033[0;0m'+' - A requisição foi recebida, compreendida, aceita e processada com êxito.'+'\033[0;0m'

        arq = open(fileName, 'w')
        content = resp.split('\n')

        i = 0
        for item in content:
        	if item == '\r':
        		break
        	i += 1

        lista = len(content) - i

        for l in range(lista):
        	if l == (lista-1):
        		break
        	
        	arq.write(content[i+1] + '\n')
        	i += 1

        arq.close()

    # ERROS
    elif status == '301': 
        print 'Status HTTP: '+'\033[31m'+'301 URL Movida Permanentemente'+'\033[0;0m'+' - Esta e todas as solicitações futuras devem ser direcionadas para a nova URL retornada.'
    elif status == '400':
        print 'Status HTTP: '+'\033[31m'+'400 Requisição inválida'+'\033[0;0m'+' - O pedido não pode ser entregue devido à sintaxe incorreta.'
    elif status == '403':
        print 'Status HTTP: '+'\033[31m'+'403 Proibido'+'\033[0;0m'+' - O pedido é reconhecido pelo servidor mas este recusa-se a executá-lo.'
    elif status == '404':
        print 'Status HTTP: '+'\033[31m'+'404 Não encontrado'+'\033[0;0m'+' - O recurso requisitado não foi encontrado.'
    elif status == '500':
        print 'Status HTTP: '+'\033[31m'+'500 Erro interno do servidor'+'\033[0;0m'+' - Ocorreu um erro do servidor ao processar a solicitação.'
    else:
        break

    break

# Fecha a conexãp quando estiver completa
clientSocket.close()
print '\nConexao finalizada. Até breve'+'\033[33m'+' :)\n'+'\033[0;0m'