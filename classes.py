import requests
import pandas as pd
from redis import StrictRedis as redis
import json
import time
from config import redis_db


class BitfinexMini(object):
    
    PROTOCOL = "https"
    HOST = "api.bitfinex.com"
    VERSION = "v2"
        
    def get_tickers(self, tickers=[]):
        if len(tickers)==0:
            tickers = self.get_symbols(v='v2')
        tickers = ','.join(tickers)
        d = requests.get('https://api.bitfinex.com/v2/tickers?symbols=%s' %tickers).json()
        return d
    
    def get_symbols(self, v='v1'):
        d = requests.get('https://api.bitfinex.com/v1/symbols').json()
        if v=='v2':
            d = ['t'+x.upper() for x in d]
        return d


class BittrexMini(object):
    
    def get_markets(self):
        d = requests.get('https://bittrex.com/api/v1.1/public/getmarketsummaries').json()
        return d['result']

class BinanceMini(object):
        
    def get_allBookTickers(self):
        #d = requests.get('https://api.binance.com/api/v1/ticker/allBookTickers').json()
        d = requests.get('https://api.binance.com/api/v1/ticker/24hr').json()
        return d






class Arbitrage(object):
    
    def __init__(self):
        #self.bittrex_markets = {}
        #self.bitfinex_markets = {}
        #self.binance_markets = {}
        self.bittrex_api = BittrexMini()
        self.bitfinex_api = BitfinexMini()
        self.binance_api = BinanceMini()
        self.fees = {
            'withdraw': pd.read_csv('wfees.csv', sep='|'),
            'trade': {
                'bittrex': .0025,
                'binance': .001,
                'bitfinex': .002,
            },
        }
        self.trade_size = {
            'bittrex': [0.1, 0.5]
        }
    
    def wfee(self, exchange, ticker):
        return self.fees['withdraw'].loc[(self.fees['withdraw'].exchange==exchange)&(self.fees['withdraw'].ticker==ticker)]['fee'].values[0]
        
    def get_markets(self, market=False):
        if market == 'bittrex':
            self.bittrex_markets = self.bittrex_api.get_markets()
        elif market == 'bitfinex':
            self.bitfinex_markets = self.bitfinex_api.get_tickers()
        elif market == 'binance':
            self.binance_markets = self.binance_api.get_allBookTickers()
        else:
            self.bittrex_markets = self.bittrex_api.get_markets()
            self.bitfinex_markets = self.bitfinex_api.get_tickers()
            self.binance_markets = self.binance_api.get_allBookTickers()
        return 

    def collect(self, bittrex=0, binance=0, bitfinex=0):
        if bittrex==0:
            bittrex = self.bittrex_markets
        if bitfinex==0:
            bitfinex=self.bitfinex_markets
        if binance==0:
            binance=self.binance_markets
        br_l = {}
        for m in bittrex:
            #Change Bitcoin Cash ticker from BCC to BCH
            market = m['MarketName'] if 'BCC' not in m['MarketName'] else m['MarketName'].replace('BCC', 'BCH')
            br_l[market] = {
                'bid': m['Bid'],
                'ask': m['Ask'],
                'last': m['Last'],
                'baseVolume':m['BaseVolume']
            }
        bf_l = {}
        for m in bitfinex:
            market = '%s-%s' %(m[0][-3:]+'T', m[0][1:-3]) if 'USD' in m[0] else '%s-%s' %(m[0][-3:], m[0][1:-3])
            bf_l[market] = {
                'bid': m[1],
                'ask': m[3],
                'last': m[7],
                'bidQty': m[2],
                'askQty': m[4],
                'baseVolume': m[8]*m[7]
            }
        bn_l = {}
        for m in binance:
            market = '%s-%s' %(m['symbol'][-4:], m['symbol'][:-4]) if 'USDT' in m['symbol'] else '%s-%s' %(m['symbol'][-3:], m['symbol'][:-3])
            bn_l[market] = {
                'bid': m['bidPrice'],
                'ask': m['askPrice'],
                'bidQty': m['bidQty'],
                'askQty': m['askQty'],
                'baseVolume': float(m['quoteVolume']),
            }
        self.bittrex_collect = br_l
        self.bitfinex_collect = bf_l
        self.binance_collect = bn_l
        return {'bittrex': br_l, 'bitfinex': bf_l, 'binance': bn_l}

    def filter_(self, bittrex=0, binance=0, bitfinex=0):
        #brbf, brbn, bnbf
        if bittrex==0:
            bittrex = self.bittrex_collect
        if bitfinex==0:
            bitfinex=self.bitfinex_collect
        if binance==0:
            binance=self.binance_collect
        l = {
            'bittrex bitfinex': {},
            'bittrex binance': {},
            'binance bitfinex': {},
        }
        #brbf
        for m in bitfinex:
            if m in bittrex.keys():
                l['bittrex bitfinex'][m] = {
                    'bittrex': {
                        'bid': "{:.8f}".format(bittrex[m]['bid']), 
                        'ask': "{:.8f}".format(bittrex[m]['ask']),
                        'volume': bittrex[m]['baseVolume'],
                    },
                    'bitfinex': {
                        'bid': "{:.8f}".format(bitfinex[m]['bid']), 
                        'ask': "{:.8f}".format(bitfinex[m]['ask']),
                        'volume': bitfinex[m]['baseVolume'],
                    },
                }
        #brbn
        for m in bittrex:
            if m in binance.keys():
                l['bittrex binance'][m] = {
                    'bittrex': {
                        'bid': "{:.8f}".format(bittrex[m]['bid']), 
                        'ask': "{:.8f}".format(bittrex[m]['ask']),
                        'volume': bittrex[m]['baseVolume'],
                    },
                    'binance': {
                        'bid': binance[m]['bid'], 
                        'ask': binance[m]['ask'],
                        'volume': binance[m]['baseVolume'],
                    },
                }
        #bnbf
        for m in bitfinex:
            if m in binance.keys():
                l['binance bitfinex'][m] = {
                    'binance': {
                        'bid': binance[m]['bid'], 
                        'ask': binance[m]['ask'],
                        'volume': binance[m]['baseVolume'],
                    },
                    'bitfinex': {
                        'bid': "{:.8f}".format(bitfinex[m]['bid']), 
                        'ask': "{:.8f}".format(bitfinex[m]['ask']),
                        'volume': bitfinex[m]['baseVolume'],
                    },
                }
        return l
    
    def show_arbitrage(self, dlt=.05):
        
        def calc_profit(q, m, buyprice, buy_exchange, sellprice, sell_exchange):
            buyprice = float(buyprice)
            sellprice = float(sellprice)
            buy_f = 1 - self.fees['trade'][buy_exchange]
            buy_q = q * buy_f
            wfee = self.wfee(buy_exchange, m.split('-')[1])
            sell_f = 1 - self.fees['trade'][sell_exchange]
            sell_q = buy_q * sell_f
            profit = (buy_q / buyprice - wfee) * sellprice - q
            minc = wfee*sellprice*sell_f / (sellprice*sell_f/buyprice/buy_f - 1 - .05)
            return {'profit': round(profit, 8), 'percent': round(profit/q*100, 2), 'minimal count': minc}
        
        self.get_markets()
        self.collect()
        exc_pairs = self.filter_()
        l = {}
        for exc_pair in exc_pairs:
            for m in exc_pairs[exc_pair]:
                #if delta between 1st exc bid and 2nd exc ask
                bid0 = float(exc_pairs[exc_pair][m][exc_pair.split(' ')[0]]['bid'])
                ask1 = float(exc_pairs[exc_pair][m][exc_pair.split(' ')[1]]['ask'])
                delta0 = abs((ask1-bid0)/bid0)
                #if delta between 2nd exc bid and 1st exc ask
                bid1 = float(exc_pairs[exc_pair][m][exc_pair.split(' ')[1]]['bid'])
                ask0 = float(exc_pairs[exc_pair][m][exc_pair.split(' ')[0]]['ask'])
                delta1 = abs((ask0-bid1)/bid1)
                if delta0 > dlt or delta1 > dlt:
                    buy_exchange = exc_pair.split(' ')[1]
                    sell_exchange = exc_pair.split(' ')[0]
                    if delta0 > delta1:
                        delta = delta0
                        buyprice = exc_pairs[exc_pair][m][exc_pair.split(' ')[0]]['bid']
                        sellprice = exc_pairs[exc_pair][m][exc_pair.split(' ')[1]]['ask']
                        buy_side_volume = exc_pairs[exc_pair][m][exc_pair.split(' ')[0]]['volume']
                        sell_side_volume = exc_pairs[exc_pair][m][exc_pair.split(' ')[1]]['volume']
                    else:
                        delta = delta1
                        buyprice = exc_pairs[exc_pair][m][exc_pair.split(' ')[1]]['bid']
                        sellprice = exc_pairs[exc_pair][m][exc_pair.split(' ')[0]]['ask']
                        buy_side_volume = exc_pairs[exc_pair][m][exc_pair.split(' ')[1]]['volume']
                        sell_side_volume = exc_pairs[exc_pair][m][exc_pair.split(' ')[0]]['volume']
                        
                        
                    
                    p = calc_profit(.1, m, buyprice, buy_exchange, sellprice, sell_exchange)
                    l[m] = {
                        'market': m,
                        'buy': buy_exchange,
                        'buy price': buyprice,
                        'sell': sell_exchange,
                        'sell price': sellprice,
                        'delta': delta,
                        'buy side volume': buy_side_volume,
                        'sell side volume': sell_side_volume,
                        '0.1 trade profit': calc_profit(.1, m, buyprice, buy_exchange, sellprice, sell_exchange)['profit'],
                        "0.1 {} trade %profit".format(m.split('-')[0]): calc_profit(.1, m, buyprice, buy_exchange, sellprice, sell_exchange)['percent'],
                        '0.5 trade profit': calc_profit(.5, m, buyprice, buy_exchange, sellprice, sell_exchange)['profit'],
                        "0.5 {} trade %profit".format(m.split('-')[0]): calc_profit(.5, m, buyprice, buy_exchange, sellprice, sell_exchange)['percent'],
                        "minimal buy count": "{:.4f} {}".format(p['minimal count'], m.split('-')[0])
                    }
        return l





