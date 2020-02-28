import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'lsadubf3489sdalifb948asdv'
