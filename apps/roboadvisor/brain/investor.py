from .models import (
    FAVORITE_STOCK,
    LIST_OF_FAVORITE_STOCKS,
    ROBO_OPTIONS,
    INVESTOR_PROFILE,
    CURRENT_INVESTORS_TYPE,
    TEST_TAKEN,
    QUESTIONS_FINANCIAL_SITUATION,
    QUESTIONS_INVESTOR_STORY,
    QUESTIONS_STUDY_TIME,
    QUESTIONS_RISK_AVERSION,
    QUESTIONS_HORIZON,
    QUESTIONS_ASSETS_LIKES,
    QUESTIONS_COMPANY_HELP,
    DISLIKES_TEST,
    LIKES_TEST,
    QUESTIONS_PORTFOLIO,
    QUESTIONS_PORTFOLIO_STOCK_COMPOSITIONS,
    QUESTIONS_PORTFOLIO_ETF_COMPOSITIONS
)

from companies_information.models import COMPANY, PER_SHARE_VALUE

import yfinance as yf

PROFILE_VERY_AGRESIVE = 'Las personas con actitudes de riesgo muy agresivas buscan maximizar sus ganancias a largo plazo y están dispuestas a aceptar un riesgo sustancial para lograrlo.\
A cambio de ese rendimiento esperado más alto, esta actitud de riesgo asume la mayor parte del riesgo de la cartera con potencialmente mucha más volatilidad y un mayor potencial de pérdidas de inversión,\
así como una gama más amplia de resultados potenciales en el futuro, buenos o malos. Las carteras muy agresivas suelen invertir mucho más en acciones que en bonos o efectivo en relación con los inversores con actitudes menos riesgosas en un esfuerzo por tener el mayor potencial de rendimiento posible.'

PROFILE_AGRESIVE = 'Las personas con actitudes agresivas frente al riesgo se sienten cómodas asumiendo riesgos y lidiando con la volatilidad del mercado a corto plazo para tener la oportunidad de alcanzar niveles más altos de riqueza en el futuro y cumplir con los objetivos de inversión a largo plazo.\
Los inversores con actitudes agresivas normalmente utilizarán más acciones en su cartera dado su mejor potencial de rendimiento que los bonos y el efectivo, pero los inversores deben ser conscientes de que el mayor potencial de rendimiento conlleva una mayor volatilidad y un mayor potencial de pérdidas.'

PROFILE_REGULAR = 'Las personas con actitudes de riesgo moderado asumen cierto riesgo de inversión, pero también desconfían de las desventajas.\
Los inversores con estos puntos de vista sobre el riesgo se sienten más cómodos con la volatilidad de la inversión hoy en día por el potencial de mejores resultados en el futuro,\
pero no llegarán a los mismos niveles de toma de riesgo de renta variable que los inversores agresivos o muy agresivos. En relación con los inversores conservadores, puede haber un riesgo reducido de no poder acumular\
suficiente riqueza para cumplir los objetivos de jubilación a largo plazo o incluso potencialmente no poder seguir el ritmo de la inflación, pero existe un mayor riesgo de volatilidad de la cartera y de corto plazo. pérdidas de plazo.'

PROFILE_CONSERVATIVE = 'Las personas con actitudes conservadoras frente al riesgo se sienten más cómodas con la toma de riesgos en comparación \
con los inversores muy conservadores, pero aún así prefieren la cautela cuando se trata de invertir. \
Los inversores con actitudes conservadoras frente al riesgo normalmente utilizarán más bonos o efectivo en su cartera que los inversores \
con actitudes más riesgosas. Si bien el riesgo de perder dinero debido a un desempeño deficiente del mercado podría reducirse con un enfoque conservador,\
este tipo de inversión conlleva otros riesgos, como no poder generar suficiente riqueza para cumplir con los objetivos financieros o incluso no poder seguir\
el ritmo. con inflación para mantener el poder adquisitivo de sus inversiones. Si bien tienen el beneficio de experimentar potencialmente menos altibajos en el mercado,\
los inversores con actitudes conservadoras de riesgo probablemente necesiten ahorrar más para alcanzar los mismos niveles de riqueza y cumplir los mismos objetivos financieros que aquellos que se sienten cómodos asumiendo más riesgos.'

