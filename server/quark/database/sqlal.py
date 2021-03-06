# -*- coding:utf-8 -*-
"""系统运行数据库连接工具
使用sqlalchemy的数据库相关的代码，仅包括数据库连接管理, ORM模型定义在model目录.

当前支持Oracle与Mysql两种方式
"""
import datetime
import os

from sqlalchemy import (create_engine, func)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.pool import NullPool

from ..base.settings import Config

############################
# Database Special Settings#
############################
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
# Oracle迁移 Oracle/Mysql 数据库切换 语法差异
if Config.DB_CONFIG.get('DB_TYPE', '') == 'oracle':
    func_to_char = func.to_char
    func_to_date = func.to_date
else:
    func_to_char = func.date_format
    func_to_date = func.str_to_date

#####################
# ORM 对象基本申明类#
#####################
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


setattr(Base, 'to_dict', to_dict)


class Database(object):
    """ Database Manager Object"""

    def __init__(self, configure, name, echo=False, pool_size=10, pool_recycle=1800,
                 poolclass=None, thread=True):
        """DB Connection Init

        :param dict configure: dblink config dict, exp:{DBNAME:DBURL}
        :param str name:dbname in configure need be connect
        :param bool echo: echo sql detail
        :param int pool_size: connection pool size
        :param int pool_recycle: recycle connection time
        :param poolclass: SQLAlchemy Pool Class, Default None
        :param bool thread: if Shared Connection between theads.Using sqlalchemy scoped_session
        """
        self.configure = configure
        extend_args = {'pool_size': pool_size}
        if poolclass == NullPool:
            extend_args = {"poolclass": NullPool}
        self.engine = create_engine(self.get_url(name), echo=echo, pool_recycle=pool_recycle, pool_pre_ping=True,
                                    encoding="utf-8", convert_unicode=False, **extend_args)
        if thread:
            self.Session = scoped_session(sessionmaker(bind=self.engine, autocommit=False,
                                                       autoflush=False))
        else:
            self.Session = sessionmaker(bind=self.engine, autocommit=False, autoflush=False)

    def __getattr__(self, name):
        if name == "session":
            return self.Session()

    def get_url(self, config_name):
        """Get DB Url From Config Dict By Name"""
        self.url = self.configure.get(config_name)
        return self.url


_SYSTEM_DB = Database({'sysdb_url': Config.SQLALCHEMY_DATABASE_URL}, 'sysdb_url')


def simple_session(url=Config.SQLALCHEMY_DATABASE_URL, process=False):
    if process:
        return Database({'url': url}, 'url', pool_size=1, thread=False).session
    else:
        return _SYSTEM_DB.session


def scope_session(*args, **kwargs):
    return _SYSTEM_DB.Session


def get_session(subject):
    """Get Session by inspect In Connection"""
    stat = inspect(subject)
    return stat.session


if __name__ == '__main__':
    session = simple_session()
    print(dir(session.bind))
    print(session.bind.url)
