LONG_TERM, MEDIUM_TERM, SHORT_TERM = "long-term", "medium-term", "short-term"

HORIZON = (
    (LONG_TERM, 'Long Term'), 
    (MEDIUM_TERM, 'Medium Term'), 
    (SHORT_TERM, 'Short Term')
)


ACTIVE, INTER, PASIVE, GAMBLER = "active", "intermediate", "pasive", "gambler"

INVESTOR_TYPE = (
    (ACTIVE, 'Activo'), 
    (INTER, 'Intermedio'), 
    (PASIVE, 'Pasivo'), 
    (GAMBLER, 'Especulador')
)

EXPERT, PRO, INTER, BASIC, NULL = "expert", "pro", "intermediate", "basic", "null"

KNOWLEDGE = (
    (EXPERT, 'Experto'), 
    (PRO, 'Profesional'), 
    (INTER, 'Intermedio'), 
    (BASIC, 'Básico'), 
    (NULL, 'Nulo')
)


CURRENCY = (
    (1, 'USD'), 
    (2, 'MXN'), 
    (3, 'EUR'), 
    (4, 'ARS'), 
    (5, 'COP'),
    (6, 'PEN')
)


FINISED, ABANDONED, STARTED, NOT_PAYED = "finished", "abandoned", "started", "not-payed" 

SERVICE_STATUS = (
    (FINISED, 'Finished'), 
    (ABANDONED, 'Abandoned'), 
    (STARTED, 'Started'),
    (NOT_PAYED, 'Not payed')
)


OBJECTIFS = (
    (1, 'Generar ingresos pasivos'), 
    (2, 'Generar un patrimonio'), 
    (3, 'Ahorrar'), 
    (4, 'Ganar dinero rápido')
)


VOLATILIDAD = (
    (1, 'Riesgo'), 
    (2, 'Oportunidad'), 
    (3, 'No le presto atención')
)


NUMBER_STOCKS = (
    (0, 'Ninguna'), 
    (1, 'Una'), 
    (2, 'Dos'), 
    (3, 'Tres'), 
    (4, 'Cuatro'),
    (5, 'Cinco'), 
    (6, 'Entre 5 y 10'), 
    (7, 'Entre 10 y 20'), 
    (8, 'Más de 20')
)


RESULTS = (
    (1, 'Comprar'), 
    (2, 'Vender'), 
    (3, 'Mantener'), 
    (4, 'Error')
)


MINUTES, HOURS, DAYS, WEEKS, MONTHS, YEARS = "minutes", "hours", "days", "weeks", "months", "years"

PERIODS = (
    (MINUTES, 'Minutos'),
    (HOURS, 'Horas'),
    (DAYS, 'Días'),
    (WEEKS, 'Semanas'),
    (MONTHS, 'Meses'),
    (YEARS, 'Años')
)


ROBO_STEPS = (
    ('stocks-portfolio', 'stocks-portfolio'),
    ('composition', 'composition'),
    ('risk-aversion', 'risk-aversion'),
    ('weights', 'weights'),
    ('experience', 'experience'),
    ('financial', 'financial'),
    ('analysis', 'analysis')
)


ROBO_RESULTS = (
    ('company-match', 'company-match'),
    ('investor-profile', 'investor-profile'),
    ('optimize-my-portfolio', 'optimize-my-portfolio')
)


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


RISK_PROFILE = (    
    ('very-agressive', 'Perfil muy agresivo'), 
    ('agressive', 'Perfil agresivo'),
    ('regular', 'Perfil regular'),
    ('conservative', 'Perfil conservador'), 
    ('very-conservative', 'Perfil muy conservador')    
)
