# electric-shop

## Setup

1. git clone https://github.com/Pirate2606/electric-shop.git
2. cd electric-shop/
3. virtualenv -p python3 nameOfEnv
4. source nameOfEnv/bin/activate
5. Set your email address in 'sendmail.py' file.
5. pip install -r requirements.txt
6. export FLASK_APP=app.py
7. flask db init
8. flask db migrate -m "initial commit"
9. flask db upgrade


