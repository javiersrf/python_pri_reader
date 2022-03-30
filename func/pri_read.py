from func.pri_file import PriFile
import mysql.connector


def leitura_de_arquivo_pri(path):
    path = 'C:/prd/'+path
    with open(path) as file:
        texto = file.read()
        pri_file = PriFile(texto)
    resume = pri_file.resume()
    valors = [list(x.values()) for x in resume["groupying"]]
    # with open(f"{path[:-4]}_RESUMO_.csv",'a+') as f:
    #     write = csv.writer(f)
    #     write.writerow(["tree_amount","volume_total"])
    #     write.writerow([resume["tree_amount"],resume["volume_total"]])
    #     write.writerow(["id","Physical length","logs_amount","volume_total"])
    #     write.writerows(valors)
    '''
    Ordenando os registro para qual foi o ultimo
    '''
    mydb = mysql.connector.connect(host="localhost", user="smartfleet", password="smartkey",database="smartfleet")
    con = mydb.cursor()
    sql = "INSERT INTO `smartfleet`.`pri`(`tree_amount`,`volume_total`,`date`)VALUES(%s,%s,%s);"
    val = (int(resume["tree_amount"]),int(resume["volume_total"]),pri_file.date_file.strftime('%Y-%m-%d %H:%M:%S'))
    con.execute(sql,val)
    mydb.commit()
    sql = "SELECT id from `smartfleet`.`pri` order by id desc limit 1;"
    con.execute(sql)
    resultado =con.fetchone()
    if resultado:
        ultimo_id = resultado[0] 
        valors = [list(x.values()) for x in resume["groupying"]]
        for x in valors:
            sql = "INSERT INTO `smartfleet`.`pri_logs_resume`(`pri_id`,`product`,`lenght`,`logs_amount`,`volume_total`)VALUES(%s,%s,%s,%s,%s);"
            val = (ultimo_id,x[0],x[1],x[2],int(x[3]))
            con.execute(sql,val)
            mydb.commit()
    mydb.close()
    with open("last_file.txt","+w") as f:
        f.write(path)
        
# s = leitura_de_arquivo_pri('s')
