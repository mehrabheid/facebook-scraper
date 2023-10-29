from db_conn import DBconn

def execute_commit(sql_query,sql_values=())->None:
    mysqlQuery=sql_query
    mysqlValues=sql_values
    cur=DBconn()
    cur.cursor.execute(mysqlQuery,mysqlValues)
    cur.connection.commit()
    cur.cursor.close()
    cur.connection.close()
    return

def execute_fetchall(sql_query,sql_values=())-> list: 
    mysqlQuery=sql_query
    mysqlValues=sql_values
    cur=DBconn()
    cur.cursor.execute(mysqlQuery,mysqlValues)
    fetchall_results=cur.cursor.fetchall()
    cur.cursor.close()
    cur.connection.close()
    sql_results=[]
    for results in fetchall_results:
        for res in results:
            sql_results.append(res)

    return sql_results     
