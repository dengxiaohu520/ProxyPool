import time
from multiprocessing import Process
from proxypool.getter import Getter
from proxypool.tester import Tester
from proxypool.setting import *
from datetime import datetime


class Scheduler():
    def schedule_tester(self, cycle=TESTER_CYCLE):
        """
        定时测试代理
        """
        tester = Tester()
        while True:
            print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '测试器开始运行')
            tester.run()
            time.sleep(cycle)
    
    def schedule_getter(self, cycle=GETTER_CYCLE):
        """
        定时获取代理
        """
        getter = Getter()
        while True:
            print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '开始抓取代理')
            getter.run()
            time.sleep(cycle)
    
    def schedule_api(self):
        """
        开启API
        """
        if API_SOURCE.upper() == 'FLASK':
            from proxypool.api_flask import app
            app.run(API_HOST, API_PORT)
        elif API_SOURCE.upper() == 'AIOHTTP':
            from aiohttp import web
            from proxypool.api_aiohttp import app
            web.run_app(app=app, host=API_HOST, port=API_PORT)
        elif API_SOURCE.upper() == 'FASTAPI':
            pass
        elif API_SOURCE.upper() == 'VIBORA':
            pass
    
    def run(self):
        print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '代理池开始运行')
        
        if TESTER_ENABLED:
            tester_process = Process(target=self.schedule_tester)
            tester_process.start()
        
        if GETTER_ENABLED:
            getter_process = Process(target=self.schedule_getter)
            getter_process.start()
        
        if API_ENABLED:
            api_process = Process(target=self.schedule_api)
            api_process.start()
