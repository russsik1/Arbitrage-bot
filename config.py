token = '###########################################' #arcrbot
bctoken = '#########################################'
dbname = 'main.db'
redis_db = 14
my_chat_id = '#########'
bank = {
    #'btc': 'C7CieqVGJVGtEDsB6JDwwdJnAeodKTbs4N', #bcy
    'btc': '1AYhX8C3jNzHtTF77osCkJmfSuLW7rR9ea',
    'ltc': 'None',
    'doge': 'None',
    'eth': 'None',
}


membership_price = {
    'btc': 0.005,
    'ltc': 0.3,
}

channel = {
    'premium': '###############',
    'free': '#########',
}

rates = {
    'free': .03,
    'premium': .8,
}


langs = {
    '🇬🇧 English': 'eng',
    '🇷🇺 Русский': 'rus',
    '🇨🇳 中文（即将推出)': 'eng',#'chi',
    '🇩🇪 Deutsch (in Kürze)': 'eng',#'deu',
    '🇰🇷 한국 (곧 제공 예정)': 'eng',#'kor',
    '🇪🇸 Español (próximamente)': 'eng', #'spa', 
    '(عربي (قريبًا 🇸🇦': 'eng', #'ara',
    '🇮🇹 italiano (presto disponibile)': 'eng',#'ita',
    '🇵🇹 Português (em breve)': 'eng',#'por',
    '🇯🇵 日本（近日公開予定）': 'eng',#'jap',
}






mainmenubtn = {
    'wtf': {
        'rus': 'Как работет арбитраж💡',
        'eng': 'What is arbitrage💡',
    },
    'join premium': {
        'rus': 'Получить премиум доступ🔑',
        'eng': 'Get premium access🔑'
    },
    'why premium': {
        'rus': 'Преимущества премиум подписки⭐️',
        'eng': 'Why premium⭐️',
    },
    'settings': {
        'rus': 'Настройки🔧',
        'eng': 'Settings🔧',
    },
}


settingsbtn = {
    'change lang': {
        'rus': 'Change language🇬🇧',
        'eng': 'Change language🇬🇧',
    },
    'contact us': {
        'rus': '💌Обратная связь',
        'eng': '💌Contact us',
    },
}


backbtn = {
    'back to menu': {
        'rus': '🔙Меню',
        'eng': '🔙Menu',
    },
    'back to settings': {
        'rus': '🔙Назад в настройки',
        'eng': '🔙Back to settings',
    },
}


paymentmenubtn = {
    'pay in btc': {
        'rus': 'Оформить подписку в BTC',
        'eng': 'Subscribe in BTC',
    },
    'check btc receipt': {
        'rus': 'Проверить поступления BTC 🌏',
        'eng': 'Check BTC receipt🌏',
    },
    'pay in ltc': {
        'rus': 'Оформить подписку в LTC',
        'eng': 'Subscribe in LTC',
    },
    'check ltc receipt': {
        'rus': 'Проверить поступления LTC 🌏',
        'eng': 'Check LTC receipt🌏',
    },
}


