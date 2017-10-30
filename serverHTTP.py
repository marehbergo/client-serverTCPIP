#!/usr/bin/python
# -*- coding: utf-8 -*-

import SimpleHTTPServer
import SocketServer
import sys, os

PORT = 8080


# Adiciona o diretório de trabalho e a port se esses parâmetros forem fornecidos na linha de comando
'''if len(sys.argv) > 1: 
	HOST = sys.argv[1]
	PORT = 8000
elif len(sys.argv) > 2: 
	HOST = sys.argv[1]
	PORT = int(sys.argv[2])
else:
	HOST = ''
	PORT = 8000
'''

Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
Handler.extensions_map.update({
    '.webapp': 'application/x-web-app-manifest+json',
});

httpd = SocketServer.TCPServer(('', PORT), Handler)

print '\033[32m'+'Servidor conectado na porta',PORT,'...'+'\033[0;0m'
httpd.serve_forever()
