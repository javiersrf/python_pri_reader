import mysql.connector
import os
import logging

from .pri_file import PriFile
from .env import MAIN_LOCAL, LOG_LOCAL 

def leitura_de_arquivo_pri(path):
    logging.basicConfig(filename = LOG_LOCAL + path[:-3] + 'txt', format= '%(asctime)s|%(levelname)s|%(message)s|', filemode='+a', level=logging.DEBUG)
    logging.info("Init reading of file " + path)
    name_path  = path
    path = MAIN_LOCAL + path

    logging.info("Checking for mysql connection")
    try:
        mydb = mysql.connector.connect(host="localhost", user="smartfleet", password="smartkey",database="smartfleet")
        con = mydb.cursor()
    except Exception as excpt:
        logging.error("Mysql connection error")
        logging.exception(msg= excpt)
 
    logging.info("Updating read status")
    sql = "UPDATE smartfleet.reading_status SET read_pri_status = 1, updated_at = current_date() where 1=1;"

    try:
        con.execute(sql)
        mydb.commit()
    except Exception as excpt:
        logging.error("Error at updating read status")
        logging.exception(msg= excpt)

    mydb.close()

    with open(path) as file:
        texto = file.read()
        logging.info("Opening pri file as PriFile python class")
        try:
            pri_file = PriFile(texto)
        except Exception as excpt:
            logging.error("Error at reading pri file")
            logging.exception(msg= excpt)


    try:
        logging.info("Checking for new mysql connection")
        mydb = mysql.connector.connect(host="localhost", user="smartfleet", password="smartkey",database="smartfleet")
        con = mydb.cursor()
    except Exception as excpt:
        logging.error("New Mysql connection error")
        logging.exception(msg= excpt)
    logging.info("Checking if pri file is valid")
    logging.info("Pri file is valid : " + str(pri_file.valid))
    if pri_file.valid:
        try:
            logging.info("Generating resume of pri file")
            resume = pri_file.resume_by_id()
        except Exception as excpt:
            logging.error("Pri file resume error")
            logging.exception(msg= excpt)

        valors = [list(x.values()) for x in resume["groupying"]]
        '''
        Ordenando os registro para qual foi o ultimo
        '''
        logging.info("Selecting last operator in appropriation")
        try:
            con.execute("SELECT operador_id,id FROM smartfleet.message_sent WHERE  form_id BETWEEN 10300 AND 10399 OR form_id BETWEEN 10700 AND 10799 OR form_id BETWEEN 11300 AND 11399 order by create_date desc limit 1")
            myresult =con.fetchone()
        except Exception as excpt:
            logging.error("Error on last operator")
            logging.exception(msg= excpt)                      
        if myresult:
            operador_ultima_apropriacao = myresult[0]
            logging.info("Last operator in appropriation: " +  str(operador_ultima_apropriacao))
            sql = "INSERT INTO smartfleet.pri(file_path,operator_id,tree_amount,volume_total,created_at)VALUES(%s,%s,%s,%s,%s);"
            try:
                logging.info("Inserting pri tables contents")
                val = (name_path, str(operador_ultima_apropriacao), int(resume["tree_amount"]), int(resume["volume_total"]), pri_file.date_file.strftime('%Y-%m-%d %H:%M:%S'))
                con.execute(sql,val)
                mydb.commit()
            except Exception as excpt:
                logging.error("Error in pri tables contents")
                logging.exception(msg= excpt)
            sql = "SELECT id from smartfleet.pri order by id desc limit 1;"
            con.execute(sql)
            resultado =con.fetchone()
            if resultado:
                ultimo_id = resultado[0] 
                valors = [list(x.values()) for x in resume["groupying"]]
                for x in valors:
                    logging.info("Inserting pri_logs_resume tables contents")
                    try:
                        sql = "INSERT INTO smartfleet.pri_logs_resume(pri_id,product,logs_amount,volume_total,max_length,min_length,avg_length)VALUES(%s,%s,%s,%s,%s,%s,%s);"
                        # pri_id,product,logs_amount,volume_total
                        val = (int(ultimo_id),str(x[0]),int(x[1]),int(x[2]),int(x[3]),int(x[4]),float(x[5]))
                        con.execute(sql,val)
                        mydb.commit()
                    except Exception as excpt:
                        logging.error("Error in pri_logs_resume tables contents")
                        logging.exception(msg= excpt)
        else:
            logging.info("No results for last operator")
            
    sql = "UPDATE smartfleet.reading_status SET read_pri_status = 0, updated_at = current_date() where 1=1;"
    con.execute(sql)
    mydb.commit()
    mydb.close()
    try:
        logging.info("Trying to remove pri file")
        os.remove(path)
    except Exception as excpt:
        logging.error("Cannot remove pri file")
        logging.exception(msg= excpt)
    finally:
        logging.info("pri file removed")
        logging.info("End of pri reading " + path)
        

