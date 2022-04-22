from ..models import Company

import yfinance as yf


def simple_stock_analysis(empresa):
    
    empresa_info = yf.Ticker(empresa.ticker)
    inf = empresa_info.info
    
    recommendationKey = None
    targetMeanPrice = None
    currentPrice = None

    result_buy = {
                'num': 1,
                'expl': 'Comprar',
            }
    
    result_sell = {
                'num': 2,
                'expl': 'Vender',
            }

    result_hold = {
                'num': 3,
                'expl': 'Mantener',
            }

    if 'recommendationKey' in inf:
        recommendationKey = inf['recommendationKey']
        if recommendationKey == 'buy':
            result = result_buy
        elif recommendationKey == 'hold':
            result = result_hold
        elif recommendationKey == 'sell':
            result = result_sell

    else:
        if 'targetMeanPrice' in inf:
            targetMeanPrice = inf['targetMeanPrice']
            if targetMeanPrice < currentPrice:
                result = result_sell
            elif targetMeanPrice > currentPrice:
                result = result_buy
            elif targetMeanPrice == currentPrice:
                result = result_hold

        else:
            if 'currentPrice' in inf:
                currentPrice = inf['currentPrice']
                try:
                    per = empresa.per_share_values.latest().eps / currentPrice
                    if per < 10:
                        result = result_buy
                    elif per > 20:
                        result = result_sell
                    elif per > 10 and per < 20:
                        result = result_hold
                except:
                    result = {
                    'num': 4,
                    'expl': 'Mantener',
                }

    result['company'] = empresa
    return result