PROFILE_VERY_CONSERVATIVE = 'Las personas con actitudes de riesgo muy conservadoras buscan inversiones estables con un riesgo mínimo para el capital de sus inversiones.\
Los inversores con actitudes de riesgo muy conservadoras normalmente utilizarán significativamente más bonos o efectivo en su cartera que los inversores con actitudes más riesgosas.\
Si bien el riesgo de perder dinero debido a un desempeño deficiente del mercado podría reducirse con un enfoque muy conservador, este tipo de inversión conlleva otros riesgos,\
como no poder generar suficiente riqueza para cumplir con los objetivos financieros o incluso no poder mantener ritmo con la inflación para mantener el poder adquisitivo de sus inversiones.\
Si bien tienen el beneficio de experimentar potencialmente menos altibajos en el mercado, los inversores con actitudes de riesgo muy conservadoras probablemente necesiten ahorrar más para alcanzar los mismos niveles de riqueza y cumplir los mismos objetivos financieros que aquellos que se sienten cómodos asumiendo más riesgos.'

def STOCK_ANALYSIS_HELP(ticker:str, empresa):
    
    empresa_info = yf.Ticker(ticker)
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


def INVESTOR_SCORE(investor_story,
    view_on_volatility,
    onefive,
    zerofive,
    investor):

    INVESTOR_TYPE = ((1, 'Activo'), (2, 'Intermedio'), (3, 'Pasivo'), (4, 'Especulador'))

    INVESTOR_RISK_PROFILE = ((1, 'PROFILE VERY AGRESIVE'), (2, 'PROFILE AGRESIVE'), (3, 'PROFILE CONSERVATIVE'), (4, 'PROFILE VERY CONSERVATIVE'), (5, 'PROFILE REGULAR'))

    if int(view_on_volatility) == 1:
        number = 2
        investor_is = 3
        if investor_story.objectif == 2 or investor_story.objectif == 3:
            result = "Muy conservador"
            risk_aversion = 4
            profile_explanation = PROFILE_VERY_CONSERVATIVE

        else:
            result = "Conservador"
            risk_aversion =3
            profile_explanation = PROFILE_CONSERVATIVE
       
    else:
        if int(zerofive) > 0:
            investor_is = 4
            number = 1
            result = "Muy agresivo"
            risk_aversion =1
            profile_explanation = PROFILE_VERY_AGRESIVE
        else:
            if int(onefive) >= 50:
                investor_is = 1
                number = 1
                result = "Agresivo"
                risk_aversion =2
                profile_explanation = PROFILE_AGRESIVE
            else:
                investor_is = 2
                number = 3
                result = "Moderado"
                risk_aversion =5
                profile_explanation = PROFILE_REGULAR            

    

    CURRENT_INVESTORS_TYPE.objects.create(
        investor_related = investor,
        investors_type = investor_is,
        risk_aversion = risk_aversion,
    )


    type_profile_investor = {
        'explanation': profile_explanation,
        'number' : number,
        'result': result
    }

    return type_profile_investor


def PORTFOLIO_OPTIMIZATION_FUNCTION(user, test):
    portfolio_to_upgrade = QUESTIONS_PORTFOLIO.objects.get(investor_related = user,test_related = test)
    empresas = QUESTIONS_PORTFOLIO_STOCK_COMPOSITIONS.objects.filter(investor_related = user,portfolio_related = portfolio_to_upgrade)
    etfs = QUESTIONS_PORTFOLIO_ETF_COMPOSITIONS.objects.filter(investor_related = user,portfolio_related = portfolio_to_upgrade)

    empresas = [empresa for empresa in empresas.company_related]
    # empresa_info = yf.Ticker(ticker)

