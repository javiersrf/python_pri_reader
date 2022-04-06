from func.pri_file import PriFile
import mysql.connector


def leitura_de_arquivo_pri(path):
    name_path  =path
    path = 'C:/prd/'+path
    with open(path) as file:
        texto = file.read()
        pri_file = PriFile(texto)
    resume = pri_file.resume()
    valors = [list(x.values()) for x in resume["groupying"]]
    '''
    Ordenando os registro para qual foi o ultimo
    '''
    mydb = mysql.connector.connect(host="localhost", user="smartfleet", password="smartkey",database="smartfleet")
    con = mydb.cursor()
    sql = "INSERT INTO smartfleet.pri(file_path,tree_amount,volume_total,created_at)VALUES(%s,%s,%s,%s);"
    val = (name_path,int(resume["tree_amount"]),int(resume["volume_total"]),pri_file.date_file.strftime('%Y-%m-%d %H:%M:%S'))
    con.execute(sql,val)
    mydb.commit()
    sql = "SELECT id from smartfleet.pri order by id desc limit 1;"
    con.execute(sql)
    resultado =con.fetchone()
    if resultado:
        ultimo_id = resultado[0] 
        valors = [list(x.values()) for x in resume["groupying"]]
        for x in valors:
            sql = "INSERT INTO smartfleet.pri_logs_resume(pri_id,product,length ,logs_amount,volume_total)VALUES(%s,%s,%s,%s,%s);"
            val = (ultimo_id,x[0],x[1],x[2],int(x[3]))
            con.execute(sql,val)
            mydb.commit()
    mydb.close()
        
# s = leitura_de_arquivo_pri('s')
