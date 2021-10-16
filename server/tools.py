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
    from quark.scripts.dbinit import dbinit
    print("xxxxxxxxxxxxx")
    dbinit()
def init_stock():
    """创建基本股票信息"""
    from quark.scripts.init_stockinfo import init_stockinfo
    init_stockinfo()

def init_price():
    """重置个股每日数据"""
    from quark.scripts.init_stockinfo import init_price
    init_price()
def init_indicator():
    """个股基本面数据"""
    from quark.scripts.init_stockinfo import init_indicator
    init_indicator()

def tools_dispatcher(options, args):
    """工作调度器
    解析命令对应的函数功能
    """
    opts = [p for p in dir(options) if not p.startswith('_')]

    _method_map = {
        'init_db' : init_db,
        'init_stock' : init_stock,
        'init_price' : init_price,
        'init_indicator' : init_indicator
    }

    for opt in opts:
        if getattr(options, opt) and opt in _method_map:
            opargs = getattr(options, opt)
            opargs = opargs if isinstance(opargs, (list, tuple)) else (opargs,)

            funcs = _method_map[opt]
            funcs = funcs if isinstance(funcs, (list, tuple)) else [funcs, ]

            for func in funcs:
                if opargs == (True,):
                    func()
                else:
                    func(*opargs)
            break

def system_command():
    """系统命令功能，将需要指定的命令在此处添加"""
    opt_parser = OptionParser()
    sys_tools_options = OptionGroup(opt_parser, "System Server Management Tools Options", "系统服务管理工具")
    sys_tools_options.add_option("--reboot_server", action="store_true", dest="reboot_server", help="重启后台所有服务")
    sys_tools_options.add_option("--start_web", action="store_true", dest="start_web", help="开启后台Web服务器功能")
    sys_tools_options.add_option("--stop_web", action="store_true", dest="stop_web", help="关闭后台Web服务器功能")
    sys_tools_options.add_option("--run_app", action="store", dest="run_app", help="""单例后台服务器, 将输出日志信息. 需指定对应IP, 若本地运行可以输入0.0.0.0""")
    opt_parser.add_option_group(sys_tools_options)

    table_tools_options = OptionGroup(opt_parser, "System Persistence layer Tools Options", "系统持久化层管理工具参数.")
    table_tools_options.add_option("--init_db", action="store_true", dest="init_db", help="重置应用数据库, 请谨慎操作！")
    table_tools_options.add_option("--init_stock", action="store_true", dest="init_stock", help="重置股票基本数据，包括公司名，股票代码等信息")
    table_tools_options.add_option("--init_price", action="store_true", dest="init_price", help="重置个股每日数据")
    table_tools_options.add_option("--init_indicator", action="store_true", dest="init_indicator", help="重置个股基本面数据")

    opt_parser.add_option_group(table_tools_options)

    tools_dispatcher(*opt_parser.parse_args())


if __name__ == '__main__':
    system_command()