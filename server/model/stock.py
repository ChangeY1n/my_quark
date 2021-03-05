import datetime

from sqlalchemy import UniqueConstraint, BigInteger, Float, Text, Column, DateTime, ForeignKey, Integer, Sequence, String
from sqlalchemy.sql.sqltypes import Boolean

from ..database.sqlal import Base

class StockINFO(Base):
    """股票信息表"""
    __tablename__ = "stock"
    id = Column(BigInteger,Sequence('stock_id_seq'), primary_key=True)
    ticker = Column(String(8), doc='股票代码',unique = True)
    instrument = Column(String(128), doc='所属行业')
    name = Column(String(String(128)), doc='公司名称')
    IPO_date = Column(DateTime,doc='上市时间')
    create_date = Column(DateTime,doc='创建时间')

class DailyPrice(Base):
    """每日价格"""
    __tablename__ = 'daily_price'
    id = Column(BigInteger,Sequence('daily_price_id_seq'),primary_key=True)
    ticker = Column(String(8),ForeignKey('stock.ticker'),doc = '股票代码')
    date = Column(DateTime,doc = '日期')
    open_price = Column(float,doc = '开盘价')
    high_price = Column(float,doc = '最高价')
    low_price = Column(float,doc = '最低价')
    close_price = Column(float,doc = '收盘价')
    pre_close = Column(float,doc = '昨日收盘点')
    change = Column(float,doc = '涨跌点')
    pct_chg = Column(float,doc = '涨跌幅%')
    vol = Column(float,doc = '成交量')
    amount = Column(float,doc = '成交额(千元)')

class StockIndicator(Base):
    """个股指标"""
    __tablename__ = 'stock_indicator'
    id = Column(BigInteger,Sequence('stock_indicator_id_seq'),primary_key=True)
    ticker = Column(String(8),ForeignKey('stock.ticker'),doc = '股票代码')
    trade_date = Column(DateTime,doc = '交易日')
    pe = Column(float,doc = '市盈率')
    pt_ttm = Column(float,doc = '市盈率TTM')
    pb = Column(float,doc = '市净率')
    ps = Column(float,doc = '市销率')
    ps_ttm = Column(float,doc = '市销率TTM')
    dv_ratio= Column(float,doc = '股息率')
    dv_ttm= Column(float,doc = '股息率TTM')
    total_mv = Column(float,doc = '总市值')

class StockFinancial(Base):
    """财务摘要"""
    __tablename__ = 'stock_financial'
    id = Column(BigInteger,Sequence('stock_financial_id_seq'),primary_key=True)
    ticker = Column(String(8),ForeignKey('stock.ticker'),doc = '股票代码')
    end_dt = Column(DateTime,doc = '截止日期')
    pre_net_assets = Column(float,doc = '每股净资产')
    pre_cashflow = Column(float,doc = '每股现金流')
    fixed_assets = Column(float,doc = '固定资产合计')
    flow_assets = Column(float,doc = '流动资产合计')
    sum_assets = Column(float,doc = '资产合计')
    longterm_liabilities = Column(float,doc = '长期负债合计')
    main_income= Column(float,doc = '主营业务收入')
    financial_expenses = Column(float,doc = '财务费用')
    net_profit = Column(float,doc = '净利润')


