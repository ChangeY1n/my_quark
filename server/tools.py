"""系统工具箱"""
import logging
import os
import traceback
from optparse import OptionGroup, OptionParser

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] PID:%(process)d-%(name)s: [%(filename)s-%(funcName)s-%(lineno)d] %(levelname)-7s: %(message)s"
)
def init_db():
    """重置数据库"""
    from fttl.scripte.dbinit import dbinit
    dbinit()
