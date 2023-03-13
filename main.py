import pymysql.cursors    
import classes as cl
import os

def choise():
    while (True):
        pr_command = input( "Вернуться назад: 1\n"
                            "> ")
        if (pr_command == "1"):
            break
        else:
            print("Упс! Такой команды нет!")

if __name__=="__main__":
    connection = pymysql.connect(host='localhost',
                                user='root',
                                password='',
                                database='myBase',
                                cursorclass=pymysql.cursors.DictCursor)
    
    user = cl.User(connection)
    product = cl.Product(connection)
    basket = cl.Basket(connection)
    
    while(True):
        comand = input("Войти: 1\n"
                       "Зарегистрироваться: 2\n"
                       "Посмотреть товары: 3\n"
                       "Посмотреть корзину: 4\n"
                       "Выход: 5\n"
                       "> ")
        
        match comand:
            case '1':
                os.system('clear')
                login = input("Введите логин: ")
                password = input("Введите пароль: ")
                user.logIn(login, password)
                pass
            case '2':
                os.system('clear')
                login = input("Введите логин: ")
                password = input("Введите пароль: ")
                fname = input("Введите имя: ")
                sname = input("Введите фамилию: ")
                user.registration(login, password, fname, sname)
                pass
            case '3':
                os.system('clear')
                product.getProducts()
                choise()
                os.system('clear')
                pass
            case '4':
                os.system('clear')
                if (user.isConected()):
                    basket.getbasket(user.getID())
                    choise()
                    os.system('clear')
                else:
                    print("Вы не вошли в систему!")
                pass
            case '5':
                os.system('clear')
                break
            case _:
                os.system('clear')
                print("Упс! Такой команды нет!")
                pass