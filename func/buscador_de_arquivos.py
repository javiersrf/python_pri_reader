import os
import mysql.connector
class CaminhoDoArquivo:
    def __init__(self,caminho,data_criado,data_atualizado):
        self.caminho = caminho
        self.data_criada = data_criado
        self.data_atualizado = data_atualizado
    def __str__(self):
        return self.caminho+ "->"+ str(self.data_atualizado)
    def __repr__(self):
        return self.caminho+ "->"+ str(self.data_atualizado)

def myFunc(e):
  return e.data_atualizado
def get_arquivo_pri():
    try:
        # Verificando se há alguma leitura em processamento
        mydb = mysql.connector.connect(host="localhost", user="smartfleet", password="smartkey",database="smartfleet")
        con = mydb.cursor()
        sql_1 = "SELECT read_pri_status FROM smartfleet.reading_status ORDER BY updated_at DESC LIMIT 1;"
        con.execute(sql_1)
        status_de_leitura = con.fetchone()
        if status_de_leitura !=None:
            if status_de_leitura[0] == 1:
                return None
        # É necessário verificar qual foi o último arquivo lido para que não haja leitura duplicada
        sql_2 = "SELECT file_path FROM smartfleet.pri ORDER BY id DESC LIMIT 1;"
        con.execute(sql_2)
        ultimo_arquivo_lido = con.fetchone()
        if ultimo_arquivo_lido!=None:
            ultimo_arquivo_lido = ultimo_arquivo_lido[0] #Adicionando o arquivo lido à variável 
        mydb.close() # fechando a conexao com o banco pois não será mais necessária
        caminho = 'C:/prd/' # Mocando o prefixo do arquivo para que seja possível localizar no diretorio
        resultado = []
        arquivos =os.listdir(caminho)    
        for arquivo in arquivos:
            data_criacao = os.path.getctime(caminho+arquivo)
            data_atualizado = os.path.getmtime(caminho+arquivo)
            if arquivo.endswith(".pri") :  
                resultado.append(CaminhoDoArquivo(caminho=arquivo,data_criado=data_criacao,data_atualizado=data_atualizado))
        resultado.sort(key=myFunc,reverse=True,)
        arquivo_mais_novo = resultado[0]
        if resultado:
            ultimo_arquivo_gravado = ultimo_arquivo_lido
            if ultimo_arquivo_gravado:
                if ultimo_arquivo_gravado!= arquivo_mais_novo.caminho:
                    return arquivo_mais_novo
                else:
                    return None
            return arquivo_mais_novo
        return None
    except :
        return None

