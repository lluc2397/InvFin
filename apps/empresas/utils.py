from apps.translate.google_trans_new import google_translator
import yfinance as yf

class UpdateCompany():
    def __init__(self, company) -> None:
        self.model_company = company
        self.yho_company = yf.Ticker(company.ticker)


    def add_logo(self):        
        try:
            self.model_company.image = self.yho_company.info['logo_url']
            self.model_company.has_logo = True
            self.model_company.save()
        except Exception as e:
            print(e)


    def add_description(self):
        try:
            self.model_company.description = google_translator().translate(self.model_company.description,lang_src='en', lang_tgt='es')
            self.model_company.description_translated = True
            self.model_company.save()
        except Exception as e:
            print(e)


    def general_update(self):        
        if self.model_company.has_logo is False:
            self.add_logo()
        if self.model_company.description_translated is False:
            self.add_description()