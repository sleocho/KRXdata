import datetime
import logging.handlers
import logging
import os

def get_logger(name=None, log_nm='log', path='./'):            #기본값 지정, 파라미터
    # 로그 생성
    logger = logging.getLogger(name)

    # 로그의 출력 기준 설정
    logger.setLevel(logging.INFO)

    # log 출력 형식
    formatter = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s')

    # log 출력
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    #파일 사이즈 제한
    log_max_size = 10 * 1024 * 1024
    log_file_count = 20
    today = datetime.date.today().isoformat()
    log_name = f'{today}_{log_nm}.txt'
    filename = os.path.join(path, log_name)
     
    fileHandler = logging.handlers.RotatingFileHandler(filename=filename , maxBytes=log_max_size,
                                                       backupCount=log_file_count, encoding='utf-8')
    fileHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)
    
    return logger        




