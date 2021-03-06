"""初始化数据库"""
import logging

from quark.database.sqlal import Base, simple_session
from..model.stock import *

def dbinit():
    """初始化数据库"""
    session = simple_session()
    print(session.bind)
    for tbname, tbinfo in Base.metadata.tables.items():
        print(tbname)
    # 重置表结构
    logging.info("Rebuild DB Tables...")
    Base.metadata.drop_all(session.bind, checkfirst=True)
    Base.metadata.create_all(session.bind, checkfirst=True)


    