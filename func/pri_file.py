import datetime
import numpy as np
def translateVariableToValue(variable)->str:
    dict = {
        "1":"price matrix",
        "2":"Species number",
        "44":"calibre",
        "20":"20",
        "201":"Diameter top, ob",
        "202":"Diameter top, ub",
        "203":"Diameter mid, ob",
        "204":"Diameter mid, ub",
        "205":"Diameter root, ob",
        "206":"Diameter root, ub",
        "207":"Middle diameter according to HKS measurement, ob",
        "208":"Middle diameter according to HKS measurement, ub",
        "300":"Forced cross-cut (break) at small end, code according to var300",
        "301":"Physical length",
        "302":"Length",
        "400":"Volume according to Var161",
        "401":"Volume m3sob",
        "402":"Volume m3sub",
        "403":"Volume m3topob",
        "404":"Volume m3topub",
        "405":"Volume m3smi ob",
        "406":"Volume m3smi ub",
        "420":"Volume according to Var161 in dl (not m3)",
        "421":"Volume dl sob",
        "422":"Volume dl sub",
        "423":"Volume dl topob",
        "424":"Volume dl topub",
        "425":"Volume dl smi ob",
        "426":"Volume dl smi ub",
        "500":"Stem number",
        "501":"Log number",
}
    if variable in dict:
        return dict[f"{variable}"]
    return variable

class PriFile:
    def __init__(self,texto,parametros = 11):
        self.valid = True
        self.__volume__ = "Volume dl sub"
        self.__length__ = "Physical length"
        self.text = texto.replace("~"," ~")
        self.text = self.text.replace("\n"," ")
        self.__parametros__ = parametros
        lista_result = self.text.split("~")
        lista_result = [l for l in lista_result if l]
        self.dict = {}
        for x in lista_result:
            splitado = x.split(" ")
            variable = splitado[0]
            # Aqui, salvará cada conjunto chave-resultados no dicionário principal,
            # sendo a chave do mesmo o conjunto "chave" + "tipo"
            self.dict[f"{variable}-{splitado[1]}"] = {
                "type":splitado[1],
                "values": [l for l in splitado[2:] if l] if len(splitado)>2 else None
            }
        # Após organizar todos os dados no dicionário,
        # chama a função que gera os dados principais com base no dicionário
        self.generate_data()


    def generate_data(self):
        # A chave 256-1 faz referência à legenda dos dados presente
        # no arquivo. Portanto, é importante começar a leitura por ela para ententer o tamanho do resultado 
        # e a posição de cada valor. 
        if "256-1" in self.dict:
            labels = self.dict["256-1"]["values"]
            labels = [translateVariableToValue(x) for x in labels]
            len_dados = len(labels)
            dados = self.dict["257-1"]["values"]
            species_numbers_6 = self.dict["121-6"]["values"]
            species_numbers_1 = self.dict["121-1"]["values"]
            species_numbers_2 = self.dict["121-2"]["values"]
            if len(species_numbers_1) > len(species_numbers_2):
                species_numbers_1_temp = []
                z = 0
                while z < len(species_numbers_1):
                    species_numbers_1_temp.append("".join([species_numbers_1[z],species_numbers_1[z+1] if len(species_numbers_1)>z+1 else ""]))
                    z+=2
                species_numbers_1 = species_numbers_1_temp
            self.values = []
            while len(dados)>= len_dados:
                dados_crus = dados[:len_dados]
                dicte = {}
                for y in range(len(dados_crus)):
                    idx = y-1
                    dicte[labels[idx]] = dados_crus[idx]
                identificador ='UNDENTIFIED'
                if "20" in dicte:
                    if dicte["20"] != '0':
                        idx_species_id = species_numbers_6.index(dicte["20"])
                        identificador = species_numbers_1[idx_species_id] +species_numbers_2[idx_species_id]     
                else:
                    if "price matrix" in dicte and dicte["price matrix"]!="0":
                        identificador = species_numbers_1[int(dicte["price matrix"])-1]
                dicte["ID"] = identificador
                self.values.append(dicte)
                dados = dados[len_dados:]
            self.date_file = self.strToDate(self.dict["16-4"]["values"][0])
        else:
            self.valid = False
        

    def strToDate(self,string):
        ano = string[:4]
        mes = string[4:6]
        dia = string[6:8]
        hora = string[8:10]
        minutos = string[10:12]
        segundos = string[12:]
        data = datetime.datetime(int(ano),int(mes),int(dia),int(hora),int(minutos),int(segundos))
        return data
        
        

    def resume_by_length(self):
        tree_amount = max([int(x["Stem number"]) for x in self.values if "Stem number" in x])
        volume_total = sum(float(x[self.__volume__]) for x in self.values if self.__volume__ in x)
        # lenght_total = sum([int(x[self.__length__]) for x in self.values if self.__length__ in x])
        ids = np.unique([x["Physical length"] for x in self.values if "Physical length" in x])
        grouyping = []
        for y in ids:
            temp = [x for x in self.values if x["Physical length"]== y]
            grouyping.append({
                "id":[x["ID"] for x in self.values if x["ID"] ==y][0],
                "Physical length": y,
                "logs_amount" :len(temp),
                "volume_total" : sum(float(x[self.__volume__]) for x in temp if self.__volume__ in x),
                # "length_total":  sum([int(x[self.__length__]) for x in temp if self.__length__ in x]),
            })
        return {
            "tree_amount":tree_amount,
            "volume_total":volume_total,
            # "length_total": lenght_total ,
            "types":list(ids),
            "groupying":grouyping}  

    def resume_by_id(self):
        tree_amount = int(self.dict["221-1"]["values"][0]) if "221-1" in self.dict else  max([int(x["Stem number"]) for x in self.values if "Stem number" in x])
        volume_total = sum(float(x[self.__volume__]) for x in self.values if self.__volume__ in x)
        
        ids = np.unique([x["ID"] for x in self.values if "ID" in x])
        grouyping = []
        for y in ids:
            temp = [x for x in self.values if x["ID"]== y]
            grouyping.append({
                "id":[x["ID"] for x in self.values if x["ID"] ==y][0],
                # "Physical length": y,
                "logs_amount" :len(temp),
                "volume_total" : sum(float(x[self.__volume__]) for x in temp if self.__volume__ in x),
                "max_length":  max([int(x[self.__length__]) for x in temp if self.__length__ in x]),
                "min_length":  min([int(x[self.__length__]) for x in temp if self.__length__ in x]),
                "avg_length":  round(float(np.mean([int(x[self.__length__]) for x in temp if self.__length__ in x])),2)
            })
        return {
            "tree_amount":tree_amount,
            "volume_total":volume_total,
            "types":list(ids),
            "groupying":grouyping}    
    def __str__(self) -> str:
        return f"Prifile with reader"



        


