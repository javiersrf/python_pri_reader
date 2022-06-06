from src.pri_read import leitura_de_arquivo_pri
from src.buscador_de_arquivos import get_arquivo_pri
import sched,time

event_schedule = sched.scheduler(time.time, time.sleep)



def app():
    '''
    criar tabela para registro caso nao haja uma
    '''
    # Funcao que verifica quais arquivos devem ser lidos e tradados
    # aqui devera ser implementado a funcao que define se o arquivo é novo ou não
    arquivos_pri_validos = get_arquivo_pri()
    if arquivos_pri_validos:
        for x in arquivos_pri_validos:
            leitura_de_arquivo_pri(x)
    
    event_schedule.enter(10, 1, app,)
  
    
event_schedule.enter(2, 1, app,)
event_schedule.run()