from func.pri_file import PriFile
with open('C:/prd/FAZENDA_TRA-220322-154221.pri') as file:
        texto = file.read()
        pri_file = PriFile(texto)
        resumo = pri_file.resume_by_id()
        print(resumo)