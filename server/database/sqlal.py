"""系统运行数据库连接工具"""
import datetime
import os

from sqlalchemy import(create_engine,func)
from sqlalchemy.ext.declarative import declarative_base

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

Base = declarative_base()

def to_dict(self, convert=True):
    """Extend Ablity To Dict Orm Object Data"""
    attrlist = [a for a in list(self.__dict__.keys()) if not a.startswith('_')]
    data = {}
    for name in attrlist:
        attr_data = getattr(self, name, None)
        if not convert:
            data[name] = attr_data
            continue

        if isinstance(attr_data, datetime.datetime):
            attr_data = attr_data.strftime('%Y-%m-%dT%H:%M:%S')  # ISO8601标准
        elif isinstance(attr_data, datetime.date):
            attr_data = attr_data.strftime('%Y-%m-%d')
        elif isinstance(attr_data, datetime.time):
            attr_data = attr_data.strftime('%H:%M:%S')
        data[name] = attr_data

    return data
setattr(Base,'to_dict',to_dict)


