import os
from pathlib import Path
import importlib
import configparser


class AutomateTests:
    current_path = Path(__file__).parent.resolve()
    config_parser = configparser.ConfigParser()

    def parse_pytest_ini(self, file_path):
        self.config_parser.read(file_path)
        sections = self.config_parser.sections()
        if 'pytest' in sections:
            if self.config_parser['pytest']['addopts']:
                possible_config = self.config_parser['pytest']['addopts'].strip()
                if possible_config.startswith('--ds='):
                    possible_config = possible_config.replace('--ds=', '')
                if possible_config.endswith(' --reuse-db'):
                    possible_config = possible_config.replace(' --reuse-db', '')
                return possible_config
            else:
                return self.config_parser['pytest']['python_files']
    
    def parse_setup_cfg(self, file_path):
        self.config_parser.read(file_path)
        sections = self.config_parser.sections()
        if 'mypy.plugins.django-stubs' in sections:
            if 'django_settings_module' in self.config_parser['mypy.plugins.django-stubs']:
                return self.config_parser['mypy.plugins.django-stubs']['django_settings_module']
        if 'isort' in sections:
            if 'known_first_party' in self.config_parser['isort']:
                return self.config_parser['isort']['known_first_party']

    def find_django_config_file(self):
        django_config_file = None
        for file in os.listdir(self.current_path):
            if file == 'setup.cfg':
                django_config_file = self.parse_setup_cfg(file)
            elif file == 'pytest.ini':
                django_config_file = self.parse_pytest_ini(file)
            if django_config_file:
                return django_config_file
            continue
    
    def get_all_apps(self):
        configuration = self.find_django_config_file()
        conf_import = importlib.import_module(configuration)
        apps = conf_import.LOCAL_APPS
        return apps
    
    def inspect_app_folder(self, app):
        path = Path(importlib.import_module(app).__file__).parent.resolve()
        for file in os.listdir(path):
            if file.startswith('test'):
                if Path(f'{path}/{file}').is_file():
                    return self.create_tests_folder(path, file)
                else:
                    if not '__init__.py' in os.listdir(f'{path}/{file}'):
                        with open(f'{path}/{file}/__init__.py', 'w') as f:
                            f.close()
                    return f'{path}/{file}'
        return self.create_tests_folder(path)
    
    def create_tests_folder(self, path: str, file:str = None):
        test_folder = f'{path}/tests'
        os.mkdir(test_folder)
        with open(f'{test_folder}/__init__.py', 'w') as f:
            f.close()
        if file:
            os.rename(f'{path}/{file}', f'{test_folder}/{file}')
        return test_folder
        
            

if __name__ == "__main__":
    apps = AutomateTests().get_all_apps()
    AutomateTests().inspect_app_folder('apps.escritos')