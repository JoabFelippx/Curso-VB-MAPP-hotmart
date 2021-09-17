import requests
import json

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# Informacoes necessarias para fazer a requisicao
api = 'https://developers.hotmart.com/'

subdomain = ''  # SUBDOMINIO DO CURSO

TOKEN = ''  # TOKEN DE PERMISSÃO PARA FAZER A REQUISICAO
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'bearer ' + TOKEN
}

url = api + 'club/api/v1/users?subdomain=' + subdomain

resquest = requests.get(url, headers=headers)

# resultado da requisicao
data = resquest.json()

items_info = data['items']  # ARMAZENAR AS INFORMACOES CONTIDA NA PAGINA
page_info = data['page_info']  # OBTER INFORMACOES SOBRE A PAGINA

# VERIFICAR SE EXISTE MAIS PAGINAS
for items in page_info.items():

    # CASO EXISTA MAIS PAGINAS COLETAR AS INFORMACOES CONTIDA NA NOVA PAGINA E JUNTAR COM AS DA PAGINA ANTERIOR (linha 43)
    if 'next_page_token' in items[0]:

        url = api + 'club/api/v1/users?page_token=' + \
            items[1] + '&subdomain=' + subdomain

        res_2 = requests.get(url, headers=headers)

        next_page_data = res_2.json()

        items_info += next_page_data['items']

        page_info = next_page_data['page_info']

students_datas = {}
# COLETAR AS INFORMACOES DESEJADA DO ALUNO
for c in range(0, len(items_info)):
    students_datas.update({
        items_info[c]['name']: items_info[c]['email']
    })

host = ''  # HOST URL, por exemplo smtp.google.com
port = 587
user = ''  # CONTA USADA PARA O ENVIO
password = ''  # SENHA DA CONTA USADA PARA O ENVIO
server = smtplib.SMTP(host, port)

server.ehlo()
server.starttls()
server.login(user, password)

# ENVIAR EMAIL
for student in students_datas.items():
    firstName = student[0].split(' ')[0]
    message = ''  # MENSAGEM DO EMAIL
    email_msg = MIMEMultipart()
    email_msg['From'] = user    
    email_msg['To'] = student[1]
    email_msg['Subject'] = ''  # ASSUNTO DO EMAIL

    email_msg.attach(MIMEText(message, 'html'))

    server.sendmail(email_msg['From'], email_msg['To'], email_msg.as_string())
    print(
        f'email enviado para {student[1]} aluno(a) {student[0]}, primeiro nome {firstName}')
server.quit()
