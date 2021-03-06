import tushare as ts

_TOKEN = '980d147319216e14b62ea909cfb30320ae7b106dfdede6571e61ef09'
ts.set_token(_TOKEN)
pro = ts.pro_api()
pro = ts.pro_api(_TOKEN)

def init_stock_by_ts():
    df = pro.stock_basic(exchange='', list_status='L', fields='ts_code,name,industry,list_date')
    index = {
        'ts_code':'ticker',
        'industry':'instrument',
        'name':'name',
        'list_date':'IPO_date'
    }
    df = df.rename(columns=index)
    return df

def init_stock_day_price(ts_code,start_dt,end_dt):
    df = pro.daily(ts_code=ts_code, start_date=start_dt, end_date=end_dt)
    index = {
        'ts_code':'ticker',
        'trade_date' : 'date',
        'open' : 'open_price',
        'high' : 'high_price',
        'low' : 'low_price',
        'close' : 'close_price',
        'pre_close' : 'pre_close',
        'change' : 'change',
        'pct_chg' : 'pct_chg',
        'vol' : 'vol',
        'amount' : 'amount'
    }
    df = df.rename(columns=index)
    return df