from ..models import Company

import yfinance as yf


def STOCK_ANALYSIS_HELP(empresa):
    
    empresa_info = yf.Ticker(empresa.ticker)
    inf = empresa_info.info
    recommendationKey = inf['recommendationKey']
    targetMeanPrice = inf['targetMeanPrice']
    currentPrice = inf['currentPrice']
    result1 = {
                'num': 1,
                'expl': 'Comprar',
            }
    
    result2 = {
                'num': 2,
                'expl': 'Mantener',
            }

    result3 = {
                'num': 3,
                'expl': 'Vender',
            }

    if recommendationKey != 'none':
        if recommendationKey == 'buy':
            result = result1
        elif recommendationKey == 'hold':
            result = result2
        elif recommendationKey == 'sell':
            result = result3
    else:
        if targetMeanPrice != None:
            if targetMeanPrice < currentPrice:
                result = result3
            elif targetMeanPrice > currentPrice:
                result = result1
            elif targetMeanPrice == currentPrice:
                result = result2
        else:
            try:
                per = (PER_SHARE_VALUE.objects.filter(company = empresa).first().eps) / currentPrice
                if per < 10:
                    result = result1
                elif per > 20:
                    result = result3
                elif per > 10 and per < 20:
                    result = result2
            except:
                result = {
                'num': 4,
                'expl': 'Mantener',
            }

    return result