class Rediska(object):
    
    def __init__(self, db=redis_db):
        self.r = redis(db=db)
        
    def get(self, key):
        try:
            return json.loads(self.r.get(key).decode("UTF-8").replace("'", '"'))
        except:
            return {}
    
    def get_markets(self):
        all_keys = self.r.keys()
        markets = [x.decode("UTF-8") for x in all_keys if b'f' in x or b'p' in x]
        return markets
    
    def add_market(self, market, value):
        self.r.set(market, value)
        self.r.expire(market, 10800)
        return {'success': True}
    
    def set(self, key, update):
        lib = self.get(key)
        for i in update:
            lib[i] = update[i]
        self.r.set(key, lib)

        


        
def prepare_message(m, market_type):
    if market_type=='free':
        s = '🔔 ' + m['market'] + '\n'+\
            'Buy: ' + m['buy'] + ' ' + m['buy price'] + '\n'+\
            'Sell: ' + m['sell'] + ' ' + m['sell price'] + '\n'+\
            'Difference: ' + "{:.2f}".format(m['delta']*100)+'%\n'
        s+= '💰 0.1BTC trade profit after fees: ' if 'BTC' in m['market'] else '💰 0.5ETH trade profit with fee: '
        s+= '%s BTC'%(m['0.1 trade profit']) if 'BTC' in m['market'] else '%s ETH'%(m['0.5 trade profit'])
    elif market_type=='premium':
        s = '💎 ' + m['market'] + '\n'+\
            'Buy: ' + m['buy'] + ' ' + m['buy price'] + '\n'+\
            'Sell: ' + m['sell'] + ' ' + m['sell price'] + '\n'+\
            'Difference: ' + "{:.2f}".format(m['delta']*100)+'%\n'+\
            m['buy']+' volume: ' + "{:.2f}".format(m['buy side volume'])+'\n'+\
            m['sell']+' volume: ' + "{:.2f}".format(m['sell side volume'])+'\n'
        s+= '💰 0.1BTC trade profit after fees: ' if 'BTC' in m['market'] else '💰 0.5ETH trade profit with fee: '
        s+= '%s BTC'%(m['0.1 trade profit']) if 'BTC' in m['market'] else '%s ETH'%(m['0.5 trade profit'])
    return s










