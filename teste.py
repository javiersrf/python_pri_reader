from func.pri_file import PriFile
with open('C:/prd/20220418_11 B_1_1.pri') as file:
        texto = file.read()
        pri_file = PriFile(texto)
        resumo = pri_file.resume_by_id()
        print(resumo)