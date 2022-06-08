from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
from datetime import datetime

from django.utils import timezone

from apps.empresas.models import Company

from .models import (
    Superinvestor,
    SuperinvestorActivity,
    Period,
    SuperinvestorHistory
)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate'
}


SITE = 'https://www.dataroma.com'


def get_investors_accronym():
    url = requests.get(f'{SITE}/m/managers.php', headers=HEADERS).content
    soup = bs(url, 'html.parser')

    main_table = soup.find('table', id='grid')

    all_td = main_table.find_all('td', class_='man')

    all_investors = []

    for t in all_td[1:]:
      superinvestor, _ = Superinvestor.objects.get_or_create(
        name=t.text,
        fund_name='',
        info_accronym=t.find('a', href=True)['href'].split('=')[1],
        last_update=timezone.now()
      )
      all_investors.append(superinvestor)
        
    return all_investors


def get_historial(superinvestor_activity):
  actual_company = superinvestor_activity.actual_company
  if type(actual_company) == str:
    ticker = actual_company.split('-')[0].strip()
    company_saved = False
  else:
    ticker = actual_company.ticker
    company_saved = True
  url = f'{SITE}/m/hist/hist.php?f={superinvestor_activity.superinvestor_related.info_accronym}&s={ticker}'
  response = requests.get(url, headers=HEADERS).content
  print(url)
  table = pd.read_html(response)[0]
  table['Activity'] = table['Activity'].fillna('Hold')
  table = table.fillna(0)
  for index, content in table.iterrows():
    period = content['Period']
    period, created = Period.objects.get_or_create(
      year=datetime.strptime(period[:4], '%Y'),
      period=period[-1:]
    )
    if company_saved == True:
      super_activity = SuperinvestorHistory.objects.filter(
        period_related=period, 
        company=actual_company,
        superinvestor_related=superinvestor_activity.superinvestor_related
      )
    else:
      super_activity = SuperinvestorHistory.objects.filter(
        period_related=period, 
        company_name=actual_company,
        superinvestor_related=superinvestor_activity.superinvestor_related
      )
    if super_activity.exists():
      continue
    reported_price = content['Reported Price']
    if type(reported_price) == int:
      reported_price = reported_price
    elif reported_price.startswith('$'):
      try:
        reported_price = float(reported_price[1:])
      except ValueError:
        reported_price = float(reported_price[1:].replace(',',''))
    history = dict(
      superinvestor_related=superinvestor_activity.superinvestor_related,
      period_related=period,
      portfolio_change=content['% Change to Portfolio'],
      movement=content['Activity'],
      shares=content['Shares'],
      reported_price=reported_price,
      portfolio_weight=content['% of Portfolio'],
    )
    if company_saved == True:
      history['company'] = actual_company
    else:
      history['company_name'] = actual_company


    superinvestor_history, created = SuperinvestorHistory.objects.get_or_create(**history)


def get_activity(superinvestor):
    main_url = f'{SITE}/m/m_activity.php?m={superinvestor.info_accronym}&typ=a'
    url = requests.get(main_url, headers=HEADERS).content
    soup = bs(url, 'html.parser')
    try:
      pages = [div.text for div in soup.find('div', id="pages").find_all('a')][1:-1]
      skip_followings = False
    except AttributeError:
      pages = range(0, 1)
      skip_followings = True
    
    for page in pages:
      if skip_followings is True and page > 0:
        continue
      investor_url = f'{main_url}&L={page}'
      url = requests.get(investor_url, headers=HEADERS).content
      soup = bs(url, 'html.parser')

      for td in soup.find_all('td')[5:]:

        info = td.text
        attrs = td.attrs
        clase = attrs.get('class')

        if td.find('b') is not None:
          quarter = td.text.split(' ')[0][1:]
          year = td.text.split(' ')[1][-4:]
          period, _ = Period.objects.get_or_create(
            year=datetime.strptime(year, '%Y'),
            period=quarter
          )
          continue # Quarter and year
        
        if clase:
          if clase[0] == 'stock':
            ticker = info.split('-')[0].strip() # Ticker
            name = info.split('-')[1].strip()
            need_verify_company = False
            not_registered_company = False
            company = None
            try:
              company = Company.objects.get(ticker=ticker)
            except Company.MultipleObjectsReturned:
              if Company.objects.filter(ticker=ticker, name=name).exists():
                if Company.objects.filter(ticker=ticker, name=name).count() == 1:
                  company = Company.objects.get(ticker=ticker, name=name)
                  need_verify_company = True
            except Company.DoesNotExist:
              if Company.objects.filter(name__icontains=name).exists():
                if Company.objects.filter(name__icontains=name).count() == 1:
                  company = Company.objects.filter(name__icontains=name)[0]
                  need_verify_company = True
                else:
                  not_registered_company = True
              else:
                not_registered_company = True
            superinvestor_activity = SuperinvestorActivity.objects.create(
              superinvestor_related=superinvestor,
              period_related=period,
              company=company,            
              company_name=info,
              not_registered_company=not_registered_company,
              need_verify_company=need_verify_company
            )
            continue

          elif clase[0] == 'buy' or clase[0] == 'sell':
            movement = None
            is_new = False
            if 'Add' in info or 'Buy' in info:
              if 'Buy' in info:
                is_new = True
              movement = 1
            elif 'Reduce' in info or 'Sell' in info:
              movement = 2
            if movement is not None:
              percentage_share_change=info.split(' ')[1][:-1]
              if percentage_share_change == '':
                percentage_share_change = 0
              superinvestor_activity.percentage_share_change=percentage_share_change
              superinvestor_activity.is_new=is_new
              superinvestor_activity.movement=movement
              superinvestor_activity.save(update_fields=[
                'percentage_share_change',
                'is_new',
                'movement',
                ])
              continue # activity
            else:
              superinvestor_activity.share_change=info.replace(',', '')
              superinvestor_activity.save(update_fields=['share_change'])
              continue # share change
        else:
          superinvestor_activity.portfolio_change=info
          superinvestor_activity.save(update_fields=['portfolio_change'])
          continue
