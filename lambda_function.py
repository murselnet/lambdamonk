#import sys
#sys.path.insert(0, 'paketler')




from mangum import Mangum
#from main import app  # main.py dosyasındaki FastAPI/Flask 'app' nesnesini import ediyoruz
from fastapi import FastAPI

app = FastAPI() # Bu 'app' nesnesi Mangum tarafından kullanılacak
handler = Mangum(app)

@app.get("/")
async def read_root():
    return {"Hello": "World from FastAPI"}












"""
# Şimdi Mangum, FastAPI (main.py üzerinden) ve diğerlerini import edebilirsiniz
try:
    from mangum import Mangum
    from main import app # main.py dosyanızdaki FastAPI/Flask uygulamanız
except ImportError as e:
    # Eğer burada bir ImportError alırsanız, sys.path doğru çalışmıyor veya
    # 'paketler' klasöründe eksik bir şeyler var demektir.
    # Bu log'u CloudWatch'ta görebilirsiniz.
    print(f"Import hatası: {e}")
    # Daha fazla hata ayıklama için sys.path'i yazdırabilirsiniz:
    print(f"sys.path: {sys.path}")
    raise e # Orijinal hatayı tekrar yükseltin ki Lambda bunu raporlasın

handler = Mangum(app)
"""

"""
import requests

def lambda_handler(event, context):
    response = requests.get("https://api.github.com")
    return {
        "statusCode": 200,
        "body": response.json()
    }
"""



"""
import json

def lambda_handler(event, context):
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda! From MRS MURSEL GitHub Actions!')
    }
"""
