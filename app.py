import os
import telebot
from flask import Flask, request
from telebot import types
from redis import StrictRedis as redis
from config import *
from classes import *
from dbmanager import *
from payments import Payments


bot = telebot.TeleBot(token)
server = Flask(__name__)
r = Rediska()
db = DBmanager()
pay = Payments()




@bot.message_handler(commands=['start'])
def getMessage(message):
    chat_id = message.chat.id
    #botan.track(config.botan_token, chat_id, None, message.text)
    res = db.get(message.chat.id)
    #if new user (does not exists in db)
    if res == {}:
        #Добавить в базу
        db.add_new_user(message)
        r.set(message.chat.id, {'lang': 'eng'})
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for lang in langs:
            markup.row(lang)
        msg = bot.send_message(message.chat.id, "Select language", reply_markup=markup)
        bot.register_next_step_handler(msg, language_select)
    else:
        lang = res['lang']
        bot.send_message(message.chat.id, extxt['welcome back'][lang]+'%s'%message.from_user.first_name+"!")
        main_menu(message)
    

def language_select(message):
    if message.text == extxt['back']:
        settings_menu(message)
    elif message.text not in langs.keys():
        msg = bot.send_message(message.chat.id, extxt['error'])
        bot.register_next_step_handler(msg, language_select)
    else:
        r.set(message.chat.id, {'lang': langs[message.text]})
        db.update(message.chat.id, {'lang': langs[message.text]})
        main_menu(message)
    return True
    
    
def main_menu(message):
    res = r.get(message.chat.id)
    lang = res['lang']
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(mainmenubtn['wtf'][lang], mainmenubtn['join premium'][lang])
    markup.row(mainmenubtn['settings'][lang], mainmenubtn['why premium'][lang])
    bot.send_message(message.chat.id, "Main menu", reply_markup=markup)
    bot.register_next_step_handler(message, main_menu_select)


def main_menu_select(message):
    res = r.get(message.chat.id)
    lang = res['lang']
    select = message.text
    if select == mainmenubtn['wtf'][lang]:
        msg = bot.send_message(message.chat.id, extxt['wtf'][lang], parse_mode='markdown', disable_web_page_preview=True)
        bot.register_next_step_handler(msg, main_menu_select)

    elif select == mainmenubtn['join premium'][lang]:
        payment_menu(message)
        
    elif select == mainmenubtn['settings'][lang]:
        settings_menu(message)

    elif select == mainmenubtn['why premium'][lang]:
        msg = bot.send_message(message.chat.id, extxt['why premium'][lang], parse_mode='markdown')
        bot.register_next_step_handler(msg, main_menu_select)
    else:
        msg = bot.send_message(message.chat.id, extxt['try again'][lang])
        bot.register_next_step_handler(msg, main_menu_select)



        
        
        
        
        
def settings_menu(message):
    res = r.get(message.chat.id)
    lang = res['lang']
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(settingsbtn['change lang'][lang], settingsbtn['contact us'][lang])
    markup.row(backbtn['back to menu'][lang])
    bot.send_message(message.chat.id, mainmenubtn['settings'][lang], reply_markup=markup)
    bot.register_next_step_handler(message, settings_menu_select)


def settings_menu_select(message):
    res = r.get(message.chat.id)
    lang = res['lang']
    select = message.text
    if select == settingsbtn['change lang'][lang]:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for l in langs:
            markup.row(l)
        markup.row(extxt['back'])
        bot.send_message(message.chat.id, "Select language", reply_markup=markup)
        bot.register_next_step_handler(message, language_select)
    elif select == backbtn['back to menu'][lang]:
        main_menu(message)
        
    elif select == settingsbtn['contact us'][lang]:
        msg = bot.send_message(message.chat.id, extxt['contact us'][lang])
        bot.register_next_step_handler(msg, settings_menu_select)
    else:
        bot.register_next_step_handler(message, settings_menu_select)



def payment_menu(message):
    res = r.get(message.chat.id)
    lang = res['lang']
    select = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(paymentmenubtn['pay in btc'][lang], paymentmenubtn['check btc receipt'][lang])
    markup.row(paymentmenubtn['pay in ltc'][lang], paymentmenubtn['check ltc receipt'][lang])
    markup.row(backbtn['back to menu'][lang])
    bot.send_message(message.chat.id, extxt['payment menu'][lang], reply_markup=markup)
    bot.register_next_step_handler(message, payment_menu_select)



