import os

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
    caminho = 'C:/prd/'
    resultado = []
    arquivos =os.listdir(caminho)    
    for arquivo in arquivos:
        # print(arquivo)
        data_criacao = os.path.getctime(caminho+arquivo)
        data_atualizado = os.path.getmtime(caminho+arquivo)
        if arquivo.endswith(".pri") :  
            resultado.append(CaminhoDoArquivo(caminho=arquivo,data_criado=data_criacao,data_atualizado=data_atualizado))
    resultado.sort(key=myFunc,reverse=True,)
    if resultado:
        ultimo_arquivo_gravado = None
        try:
            with open("last_file.txt","r") as f:
                t = f.read()
                ultimo_arquivo_gravado = t      
        except FileNotFoundError as e:
            pass
        if ultimo_arquivo_gravado:
            if ultimo_arquivo_gravado!= caminho +resultado[0].caminho:
                return resultado[0]
            else:
                return None
        return resultado[0]
    return None 

# get_arquivo_pri()