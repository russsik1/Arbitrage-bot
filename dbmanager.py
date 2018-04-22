import sqlite3
from config import dbname
from payments import Payments




class DBmanager:
    
    def __init__(self, dbname=dbname):
        self.dbname = dbname
#        self.conn = psycopg2.connect(dbname='testdb', user='r', host=server, password='r')
#        self.c = self.conn.cursor()

    def add_new_user(self, message):
        pay = Payments()
        chat_id = message.chat.id
        username = message.from_user.username if message.from_user.username is not None else 'None'
        firstname = message.from_user.first_name if message.from_user.first_name is not None else 'None'
        lastname = message.from_user.last_name if message.from_user.last_name is not None else 'None'
        btc_addr = pay.generate_address(chat_id, 'btc')['addr']
        ltc_addr = pay.generate_address(chat_id, 'ltc')['addr']
        btc_addr_balance = 0
        ltc_addr_balance = 0
        btc_addr_info = 'None'
        ltc_addr_info = 'None'
        last_check_receipt = 0
        payment_date = 0
        last_notification = 0
        referrer = message.text.split(' ')[-1]
        comments = 'free'
        lang = 'eng'
        with sqlite3.connect(self.dbname) as conn:
            c = conn.cursor()
            columns = [
                'chat_id', 'username', 'firstname', 'lastname', 
                'btc_addr', 'btc_addr_balance', 'btc_addr_info', 
                'ltc_addr', 'ltc_addr_balance', 'ltc_addr_info',
                'last_check_receipt', 'payment_date', 'last_notification',
                'referrer', 'comments', 'lang',
            ]
            stmt = 'INSERT INTO users ({}) VALUES ({});'.format(', '.join(columns), ('?, '*len(columns))[:-2])
            args = [
                (chat_id), (username), (firstname), (lastname), 
                (btc_addr), (btc_addr_balance), (btc_addr_info),
                (ltc_addr), (ltc_addr_balance), (ltc_addr_info),
                (last_check_receipt), (payment_date), (last_notification),
                (referrer), (comments), (lang),
            ]
            c.execute(stmt, args)
            conn.commit()
    
    
    def get(self, chat_id):
        with sqlite3.connect(self.dbname) as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE chat_id = (?)", (chat_id,))
            values = c.fetchall()
            lib = {}
            if values != []:
                #c.execute("SELECT column_name FROM information_schema.columns WHERE TABLE_NAME='users';")
                #column_names = [x[0] for x in c.fetchall()]
                c.execute('PRAGMA table_info(users);')
                column_names = [x[1] for x in c.fetchall()]
                values = values[0]
                for i in range(1, len(column_names)):
                    lib[column_names[i]] = values[i]
            return lib
    
    
    def update(self, chat_id, update):
        with sqlite3.connect(self.dbname) as conn:
            c = conn.cursor()
            col_and_val = ", ".join(["%s = '%s'"%(key, update[key]) for key in update])
            stmt = "UPDATE users SET {} WHERE chat_id = {};".format(col_and_val, chat_id)
            c.execute(stmt)
            conn.commit()
            return update
    
    
    def transct(self, chat_id, addr_from, addr_to, amount, tx, tx_type, coin):
        with sqlite3.connect(self.dbname) as conn:
            c = conn.cursor()
            stmt = "INSERT INTO transct (chat_id, addr_from, addr_to, amount, tx, tx_type, coin) VALUES (?, ?, ?, ?, ?, ?, ?)"
            args = (chat_id, addr_from, addr_to, amount, tx, tx_type, coin)
            c.execute(stmt, args)
            conn.commit()
        
    

    
