import sqlite3
con=sqlite3.connect("proje.db")
cursor=con.cursor()
def createTable(tblName):
    sqlText="CREATE TABLE IF NOT EXISTS "+ tblName+" (id INT, name TEXT, price DOUBLE)"
    cursor.execute(sqlText)
    con.commit

def addProduct(tblName,id, name, price):
    kontrol_sorgusu = "SELECT id FROM "+tblName+" WHERE id = ?"
    kontrol_verileri = (id,)
    cursor.execute(kontrol_sorgusu, kontrol_verileri)
    var_mi = cursor.fetchone()
    if var_mi:
        print("Bu ID ile zaten bir satır var.")
    else:
        sorgu = "INSERT INTO "+tblName+" (id, name, price) VALUES (?, ?, ?)"
        veriler = (id, name, price)
        cursor.execute(sorgu, veriler)
        print("Veri başarıyla eklendi.")
    con.commit()
def get(tblName,id,colName):
    data=""
    cursor.execute(f"SELECT {colName} FROM {tblName} WHERE id = ?", (id,))
    result = cursor.fetchone()
    if result:
        data = result[0]
    else:
        print("Eşleşen ID bulunamadı.")
    con.commit
    return data
    return data
def isThere(tblName,id):
    kontrol_sorgusu = "SELECT id FROM "+tblName+" WHERE id = ?"
    kontrol_verileri = (id,)
    cursor.execute(kontrol_sorgusu, kontrol_verileri)
    var_mi = cursor.fetchone()

    if var_mi:
        return True
    elif id==None:
        return False
    else:
        return False

    con.commit()

def updateProduct(tblName,id, name, price):
    kontrol_sorgusu = "SELECT id FROM "+tblName+" WHERE id = ?"
    kontrol_verileri = (id,)
    cursor.execute(kontrol_sorgusu, kontrol_verileri)
    var_mi = cursor.fetchone()

    if var_mi:
        guncelle_sorgusu = "UPDATE "+tblName+" SET name = ?, price = ? WHERE id = ?"
        guncelle_verileri = (name, price, id)
        cursor.execute(guncelle_sorgusu, guncelle_verileri)
        print("Veri güncellendi.")
    else:
        print("girilen id bulunamadı!")

    con.commit()
    
def deleteProduct(tblName,id):
    kontrol_sorgusu = "SELECT id FROM "+tblName+" WHERE id = ?"
    kontrol_verileri = (id,)
    cursor.execute(kontrol_sorgusu, kontrol_verileri)
    var_mi = cursor.fetchone()
    if var_mi:
        sil_sorgusu = "DELETE FROM "+tblName+" WHERE id = ?"
        sil_verileri = (id,)
        cursor.execute(sil_sorgusu, sil_verileri)
        print("Veri silindi.")
    else:
        print("Bu ID'ye sahip bir satır bulunamadı.")
    con.commit()
createTable("productTbl")
addProduct("productTbl",2,"varan2",0.99)
print(get("productTbl",2,"price"))
