from func.pri_read import leitura_de_arquivo_pri
from func.buscador_de_arquivos import get_arquivo_pri
import sched,time

event_schedule = sched.scheduler(time.time, time.sleep)



def app():
    '''
    criar tabela para registro caso nao haja uma
    '''
    # Funcao que verifica quais arquivos devem ser lidos e tradados
    # aqui devera ser implementado a funcao que define se o arquivo é novo ou não
    arquivo_pri_valido = get_arquivo_pri()
    if arquivo_pri_valido:
        leitura_de_arquivo_pri(arquivo_pri_valido.caminho)
    
    event_schedule.enter(10, 1, app,)
# app()
   
    
event_schedule.enter(2, 1, app,)
event_schedule.run()