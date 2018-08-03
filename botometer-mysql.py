import botometer
import mysql.connector
from mysql.connector import MySQLConnection, Error
from python_mysql_dbconfig import read_db_config
import time
import json
import datetime


def update_tabela(botometer, username):
    # read database configuration
    db_config = read_db_config()
 
    # prepare query and data
    query = """ UPDATE extracaoTeste2
                SET botometer = %s
                WHERE username = %s """
 
    data = (botometer, username)
 
    try:
        conn = MySQLConnection(**db_config)
 
        # update book title
        cursor = conn.cursor()
        cursor.execute(query, data)
 
        # accept the changes
        conn.commit()
 
    except Error as error:
        print(error)
 
    finally:
        cursor.close()
        conn.close()

#Chave fornecida pela API do Botometer
mashape_key = ""
#Chaves da API do Twitter
twitter_app_auth = {
    'consumer_key': '',
    'consumer_secret': '',
    'access_token': '',
    'access_token_secret': '',
  }
bom = botometer.Botometer(wait_on_ratelimit=True,
                          mashape_key=mashape_key,
                          **twitter_app_auth)

#Conexão com o banco
cnx = mysql.connector.connect(user='', password='',
                              host='',
                              database='',
                              charset='')
cursor = cnx.cursor()
query = ("Select username From extracaoTeste2")
cursor.execute(query)


dados = []
#carregando os dados da tabela com o select
for usuario in cursor:
  dados.append(usuario)
#Carregando os nomes dos usuarios a partir da lista dados  
for i in range(0,len(dados)):
    #O username está na posião [i][o], o i percorremos por toda tuple, não é um alista 
  result = bom.check_account(dados[i][0])
    #A variavel aponta para o percentual universal do Botometer 
  botcap = str(result['cap']['universal'])
    #A variavel aponta para o usuario utilizado no Botometer
  user = str(result['user']['screen_name'])
    #Chamo a função para inserir o CAP Universal na tabela de dados
  update_tabela(botcap, user)
    #O print não é necessário, mas vale apena para saber que está percorrendo corredamente pelos usuários e cap
  print (botcap)
  print(user)
    #Criando arquivo json com o resultado do botometer
  with open(dados[i][0] + '.json', 'w') as f:
    json.dump(result, f)
#Fecho a conexão com o banco
cursor.close()
cnx.close()