extxt = {
    'why premium': {
        'rus': 'Члены premium канала получают сигналы монет с большим объемом торгов и средней доходностью *9.7%%* от сделки после вычета комиссий. Стоимость подписки для вступления в premium канал составляет: *%s BTC* или *%s LTC*. Доступ предоставляется на месяц в течение которого выполняется 24 часовая 👷 поддержка. Остались вопросы, свяжитесь @goldmiller. Удачи!' %(membership_price['btc'], membership_price['ltc']),
        'eng': "Members of the premium channel receive signals of coins with a large volume of trades and with an average 9.7%% trade profit after paying fees. The subscription price for joining premium channel is: %s BTC or *%s LTC*. Access is granted for a month during which You have 24/7 👷 support. Have any questions, please contact @goldmiller. Good luck!" %(membership_price['btc'], membership_price['ltc']),
    },
    'welcome back': {
        'rus': 'С возвращением, ',
        'eng': 'Welcome back, ',
    },
    'try again': {
        'rus': 'Что то пошло не так, попробуйте еще раз',
        'eng': 'Ops, try again',
    },
    'contact us': {
        'rus': 'По всем вопросам писать сюда: @goldmiller',
        'eng': 'Any questions, please contact @goldmiller',
    },
    'next try': {
        'rus': 'Следующая попытка через %s секунд',
        'eng': 'Next try in %s sec',
    },
    'wait': {
        'rus': 'Пожалуйста, ждите, это может занять некоторое время⌛️',
        'eng': 'Please wait, it could take some time⌛️'
    },
    'no receipt': {
        'rus': 'Нет зачислений по счету',
        'eng': 'No account crediting'
    },
    'new receipt': {
        'rus': 'Поздравляем! платеж прошел успешно, ссылка в premium канала будет доступна в ближайшее время. Получено: ',
        'eng': 'Payment successfully verified, the link will be available soon. Payament amount: ',
    },
    'pay in btc': {
        'rus': 'Выполните транзакцию на данный адрес суммой *%s BTC*. Проверить статус транзакции можно [здесь](https://blockchain.info/address/%s). После выполнения транзакции нажмите "Подтвердить оплату BTC 🌏". Вы получите ссылку для вступления в premium канал.\nАдрес перевода 👇 скопируйте:',
        'eng': 'Send *%s* BTC to the address below. You can check the transaction status [here](https://blockchain.info/address/%s). After the transaction is complete, tap "Confirm payment BTC 🌏". You will receive a link to join the premium channel.\nBTC address 👇 copy:',
    },
    'pay in ltc': {
        'rus': 'Выполните транзакцию на данный адрес суммой *%s LTC*. Проверить статус транзакции можно [здесь](https://bchain.info/LTC/addr/%s). После выполнения транзакции нажмите "Подтвердить оплату LTC 🌏". Вы получите ссылку для вступления в premium канал.\nАдрес перевода 👇 скопируйте:',
        'eng': 'Send *%s* LTC to the address below. You can check the transaction status [here](https://bchain.info/LTC/addr/%s). After the transaction is complete, tap "Confirm payment LTC 🌏". You will receive a link to join the premium channel.\nLTC address 👇 copy:',
    },
    'error': 'Error',
    'back': '🔙',
    'wtf': {
        'rus': '[Арбитраж](https://www.investopedia.com/terms/a/arbitrage.asp) - операция, при которой осуществляется покупка актива на одной бирже для следующей перепродажи на другой бирже. Арбитраж возникает за счет неэффективностей рынка, и не существовал бы если все рынки торговались синхронно. Приведем пример, альткоин торгуется на двух биржах, на одной из них цена монеты начала расти. Для извлечения прибыли необходимо купить альткоин на бирже, где цена ниже и продать на той бирже где цена выше. Разница с покупки/продажи с учетом комиссий составит прибыль.\n Переходите в бесплатный канал @arcrb для получения ограниченных сигналов со средней доходностью ~2%% от сделки.\n В нашем премиум канале доступны сигналы с большими объемами со средней доходностью *9.7%%* от сделки. Для вступления выберите в меню соответствующую кнопку', #%(channel['free']),
        'eng': "[Arbitrage](https://www.investopedia.com/terms/a/arbitrage.asp) is the simultaneous purchase and sale of an asset to profit from a difference in the price. It is a trade that profits by exploiting the price differences of identical or similar financial instruments on different markets or in different forms. Arbitrage exists as a result of market inefficiencies and would therefore not exist if all markets were perfectly efficient. For example, the altcoin is trading on two exchanges. The price starts growing on first exchange while price on second exchange doesn't change. A trader can buy the altcoin on the first exchange and immediately sell the same altcoin on the second exchange. Difference in prices after fees gives a profit.\n Join owr free channel @arcrb to get limited signals with average 2%% profit.\n Become a member of premium channel to get signals with avarage *9.7%%* profit.", #%(channel['free']),
    },
    'payment menu': {
        'rus': 'Выберите валюту и для оплаты доступа в premium канал',
        'eng': 'Choose coin to pay premium channel subscription',
    }
}








"""
BOT START DESCRIPTION >>>

⭐️Premium access⭐️
BTC🔀ETH🔀USD
🇬🇧 Arbitrage. Cross exchange trading
🇷🇺 Межбиржевой арбитраж
🇨🇳 套利。 交叉交易
🇩🇪 Arbitrage. Handel zwischen Börsen
🇰🇷 사는 즉시 팔아 차액을 버는 거래
🇪🇸 Arbitraje. Intercambio cruzado
موازنة. تداول الصرف 🇸🇦
🇮🇹 Arbitraggio. Cross exchange
🇵🇹 Arbitragem. Negociação de troca cruzada
🇯🇵 アービトラージ。 クロス取引

<<< END
"""




