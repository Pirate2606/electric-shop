# electric-shop

## Setup

    1. git clone https://github.com/Pirate2606/electric-shop.git
    2. cd electric-shop/
    3. virtualenv -p python3 nameOfEnv
    4. source nameOfEnv/bin/activate
    5. Set your email address in 'sendmail.py' file.
    6. pip install -r requirements.txt
    7. export FLASK_APP=app.py
    8. flask db init
    9. flask db migrate -m "initial commit"
    10. flask db upgrade
    11. python3 app.py
