import json
import logging
import os
import time

from ..database.sqlal import simple_session
from ..model.stock import StockINFO,DailyPrice
from ..tools.tusharetool import init_stock_by_ts,init_stock_day_price

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

    # 得到股票列表
    stocks = session.query(StockINFO.ticker,StockINFO.name).all()
    for stock in stocks:
        df = init_stock_day_price(stock.ticker,'20140101','20210305')
        logging.info("导入 [%s]数据"%(stock.name))
        prices = [DailyPrice(**each) for each in df.to_dict("records")]
        session.add_all(prices)
        session.commit()
        time.sleep(6)
    
    session.close()