def payment_menu_select(message):
    res = r.get(message.chat.id)
    lang = res['lang']
    user = db.get(message.chat.id)
    select = message.text
    #deposit
    if select == paymentmenubtn['pay in btc'][lang]:
        bot.send_message(message.chat.id, extxt['pay in btc'][lang] %(membership_price['btc'], user['btc_addr']), parse_mode='markdown', disable_web_page_preview=True)
        msg = bot.send_message(message.chat.id, '```%s```'%(user['btc_addr']), parse_mode='markdown')
        bot.register_next_step_handler(msg, payment_menu_select)
    elif select == paymentmenubtn['pay in ltc'][lang]:
        bot.send_message(message.chat.id, extxt['pay in ltc'][lang] %(membership_price['ltc'], user['ltc_addr']), parse_mode='markdown', disable_web_page_preview=True)
        msg = bot.send_message(message.chat.id, '`%s`'%(user['ltc_addr']), parse_mode='markdown')
        bot.register_next_step_handler(msg, payment_menu_select)
    #сheck BTC/LTC receipt
    elif select == paymentmenubtn['check btc receipt'][lang] or select == paymentmenubtn['check ltc receipt'][lang]:
        st = time.time() - user['last_check_receipt']
        if st < 90:
            msg = bot.send_message(message.chat.id, extxt['next try'][lang]%(round(90-st,1)))
            bot.register_next_step_handler(msg, payment_menu_select)
        else:
            update = {}
            #определение валюты и адреса
            coin = 'ltc' if 'LTC' in select else 'btc'
            addr = user[coin+'_addr']
            minimal_payment = membership_price[coin]*.95 #Дадим скидочку из за неопределенности комиссий 
            msg = bot.send_message(message.chat.id, extxt['wait'][lang])
            bot.register_next_step_handler(msg, payment_menu_select)
            #запрос баланса
            b = pay.get_balance(message.chat.id, coin)
            balance_satoshi = b['balance']
            balance = balance_satoshi/100000000
            tx = 'None' if len(b['txrefs']) == 0 else b['txrefs'][0]['tx_hash']
            # баланс на адресе менее необходимой суммы и в бд равны (0 или только пришли поступления и ждут отправки)
            if balance < minimal_payment:
                msg = bot.send_message(message.chat.id, extxt['no receipt'][lang])
                update['last_check_receipt'] = round(time.time())
            # 
            elif balance >= minimal_payment and user[coin+'_addr_info'] == 'None' and balance != user[coin+'_addr_balance']:
                receipt = balance - user[coin+'_addr_balance']
                bot.send_message(message.chat.id, extxt['new receipt'][lang]+"{:.8f}".format(receipt).rstrip('0')+' '+coin.upper())
                bot.send_message(my_chat_id, "{:.8f}".format(receipt).rstrip('0')+' '+coin.upper()+' chat_id: %s' %(message.chat.id))
                db.transct(message.chat.id, addr_from='sender_addr', addr_to=user[coin+'_addr'], amount=receipt, tx=tx, tx_type='deposit', coin=coin)
                update[coin+'_addr_balance'] = balance
                update[coin+'_addr_info'] = 'None'
                update['last_check_receipt'] = round(time.time())
                update['comments'] = 'premium'
                
                #send link
                time.sleep(2)
                linkboard = types.InlineKeyboardMarkup()
                link = types.InlineKeyboardButton(text="Join premium", url="https://t.me/joinchat/AAAAAEl4lv2MT2uOssegWA")
                linkboard.add(link)
                bot.send_message(message.chat.id, "Member's link. Enjoy🍾!", parse_mode='markdown', reply_markup=linkboard)
                    
            #Перевод в банк
            elif balance != user[coin+'_addr_balance'] and user[coin+'_addr_info'] == 'delivering to bank':
                update[coin+'_addr_balance'] = balance
                update[coin+'_addr_info'] = 'None'
                update['last_check_receipt'] = round(time.time())
                bot.send_message(message.chat.id, extxt['no receipt'][lang])
            db.update(message.chat.id, update)
            
            
    elif select == backbtn['back to menu'][lang]:
        main_menu(message)
    
    else:
        bot.register_next_step_handler(message, funds_menu_select)
        return








#@bot.message_handler(commands=['help'])
#def getMessage(message):
    
    #keyboard = types.InlineKeyboardMarkup()
    #url = 'https://github.com/russsik1/inflation_bot/tree/master'
    #link = types.InlineKeyboardButton(text='README.md', url=url)
    #keyboard.add(link)
    #bot.send_message(message.chat.id, help_text, reply_markup=keyboard)

#start
    #add to db
#choose lang
#welcome page
    # what is arbitrage
    # how can i profit from it
    # join!
        #get premium access
            #payment module #add to premium channel if get paid
    # about us
    

#scheduler
    #check every hour every person to expire access to premium
    
    
@bot.message_handler(func=lambda message: True, content_types=['text'])
def getMessage(message):
    main_menu(message)




bot.remove_webhook()
bot.polling(none_stop=True)