import json
import logging
import os
import time
import datetime

import akshare as ak

from ..database.sqlal import simple_session
from ..model.stock import StockINFO,DailyPrice,StockIndicator
from ..tools.tusharetool import init_stock_by_ts,init_stock_day_price
from ..tools.aksharetool import get_stock_indicator

def init_stockinfo(session = None):
    """生成股票基本信息"""
    if not bool(session):
        session = simple_session()
    
    logging.info("Init STOCK INFO")
    session.query(StockINFO).delete()
    session.commit()

    df = init_stock_by_ts()
    stock_info = [StockINFO(**each) for each in df.to_dict("records")]
    session.add_all(stock_info)
    session.commit()
    session.close()

def init_price(session = None):
    """生成股票每日价格信息"""
    if not bool(session):
        session = simple_session()
    
    logging.info("Init stock price")
   
    session.query(DailyPrice).delete()
    session.commit()
    ticks = session.query(DailyPrice.ticker).all()
    tickers = [i[0] for i in ticks]

    # 得到股票列表
    stocks = session.query(StockINFO.ticker,StockINFO.name).all()
    for stock in stocks:
        if stock.ticker not in tickers:
            df = init_stock_day_price(stock.ticker,'20210511','20210927')
            logging.info("导入 [%s]数据"%(stock.name))
            print("导入 [%s]数据"%(stock.name))
            prices = [DailyPrice(**each) for each in df.to_dict("records")]
            session.add_all(prices)
            session.commit()
        else:
            logging.info("已导入[%s]" % stock.name)
            print("已导入[%s]" % stock.name)
        # time.sleep(6)
    
    session.close()

def init_indicator(session = None):
    """初始化个股各种指标"""
    if not bool(session):
        session = simple_session()
    
    session.query(StockIndicator).delete()
    session.commit()
    logging.info("Init stock indicator")
    # 得到股票列表
    stocks = session.query(StockINFO.ticker,StockINFO.name).all()
    for stock in stocks:
        df = get_stock_indicator(stock.ticker)
        logging.info("导入 [%s]基本面数据"%(stock.name))
        indicators = [StockIndicator(**each) for each in df.to_dict("records")]
        session.add_all(indicators)
        session.commit()
    logging.info("导入完毕！")
    session.close()

def add_indicator(date=None):
    """导入指定日期的指标数据"""
    if bool(date):
        date = datetime.datetime.now().strftime("%Y-%m-%d")
    session = simple_session()
    stocks = session.query(StockINFO.ticker,StockINFO.name).all()
    for stock in stocks:
        df = ak.stock_a_lg_indicator(stock=stock.ticker[:6])
        data = df[df['trade_date'] == date]
        logging.info("导入 [%s]基本面数据"%(stock.name))
        indicators = [StockIndicator(**each) for each in data.to_dict("records")]
        session.add_all(indicators)
        session.commit()
    logging.info("导入完毕！")
    session.close()

if __name__ == "__main__":
    init_price()







