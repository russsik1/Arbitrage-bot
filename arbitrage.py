import os, sys
import time
import telebot
from flask import Flask, request
from telebot import types
from redis import StrictRedis as redis
from classes import *
from config import token, rates, channel


bot = telebot.TeleBot(token)
arb = Arbitrage()
r = Rediska()


def arbitrage():
    arb.get_markets()
    arb.collect()
    arb.filter_()
    arbitrage_markets = arb.show_arbitrage()
    markets = r.get_markets()
    for market in arbitrage_markets:
        
        market_type = ''
        #define market_type
        if arbitrage_markets[market]['buy side volume'] > 30 and arbitrage_markets[market]['sell side volume'] > 30:
            if arbitrage_markets[market]['delta'] > rates['premium']:
                market_type = 'premium'
            elif arbitrage_markets[market]['delta'] > rates['free']:
                market_type = 'free'
        #else:
        if arbitrage_markets[market]['buy side volume'] > 15 and arbitrage_markets[market]['sell side volume'] > 15:
            if arbitrage_markets[market]['delta'] > rates['free'] and arbitrage_markets[market]['delta'] < rates['premium']:
                market_type = 'free'
        
        market_ = market+' '+market_type
        if market_type != '':
            if market_ not in markets:
                r.add_market(market_, arbitrage_markets[market])
                #define mes (message) content
                mes = prepare_message(arbitrage_markets[market], market_type=market_type)
                bot.send_message(channel[market_type], mes)
                time.sleep(3) #wait 3 sec after messages



def notification():
    pass


def kick_expire_members():
    pass


regular_procedures = {
    'signal': {
        'timer': time.time(),
        'update every': 1, #minutes
        'lag': 0,
        'method': arbitrage,
    },
    'notifications': {
        'timer': time.time(),
        'update every': 60, #minutes
        'lag': 0,
        'method': notification,
    },
    'member kick': {
        'timer': time.time(),
        'update every': 60, #minutes
        'lag': 0,
        'method': kick_expire_members,
    },
}




while True:
    for procedure in regular_procedures:
        st = regular_procedures[procedure]['timer']
        update_every = regular_procedures[procedure]['update every']
        lag = regular_procedures[procedure]['lag']
        method = regular_procedures[procedure]['method']
        if time.time() > st:
            regular_procedures[procedure]['timer'] = round(((time.time()+lag)-60*update_every/2)/60/update_every)*60*update_every+60*update_every
            method()
        time.sleep(5)





