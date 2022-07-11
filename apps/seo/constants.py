ADS = 'ads'
EMAILS = 'email'
INVFIN = 'invfin'
SOCIAL_MEDIA_POSTS = 'social-media-posts'

MEDIUMS = (
    (ADS, 'Ads'),
    (EMAILS, 'Email'),
    (INVFIN, 'Web'),
    (SOCIAL_MEDIA_POSTS, 'Social media posts'),
)

SIDE = 'side'
TOP = 'top'
MIDDLE = 'middle'
BOTTOM = 'bottom'
IN_BETWEEN = 'in_between'

WEP_PROMOTION_PLACE = (
    (SIDE, 'Side'),
    (TOP, 'Top'),
    (MIDDLE, 'Middle'),
    (BOTTOM, 'Bottom'),
    (IN_BETWEEN, 'In between'),
)

POP_UP = 'pop_up'
BANNER = 'banner'
LISTA = 'lista'
SOLO = 'solo'

WEP_PROMOTION_TYPE = (
    (POP_UP , 'Pop up'),
    (BANNER , 'Big Banner'),
    (LISTA , 'List'),
    (SOLO , 'Solo'),
)

WEB_INICIO = 'web-inicio'
SCREENER_INICIO = 'screener-inicio'
CARTERA_INICIO = 'cartera-inicio'
PUBLIC_PROFILE = 'public-profile'
PRIVATE_PROFILE = 'private-profile'
QUESIOTN_INICIO = 'question-inicio'
TERM_INICIO = 'term-inicio'
BLOG_INICIO = 'blog-inicio'
CARTERA_FINANCILAS = 'cartera-financials'
CARTERA_BALANCE = 'cartera-balance'
SCREENER_MARKET = 'screener-market'
SCREENER_COMPANY = 'screener-company'
BLOG_DETAILS = 'blog-details'
TERM_DETAILS = 'term-details'
QUESTION_DETAILS = 'question-details'

WEP_PROMOTION_LOCATION = (
    (WEB_INICIO, 'Web Inicio'),
    (SCREENER_INICIO, 'Screener Inicio'),
    (SCREENER_MARKET, 'Screener Market'),
    (SCREENER_COMPANY, 'Screener Company'),
    (CARTERA_INICIO, 'Cartera Inicio'),
    (CARTERA_FINANCILAS, 'Cartera Financials'),
    (CARTERA_BALANCE, 'Cartera Balance'),
    (PRIVATE_PROFILE, 'Private Profile'),
    (PUBLIC_PROFILE, 'Public Profile'),
    (QUESIOTN_INICIO, 'Question Inicio'),
    (QUESTION_DETAILS, 'Question Details'),
    (TERM_INICIO, 'Term Inicio'),
    (TERM_DETAILS, 'Term Details'),
    (BLOG_INICIO, 'Blog Inicio'),
    (BLOG_DETAILS, 'Blog Details'),
)
