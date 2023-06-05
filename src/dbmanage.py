import sqlite3
class dbmanage():
    def __init__(self):
        self.con=sqlite3.connect("proje.db")
        self.cursor=self.con.cursor()

    def createTable(self,tblName):
        sqlText="CREATE TABLE IF NOT EXISTS "+ tblName+" (id INT, name TEXT, price DOUBLE)"
        self.cursor.execute(sqlText)
        self.con.commit

    def addProduct(self,tblName,id, name, price):
        kontrol_sorgusu = "SELECT id FROM "+tblName+" WHERE id = ?"
        kontrol_verileri = (id,)
        self.cursor.execute(kontrol_sorgusu, kontrol_verileri)
        var_mi = self.cursor.fetchone()
        if var_mi:
            print("Bu ID ile zaten bir satır var.")
        else:
            sorgu = "INSERT INTO "+tblName+" (id, name, price) VALUES (?, ?, ?)"
            veriler = (id, name, price)
            self.cursor.execute(sorgu, veriler)
            print("Veri başarıyla eklendi.")
        self.con.commit()
    def get(self,tblName,id,colName):
        data=""
        self.cursor.execute(f"SELECT {colName} FROM {tblName} WHERE id = ?", (id,))
        result = self.cursor.fetchone()
        if result:
            data = result[0]
        else:
            print("Eşleşen ID bulunamadı.")
        self.con.commit
        return data
        return data
    def isThere(self,tblName,id):
        kontrol_sorgusu = "SELECT id FROM "+tblName+" WHERE id = ?"
        kontrol_verileri = (id,)
        self.cursor.execute(kontrol_sorgusu, kontrol_verileri)
        var_mi = self.cursor.fetchone()

        if var_mi:
            return True
        elif id==None:
            return False
        else:
            return False

        con.commit()

    def updateProduct(self,tblName,id, name, price):
        kontrol_sorgusu = "SELECT id FROM "+tblName+" WHERE id = ?"
        kontrol_verileri = (id,)
        self.cursor.execute(kontrol_sorgusu, kontrol_verileri)
        var_mi = self.cursor.fetchone()

        if var_mi:
            guncelle_sorgusu = "UPDATE "+tblName+" SET name = ?, price = ? WHERE id = ?"
            guncelle_verileri = (name, price, id)
            self.cursor.execute(guncelle_sorgusu, guncelle_verileri)
            print("Veri güncellendi.")
        else:
            print("girilen id bulunamadı!")

        self.con.commit()
        
    def deleteProduct(self,tblName,id):
        kontrol_sorgusu = "SELECT id FROM "+tblName+" WHERE id = ?"
        kontrol_verileri = (id,)
        self.cursor.execute(kontrol_sorgusu, kontrol_verileri)
        var_mi = self.cursor.fetchone()
        if var_mi:
            sil_sorgusu = "DELETE FROM "+tblName+" WHERE id = ?"
            sil_verileri = (id,)
            self.cursor.execute(sil_sorgusu, sil_verileri)
            print("Veri silindi.")
        else:
            print("Bu ID'ye sahip bir satır bulunamadı.")
        self.con.commit()


