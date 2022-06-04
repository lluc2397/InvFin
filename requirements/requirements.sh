virtualenv temp_venv
$1 install -U pip
$1 install -r requirements/base.txt
$1 freeze > requirements/requirements.txt
$1 list --outdated --format=columns > requirements/outdated.txt