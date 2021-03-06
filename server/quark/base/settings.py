"""
系统参数配置模块
"""
import logging
import os
import sys
import traceback
from string import Template

class SystemConfig(object):
    """系统运行配置项"""
    # 主目录
    BASEPATH = os.path.join(sys.path[0],'../')

    # Flask前后台交互安全码
    SECRET_KEY = os.environ.get('SECRET_KEY','')

    # 后台服务SwaggerUI文档
    SYS_SWAGGER_TITLE = 'Service API'
    SYS_SWAGGER_API = os.environ.get('SYS_SWAGGER_API','/APIDOC')

    # 前端项目目录
    WEB_HOME= os.path.join(BASEPATH,'web')

    # 后台静态资源目录
    SERVER_STATIC_PATH = os.path.join(os.path.expanduser('~'),'server_static')
    if not os.path.isdir(SERVER_STATIC_PATH):
        os.makedirs(SERVER_STATIC_PATH)
    
     # 前端静态资源目录
    WEB_STATIC_PATH = os.path.join(WEB_HOME, 'static')

    # 前端请求地址 纯请求地址,例如 download链接为 ip/static/交易数据.xls
    WEB_STATIC_URL = '/static'

    """后端运行服务日志配置"""
    LOG_PATH = os.path.join(os.path.expanduser('~'),'server_logs')
    if not os.path.isdir(LOG_PATH):
        os.makedirs(LOG_PATH)
    DEBUG_LOG = os.path.join(LOG_PATH, 'debug.log')
    ERROR_LOG = os.path.join(LOG_PATH, 'error.log')
    FORMATTER_LOG = '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'

    """数据库配置信息"""
    # 系统数据库
    DB_ALL_TYPE = ['postgis']
    DB_TYPE = os.environ.get('DB_TYPE', 'postgis').lower()
    DB_CONFIG = {
        'DB_USER': os.environ.get('FTTL_DB_USER', 'quark'),  # 数据库用户
        'DB_PASSWD': os.environ.get('FTTL_DB_PASSWD', 'qwe123'),  # 数据库密码
        'DB_HOST': os.environ.get('FTTL_DB_HOST', '0.0.0.0'),  # 数据库地址
        'DB_PORT': os.environ.get('FTTL_DB_PORT', '5432'),  # 数据库端口
        'DB_INSTANCE': os.environ.get('FTTL_DB_INSTANCE', 'quark_db'),  # 数据库实例名
    }
    SQLALCHEMY_DATABASE_URL = Template(
        "postgresql://$DB_USER:$DB_PASSWD@$DB_HOST:$DB_PORT/$DB_INSTANCE").safe_substitute(
        **DB_CONFIG)
    

class ProdConfig(SystemConfig):
    """投产模式"""
    os.environ['MODE'] = "PRODUCTION"

class DevConfig(SystemConfig):
    """开发者模式"""
    os.environ['MODE'] = "DEVELOP"
    logging.warning("Current Using Dev Config, Don't Use It In A Production Deployment.")

    HOST = '0.0.0.0'
    PORT = 4000

    # 开启性能检测功能
    PERFORMANCE_PROFILE = False

Config = DevConfig()
