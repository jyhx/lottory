from flask import Flask

import config

# 初始化web应用
app = Flask(__name__, instance_relative_config=True)
app.config['DEBUG'] = config.DEBUG
app.config['LOTTERY'] = config.LOTTERY

from oppo_lottery import views
from oppo_lottery.dao import loadDataFromFile

loadDataFromFile('oppo_lottery/person.txt')
