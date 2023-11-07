import json
import natsort
import pandas as pd
import os
from datetime import datetime
import traceback
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
import matplotlib
matplotlib.use('Agg')       #서버에서, 화면에 표시하기 위해서 필요
#import seaborn as sns
# import altair as alt               ##https://altair-viz.github.io/
# import plotly.express as px
from config import Config
from logger import get_logger

logger = get_logger(name = "main_log", log_nm="main_log", path = Config.LOG_PATH)

class KRX:
    def read_all_json_files_in_directory(self, directory_path: str):
        json_files = defaultdict(list)
        date_format = "%Y%m%d%H%M%S"
        result = dict()
       
        for root, _, files in os.walk(directory_path):
            for file in files:
                if file.endswith('.json'):  # JSON 파일만 처리
                    filename = os.path.join(root, file)\                    
                    json_files[root].append(filename)
       
        file_name_list = list()     
        for i in json_files.keys():
            file_list = list(reversed(natsort.natsorted(os.listdir(i))))   
            ticker_list = list()
            for data in file_list:
                
                date_time = data.split("_")[-1].split(".json")[0]
                ticker = '_'.join(data.split('_')[:-1])
                ticker = f'{i}\\{ticker}'

                if ticker in ticker_list:
                    continue
                ticker_list.append(ticker)
                file_name_list.append(f'{ticker}_{date_time}.json')    
            break    ###

        for filename in file_name_list:        
            file_name = filename.split("_")[-1].split(".json")[0]
            
            leaf = filename.split( '.' )[ 0 ].strip()
            group_id, index_id, dummy, timestamp = list( map( str.strip, leaf.split( '_' ) ) )
            asof = timestamp[ :8 ]

            date_obj = datetime.strptime(file_name, date_format)  #file_name
            formatted_date = date_obj.strftime("%Y-%m-%d")

            __ = list()
            with open(filename, 'r', encoding='utf-8') as json_file:
            # JSON 파일 파싱
                data = json.load(json_file)
                
                for data_dict in data["output"]:
                    
                    result_dict = {"basedate" : formatted_date, "종목코드" : data_dict['isu_cd'], "종목명" : data_dict['isu_nm'], "현재가" : data_dict['tdd_clsprc'], "대비" : data_dict['cmpprevdd_prc'],
                                "등락률(%)" : data_dict['updn_rate'], "거래대금(원)" : data_dict['acc_trdval']}
                               
                    if 'mktcap' in data_dict:
                        result_dict["상장시가총액(원)"] =  data_dict['mktcap']

                    __.append(result_dict)
            if dummy:
                uniq = ( asof, index_id, dummy )
            else:
                uniq = ( asof, index_id )
            if uniq not in result:
                result[ uniq ] = __
            else:
                result[ uniq ].extend( __ )

        return result

    def mk_csv(self, json_data: dict):
        loot = Config.OUTCOME_PATH
        if not os.path.isdir( loot ):
            os.makedirs( loot, exist_ok = True )

        for k, v in json_data.items():
            if len(k) ==2:
                asof, index_id = k
                dest = os.path.join( loot, '{}-{}.csv'.format( index_id, asof ) )
            else:
                asof, index_id, index_num = k
                dest = os.path.join( loot, '{}-{}-{}.csv'.format( index_id, index_num, asof ) )
            asdf = pd.DataFrame( v )
            asdf.to_csv( dest, index=False, encoding="euc-kr")
            

krx = KRX()
json_data = krx.read_all_json_files_in_directory(Config.JSON_PATH + "/MKD03040101")
#print(json_data)
krx.mk_csv(json_data)