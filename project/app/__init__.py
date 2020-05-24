from flask import Flask, jsonify,request
import json
#import schedule
from datetime import datetime,timedelta
from datetime import date
from apscheduler.schedulers.background import BackgroundScheduler
#from flask_apscheduler import APScheduler
# Start the scheduler

app = Flask(__name__)

# scheduler = APScheduler()
# scheduler.init_app(app)
# scheduler.start()
#from apscheduler.scheduler import Scheduler

scheduler = BackgroundScheduler()
scheduler.start()
from app import views