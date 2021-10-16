import akshare as ak

def get_stock_indicator(ticker):
    if len(ticker) > 6:
        ticker_code = ticker[:6]
    else:
        ticker_code = ticker
    df = ak.stock_a_lg_indicator(stock=ticker_code)
    df['ticker'] = ticker
    return df

def get_stock_financial(ticker):
    if len(ticker) > 6:
        ticker_code = ticker[:6]
    else:
        ticker_code = ticker
    df = ak.stock_financial_abstract(stock=ticker_code)
    index = {
        '截止日期' : 'end_dt',
        '每股净资产-摊薄/期末股数' : 'pre_net_assets',
        '每股现金流' : 'pre_cashflow',
        '固定资产合计' : ""
    }

    
