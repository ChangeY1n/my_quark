import datetime

from sqlalchemy import  BigInteger, Float, Text, Column, DateTime, ForeignKey, Integer, Sequence, String
from sqlalchemy.sql.sqltypes import Boolean

from quark.database.sqlal import Base,simple_session


class StockINFO(Base):
    """股票信息表"""
    __tablename__ = "stock"
    id = Column(BigInteger,Sequence('stock_id_seq'), primary_key=True)
    ticker = Column(String(64), doc='股票代码',unique = True)
    instrument = Column(String(512), doc='所属行业')
    name = Column(String(512), doc='公司名称')
    IPO_date = Column(DateTime,doc='上市时间')
    create_date = Column(DateTime,doc='创建时间')

class DailyPrice(Base):
    """每日价格"""
    __tablename__ = 'daily_price'
    id = Column(BigInteger,Sequence('daily_price_id_seq'),primary_key=True)
    ticker = Column(String(64),ForeignKey('stock.ticker'),doc = '股票代码')
    date = Column(DateTime,doc = '日期')
    open_price = Column(Float,doc = '开盘价')
    high_price = Column(Float,doc = '最高价')
    low_price = Column(Float,doc = '最低价')
    close_price = Column(Float,doc = '收盘价')
    pre_close = Column(Float,doc = '昨日收盘点')
    change = Column(Float,doc = '涨跌点')
    pct_chg = Column(Float,doc = '涨跌幅%')
    vol = Column(Float,doc = '成交量')
    amount = Column(Float,doc = '成交额(千元)')

class StockIndicator(Base):
    """个股指标"""
    __tablename__ = 'stock_indicator'
    id = Column(BigInteger,Sequence('stock_indicator_id_seq'),primary_key=True)
    ticker = Column(String(64),ForeignKey('stock.ticker'),doc = '股票代码')
    trade_date = Column(DateTime,doc = '交易日')
    pe = Column(Float,doc = '市盈率')
    pt_ttm = Column(Float,doc = '市盈率TTM')
    pb = Column(Float,doc = '市净率')
    ps = Column(Float,doc = '市销率')
    ps_ttm = Column(Float,doc = '市销率TTM')
    dv_ratio= Column(Float,doc = '股息率')
    dv_ttm= Column(Float,doc = '股息率TTM')
    total_mv = Column(Float,doc = '总市值')

class StockFinancial(Base):
    """财务摘要"""
    __tablename__ = 'stock_financial'
    id = Column(BigInteger,Sequence('stock_financial_id_seq'),primary_key=True)
    ticker = Column(String(64),ForeignKey('stock.ticker'),doc = '股票代码')
    end_dt = Column(DateTime,doc = '截止日期')
    pre_net_assets = Column(Float,doc = '每股净资产')
    pre_cashflow = Column(Float,doc = '每股现金流')
    fixed_assets = Column(Float,doc = '固定资产合计')
    flow_assets = Column(Float,doc = '流动资产合计')
    sum_assets = Column(Float,doc = '资产合计')
    longterm_liabilities = Column(Float,doc = '长期负债合计')
    main_income= Column(Float,doc = '主营业务收入')
    financial_expenses = Column(Float,doc = '财务费用')
    net_profit = Column(Float,doc = '净利润')
