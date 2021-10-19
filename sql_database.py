import mysql.connector
from data_indsamler import indsaml, webScrape
from dotenv import load_dotenv
import os

load_dotenv()
sql_host = os.getenv("sql_host")
sql_user = os.getenv("sql_user")
sql_pass = os.getenv("sql_pass")
lectio_user = os.getenv("lectio_user")
lectio_pass = os.getenv("lectio_pass")
lectio_opgaver = os.getenv("lectio_opgaver")
lectio_base = os.getenv("lectio_base")



def connect():
    mindb = mysql.connector.connect(
        host=sql_host,
        user=sql_user,
        password=sql_pass
    )

    mincursor = mindb.cursor()

    sql = "USE skoledatabase"

    mincursor.execute(sql)
    mindb.commit()
    mincursor.close()
    #print("Connected til database...")
    return mindb

def makeCursor(mindb):
    mincursor = mindb.cursor()
    return mincursor

# Reset af tabel
def resetTable():
    mindb = connect()
    mincursor = makeCursor(mindb)
    sql = "DROP TABLE lektier"
    mincursor.execute(sql)

    sql = """CREATE TABLE `skoledatabase`.`lektier` (
      `idlektier` INT NOT NULL AUTO_INCREMENT,
      `titel` VARCHAR(45) NOT NULL,
      `frist` DATETIME NOT NULL,
      `elevtid` VARCHAR(45),
      PRIMARY KEY (`idlektier`));"""
    mincursor.execute(sql)

    print("Tabel resat!")
    mincursor.close()
    mindb.close()

# Upload
def uploadToTable():
    names, frister, elevtid = indsaml(webScrape(lectio_base + "login.aspx", lectio_base + lectio_opgaver, lectio_user, lectio_pass))
    if len(os.listdir("html/")) >= 4:
        os.remove("html/" + os.listdir("html/")[0])

    mindb = connect()
    mincursor = makeCursor(mindb)
    for i in range(len(names)):
        sql = "INSERT INTO lektier (titel, frist, elevtid) VALUES (%s, %s, %s)"
        val = (names[i], frister[i], elevtid[i])
    
        #print(val)
        mincursor.execute(sql, val)
        
        mindb.commit()
    print("Data uploadet!")
    mincursor.close()
    mindb.close()

# Vis data i tabeller
def showNext(limitval):
    mindb = connect()
    mincursor = makeCursor(mindb)
    sql = f"SELECT titel, frist, elevtid FROM lektier WHERE frist > curtime() ORDER BY frist LIMIT {limitval}"
    mincursor.execute(sql)
    resultat = mincursor.fetchall()


    resultater = []

    for x in resultat:
        resultater.append(x)
    
    #print("Lektier optalt...")
    mincursor.close()
    mindb.close()
    #print(list(resultater[0]))
    #print(resultater)
    return resultater

# Slet gamle opgaver
def deleteOld():
    mindb = connect()
    mincursor = makeCursor(mindb)
    
    # Fjerner gamle lektier
    sql = f"DELETE FROM lektier WHERE frist < curtime()"
    mincursor.execute(sql)
    mindb.commit()

    # Fjerner duplicates -- Beholder den lektier med lavest ID
    sql = f"DELETE t1 FROM lektier t1 INNER JOIN lektier t2 WHERE t1.idlektier > t2.idlektier AND t1.titel = t2.titel;"
    mincursor.execute(sql)
    mindb.commit()

    print("Gamle lektier fjernet!")
    mincursor.close()
    mindb.close()



#webScrape(lectio_base + "login.aspx", lectio_base + lectio_opgaver, lectio_user, lectio_pass)
#mindb = connect()
#resetTable()
#print(showNext(3))
#print(showNext(3)[0][1])

# Updates database

""" uploadToTable()
deleteOld()"""