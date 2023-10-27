import datetime

today = datetime.date.today().isoformat()

TODAY = lambda: datetime.date.today().strftime( '%Y%m%d' )

class Config:

    TODAY = TODAY()

    BASE_PATH = "C:/Users/sally/OneDrive/문서/GitHub/KRX/KRXdata"
    LOG_PATH = "C:/Users/sally/OneDrive/문서/GitHub/KRX/KRXdata/log"
    JSON_PATH = "C:/Users/sally/OneDrive/문서/GitHub/KRX/KRXdata/raw"
    OUTCOME_PATH = "C:/Users/sally/OneDrive/문서/GitHub/KRX/KRXdata/outcome"
    CSV_PATH = f"C:/Users/sally/OneDrive/문서/GitHub/KRX/KRXdata/dl_ods/{today}_dl_ods.csv"
     
    