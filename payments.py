import bitcoin as pbt
import blockcypher as bc
import time
import hashlib
import string
import codecs
import base58
import ecdsa
import random
#from cryptocurrency_wallet_generator.currencies.litecoin import Litecoin
#from cryptocurrency_wallet_generator.currencies.bitcoin import Bitcoin
import sqlite3
from config import dbname, bctoken
from classes import *
from dbmanager import *




class Litecoin_wallet_generator:
    
        """ Litecoin Wallet Generator v0.1
            Pedro Fortes - 02/2018
            https://pypi.python.org/pypi/ecdsa - ECDSA manual"""

        def __init__(self):
            self.privkey = ''
            self.pubkey  = ''
            self.pubaddr = ''

            self.generate()
 
        def generate(self, seed=None):

            if(seed==None): seed = str(time.time()) + ''.join([random.choice(string.ascii_uppercase + string.digits) for x in range(20)])

            oPk = hashlib.sha256(seed.encode())
            self.privkey = oPk.hexdigest()
            
            # SECP256k1 - Bitcoin elliptic curve
            oSk = ecdsa.SigningKey.from_string(oPk.digest(), curve=ecdsa.SECP256k1)                    
            oVk = oSk.get_verifying_key()

            hexlify = codecs.getencoder('hex')
             
            self.pubkey = str(hexlify(b'\04' + oVk.to_string())[0].decode('utf-8'))
            #print(self.pubkey)
            ripemd160 = hashlib.new('ripemd160')
            ripemd160.update(hashlib.sha256(codecs.decode(self.pubkey, "hex")).digest())

            middle_man = b'\x30' + ripemd160.digest()
            checksum = hashlib.sha256(hashlib.sha256(middle_man).digest()).digest()[:4]        
            binary_addr = middle_man + checksum
            
            self.pubaddr = base58.b58encode(binary_addr)
    
            return (self.privkey, self.pubaddr)

        def __str__(self):    
            return 'Private Key: {0}\nPublic Key: {1}'.format(self.privkey, self.pubaddr)



class Payments:
    
    def __init__(self, bctoken=bctoken):
        self.token = bctoken
        self.dbname = dbname
        self.ltcgen = Litecoin_wallet_generator()
        
    def generate_address(self, chat_id, coin):
        def real(chat_id=chat_id, coin=coin):
            if coin == 'btc':
                #priv, addr = generate_wallet("Bitcoin")
                priv = pbt.random_key()
                pub = pbt.privtopub(priv)
                addr = pbt.pubtoaddr(pub)
                addr = self.record_to_addressdb(chat_id, coin, addr, priv)
            elif coin == 'ltc':
                #priv, addr = generate_wallet("Litecoin")
                priv, addr = self.ltcgen.generate()
                addr = self.record_to_addressdb(chat_id, coin, addr, priv)
            return addr
        def test(chat_id=chat_id, coin=coin):
            if coin == 'btc':
                b = bc.generate_new_address(api_key=self.token, coin_symbol='bcy')
                addr = b['address']
                priv = b['private']
                self.record_to_addressdb(chat_id, coin, addr, priv)
            elif coin == 'ltc':            
                b = bc.generate_new_address(api_key=self.token, coin_symbol='bcy')
                addr = b['address']
                priv = b['private']
                self.record_to_addressdb(chat_id, coin, addr, priv)
            return addr
        
        
        ########ATTENTION!########ATTENTION!#######ATTENTION!#########
        #addr = test()
        addr = real()
        
        
        return {'success': True, 'addr': addr}
    

    def record_to_addressdb(self, chat_id, coin, addr, priv):
        with sqlite3.connect(self.dbname) as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM " + coin + " WHERE chat_id = (?)", (chat_id,))
            if c.fetchall() == []:
                stmt = "INSERT INTO " + coin + " (chat_id, addr, priv) VALUES (?, ?, ?)"
                args = [(chat_id), (addr), (priv),]
                c.execute(stmt, args)
                conn.commit()
            c.execute("SELECT * FROM " + coin + " WHERE chat_id = (?)", (chat_id,))
            addr = c.fetchall()[0][2]
        return addr
        
        
    def get_balance(self, chat_id, coin):
        addr = self.get_address(chat_id, coin)
        def real(coin=coin):
            if coin in ['btc', 'ltc']:#, 'doge']:
                return bc.get_address_details(addr, coin_symbol=coin)
        def test(coin=coin):
            if coin in ['btc', 'ltc']:
                return bc.get_address_details(addr, coin_symbol='bcy')
        
        
        ########ATTENTION!########ATTENTION!#######ATTENTION!#########
        balance_info = real()
        #balance_info = test()
        
        
        return balance_info


    def get_address(self, chat_id, coin):
        with sqlite3.connect(self.dbname) as conn:
            c = conn.cursor()
            c.execute("SELECT addr FROM {} WHERE chat_id={}".format(coin, chat_id))
            addr = c.fetchall()[0][0]
        return addr
    

    def send_to_bank(self, chat_id, amount, coin):
        #with psycopg2.connect(dbname='testdb', user='r', host='localhost', password='r') as conn:
        #    c = conn.cursor()
        #    c.execute("SELECT priv FROM " + coin + " WHERE chat_id = (%s)", (chat_id,))
        #    priv = c.fetchall()[0][0]
        #if coin in ['btc', 'ltc']:#, 'doge']:
        #    fee = bc.get_blockchain_fee_estimates(coin_symbol=coin)['medium_fee_per_kb']
        #    b = bc.simple_spend(from_privkey=priv, to_address=bank[coin], to_satoshis=amount, coin_symbol=coin, api_key=self.token)
            #--------------test
            #fee = bc.get_blockchain_fee_estimates(coin_symbol='bcy')['medium_fee_per_kb']
            #amount = amount - fee
            #b = bc.simple_spend(from_privkey=priv, to_address=bank[coin], to_satoshis=amount, coin_symbol='bcy', api_key=self.token)
        #elif coin in 'eth':
        #    pass
        #return b
        pass

    
    





    
