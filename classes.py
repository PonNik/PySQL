import pymysql.cursors    

class User:
    def __init__(self, connection):
        self.connect = connection
        self.ID = None

    def logIn(self, login, password):
        with self.connect.cursor() as cursor:
            # Read a single record
            sql = f"SELECT * FROM `users` WHERE ulogin='{login}' AND upassword='{password}'"
            cursor.execute(sql)
            results = cursor.fetchall()
            
            if (len(results) == 0):
                print("Неправильный логин или пароль")
                return -1
            else:
                for result in results:
                    print("Добро пожаловать, " + result['ufirstName'] + " " + result['usecondName'])
                    self.ID = result['uID']
                    self.password = result['upassword']
                return 0
        
    def registration(self, ulogin, upassword, ufirstName, usecondName):
        with self.connect.cursor() as cursor:
            # Read a single record
            sql = f"SELECT * FROM `users` WHERE ulogin='{ulogin}'"
            cursor.execute(sql)
            result = cursor.fetchall()
            
            if (len(result) == 0):
                with self.connect:
                    with self.connect.cursor() as cursor:
                        
                        sql = "INSERT INTO users(ulogin, upassword, ufirstName, usecondName) VALUES (%s, %s, %s, %s)"
                        cursor.execute(sql, (ulogin, upassword, ufirstName, usecondName))
                    self.connect.commit()
                print("Регистрация прошла успешно!")
                return 0
            else:
                print("Этот логин занят!") 
                return -1
            
    def isConected(self):
        if self.ID != None:
            return True
        return False
    
    def getID(self):
        return self.ID
    
    def changePassword(self, password_now, password):
        if (self.password == password_now):
            with self.connect:
                with self.connect.cursor() as cursor:
                    sql = f"UPDATE users SET upassword = '{password}' WHERE uID = '{self.ID}'"
                    cursor.execute(sql)
                self.connect.commit()
            return 0
        else:
            print("Ошибка! Неверный пароль!")
            return -1
    
class Product:
    def __init__(self, connection):
        self.connect = connection
        
    def createnewProduct(self, name, price):
        with self.connect:
            with self.connect.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO Product(ProductName, ProductPrice) VALUES (%s, %s)"
                cursor.execute(sql, (name, price))
            self.connect.commit()
        return 0

    def getProducts(self):
        with self.connect.cursor() as cursor:
            # Read a single record
            sql = "SELECT * FROM Product"
            
            cursor.execute(sql)
            results = cursor.fetchall()
            
            for result in results:
                print(str(result['ProductID']) +" "+ result['ProductName'] +" "+ str(result['ProductPrice']))
        pass

    def changeNameProduct(self, id, new_name):
        with self.connect:
            with self.connect.cursor() as cursor:
                # Create a new record
                sql = f"UPDATE Product SET ProductName = '{new_name}' WHERE ProductID = '{id}'"
                cursor.execute(sql)
            self.connect.commit()
            
    def changePrice(self, id, new_price):
        with self.connect:
            with self.connect.cursor() as cursor:
                # Create a new record
                sql = f"UPDATE Product SET ProductPrice = '{new_price}' WHERE ProductID = '{id}'"
                cursor.execute(sql)
            self.connect.commit()
    
    def addProduct(self, pname, pprice):
        with self.connect:
            with self.connect.cursor() as cursor:
                sql = "INSERT INTO Product(ProductName, ProductPrice) VALUES (%s, %s)"
                cursor.execute(sql, (pname, pprice))
            self.connect.commit()

    def deleteProduct(self, id):
        with self.connect:
            with self.connect.cursor() as cursor:
            
                sql = f"DELETE FROM Product WHERE ProductID = '{id}'"
                cursor.execute(sql)
            self.connect.commit()

class Basket:
    def __init__(self, connection):
        self.connect = connection

    def getbasket(self, uid):
        with self.connect.cursor() as cursor:
            # Read a single record
            sql = f"SELECT ProductName, ProductPrice, pCount FROM Product AS p INNER JOIN basket AS a ON p.ProductID = a.pID AND userID = '{uid}'"
            
            cursor.execute(sql)
            results = cursor.fetchall()
            
            if (len(results) == 0):
                print("корзина пуста")
                return -1
            else:
                for result in results:
                    print(result['ProductName'] +" "+ str(result['ProductPrice']) + " " + str(result["pCount"]))
                return 0
        
    def addProductInBasket(self, pID, userID, pCount):
        with self.connect.cursor() as cursor:
        
            sql = f"SELECT pID FROM basket WHERE pId = {pID} AND userID = '{userID}'"
                
            #sql = f"SELECT * FROM `users` WHERE ulogin='{pID}'"
            cursor.execute(sql)
            result = cursor.fetchall()
                
            if (len(result) != 0):
                with self.connect:
                    with self.connect.cursor() as cursor:
                    # Create a new record
                        sql = f"UPDATE `basket` SET `pCount`=`pCount` + '{pCount}' WHERE userID = '{userID}'"
                        cursor.execute(sql)
                    self.connect.commit()
                return 0
            else:
                with self.connect:
                    with self.connect.cursor() as cursor:
                        sql = "INSERT INTO basket(pID, userID, pCount) VALUES (%s, %s, %s)"
                        cursor.execute(sql,(pID, userID, pCount))
                    self.connect.commit()
                return 0

    def delProductInBasket(self, pID, userID, pCount):
        with self.connect.cursor() as cursor:
        
            sql = f"SELECT pCount FROM basket WHERE pId = {pID} AND userID = '{userID}'"
            
            #sql = f"SELECT * FROM `users` WHERE ulogin ='{pID}'"
            cursor.execute(sql)
            r = cursor.fetchone()
            if r['pCount'] - pCount > 0:
                with self.connect:
                    with self.connect.cursor() as cursor:
                    # Create a new record
                        sql = f"UPDATE `basket` SET `pCount`=`pCount` - '{pCount}' WHERE userID = '{userID}'"
                        cursor.execute(sql)
                    self.connect.commit()
                return 0
            else:
                with self.connect:
                    with self.connect.cursor() as cursor:
                    # Create a new record
                        sql = f"DELETE FROM `basket` WHERE `userid` = {userID} AND `pId` = {pID}"
                        print("Товар удален!")
                        cursor.execute(sql)
                    self.connect.commit()
                return 0
        