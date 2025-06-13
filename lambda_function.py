import sys
import json
import logging

# Logging yapılandırması
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Paketler klasörünü Python path'ine ekle
sys.path.insert(0, 'paketler')

# Import işlemleri
try:
    from mangum import Mangum
    from main import app  # main.py dosyasındaki FastAPI uygulaması
    logger.info("Başarıyla import edildi: mangum ve main.app")
except ImportError as e:
    logger.error(f"Import hatası: {e}")
    logger.error(f"sys.path: {sys.path}")
    raise e



# Custom Mangum wrapper class
class CustomMangum:
    def __init__(self, app):
        self.app = app
        self.mangum = Mangum(
            app,
            lifespan="off",
            api_gateway_base_path=None,
            text_mime_types=[
                "application/json",
                "application/javascript",
                "application/xml",
                "application/vnd.api+json",
                "text/plain",
                "text/html",
            ],
        )
    
    def __call__(self, event, context):
        # Event'i log'la
        logger.info(f"Received event: {json.dumps(event, default=str)}")
        
        # Event formatını kontrol et ve düzelt
        if not self._is_api_gateway_event(event):
            logger.info("Event API Gateway formatına dönüştürülüyor")
            event = self._convert_to_api_gateway_event(event)
            logger.info(f"Converted event: {json.dumps(event, default=str)}")
        
        try:
            # Mangum handler'ını çağır
            response = self.mangum(event, context)
            logger.info(f"Response: {json.dumps(response, default=str)}")
            return response
        except Exception as e:
            logger.error(f"Mangum handler hatası: {str(e)}")
            return self._error_response(str(e))
    
    def _is_api_gateway_event(self, event):
        """Event'in API Gateway formatında olup olmadığını kontrol et"""
        required_fields = ['httpMethod', 'headers', 'requestContext']
        return all(field in event for field in required_fields)
    
    def _convert_to_api_gateway_event(self, event):
        #!>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        """
        Event'i API Gateway formatına dönüştür
        
        ⚠️  ŞABLON VERİLER - Gerçek production'da AWS tarafından otomatik doldurulur
        Bu bölümdeki tüm değerler test amaçlı sahte verilerdir!
        """
        # ===== ŞABLON BAŞLANGICI - Gerçek API Gateway Event Template =====
        api_gateway_event = {
            # 🔹 Bu alan gerçekte dynamic olarak değişir
            "resource": "/",  # ŞABLON: Gerçekte API Gateway resource path'i gelir
            "path": "/",      # ŞABLON: Gerçekte request edilen path gelir
            "httpMethod": "GET",  # ŞABLON: Gerçekte kullanılan HTTP method gelir
            
            # 🔹 Headers - AWS tarafından otomatik eklenir/güncellenir
            "headers": {
                "Accept": "application/json",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en-US,en;q=0.9",
                "Content-Type": "application/json",
                # ŞABLON: Gerçekte client'ın gerçek Host header'ı gelir
                "Host": "example.execute-api.region.amazonaws.com",  
                "User-Agent": "Custom User Agent String",  # ŞABLON: Gerçek user agent gelir
                # ŞABLON: AWS X-Ray tracing ID - her request için benzersiz
                "X-Amzn-Trace-Id": "Root=1-5e66d96f-7491f09xmpl79d18acf3d050"
            },
            
            # 🔹 Multi-value headers - AWS tarafından otomatik organize edilir
            "multiValueHeaders": {
                "Accept": ["application/json"],
                "Accept-Encoding": ["gzip, deflate, br"]
            },
            
            # 🔹 Bu alanlar gerçekte request'e göre doldurulur
            "queryStringParameters": None,  # ŞABLON: ?param=value varsa buraya gelir
            "multiValueQueryStringParameters": None,
            "pathParameters": None,  # ŞABLON: /users/{id} gibi path params gelir
            "stageVariables": None,  # ŞABLON: API Gateway stage variables
            
            # ===== EN ÖNEMLİ ŞABLON BÖLÜMÜ - REQUEST CONTEXT =====
            "requestContext": {
                # ŞABLON: Her API için benzersiz resource ID
                "resourceId": "123456",
                # ŞABLON: Resource path template
                "resourcePath": "/",
                # ŞABLON: HTTP method (yukarıdaki ile aynı)
                "httpMethod": "GET",
                
                # 🚨 ŞABLON - AWS tarafından her request için YENİ OLUŞTURULUR
                "extendedRequestId": "JJbxmplHYosFVYQ=",  # Her çağrıda farklı olur
                "requestTime": "10/Mar/2020:00:03:59 +0000",  # Gerçek zaman gelir
                "requestTimeEpoch": 1583798639428,  # Gerçek epoch time gelir
                
                # ŞABLON: API Gateway deployment bilgileri
                "path": "/Prod/",  # Gerçek stage path gelir
                "accountId": "123456789012",  # Gerçek AWS Account ID gelir
                "protocol": "HTTP/1.1",
                "stage": "Prod",  # Gerçek stage name gelir (dev, prod, test vs.)
                
                # 🚨 ŞABLON - Her API Gateway için FARKLI OLUR
                "domainPrefix": "70ixmpl4fl",  # Gerçek domain prefix gelir
                "requestId": "JJbxmpl-xmpl-xmpl-xmpl-xmplHYosFVYQ",  # Her request benzersiz
                
                # 🔹 Client identity bilgileri - AWS tarafından doldurulur
                "identity": {
                    "accessKey": None,  # IAM access varsa gelir
                    "accountId": None,
                    "caller": None,
                    "cognitoAuthenticationProvider": None,  # Cognito auth varsa gelir
                    "cognitoAuthenticationType": None,
                    "cognitoIdentityId": None,
                    "cognitoIdentityPoolId": None,
                    "principalOrgId": None,
                    "sourceIp": "192.0.2.1",  # ŞABLON: Gerçek client IP gelir
                    "user": None,
                    "userAgent": "Custom User Agent String",  # ŞABLON: Gerçek user agent
                    "userArn": None,
                    "apiKey": None,  # API Key kullanılıyorsa gelir
                    "apiKeyId": None
                },
                
                # 🚨 ŞABLON - Bu değerler gerçekte API Gateway'e özel olur
                "domainName": "70ixmpl4fl.execute-api.us-east-2.amazonaws.com",  # Gerçek domain
                "apiId": "70ixmpl4fl"  # Gerçek API Gateway ID'si
            },
            # ===== REQUEST CONTEXT ŞABLON SONU =====
            
            # 🔹 Request body - POST/PUT request'lerde gelir
            "body": None,  # ŞABLON: Gerçek request body buraya gelir
            "isBase64Encoded": False  # Binary data için true olur
        }
        # ===== ŞABLON SONU =====
        #!>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        
        # 🔧 Eğer orijinal event'te bazı GERÇEK değerler varsa onları kullan
        if isinstance(event, dict):
            # HTTP method'u güncelle
            if 'httpMethod' in event:
                api_gateway_event['httpMethod'] = event['httpMethod']
            elif 'method' in event:
                api_gateway_event['httpMethod'] = event['method']
            
            # Path'i güncelle
            if 'path' in event:
                api_gateway_event['path'] = event['path']
                api_gateway_event['resource'] = event['path']
                api_gateway_event['requestContext']['resourcePath'] = event['path']
            
            # Body'yi güncelle
            if 'body' in event:
                api_gateway_event['body'] = event['body']
            
            # Headers'ı güncelle (gerçek headers varsa)
            if 'headers' in event and isinstance(event['headers'], dict):
                api_gateway_event['headers'].update(event['headers'])
        
        return api_gateway_event
    
    def _error_response(self, error_message):
        """
        Hata durumunda API Gateway uyumlu response döndür
        
        ⚠️  Bu format API Gateway tarafından beklenen standart format
        """
        return {
            "statusCode": 500,  # HTTP status code
            "headers": {
                "Content-Type": "application/json",
                # CORS headers - production'da domain'inize göre ayarlayın
                "Access-Control-Allow-Origin": "*",  # 🚨 Production'da "*" yerine domain kullanın
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PUT,DELETE"
            },
            "body": json.dumps({  # Response body JSON string olarak
                "error": "Internal Server Error",
                "message": error_message
            })
        }


#!>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Handler'ı oluştur
handler = CustomMangum(app)

# Lambda handler fonksiyonu (AWS Lambda tarafından çağrılır)
def lambda_handler(event, context):
    """
    AWS Lambda entry point
    
    ⚠️  Bu fonksiyon AWS Lambda tarafından otomatik çağrılır
    - event: API Gateway'den gelen request data
    - context: AWS Lambda runtime context
    """
    return handler(event, context)



"""
🚨 Şablon Bölümlerin Özeti:
Tamamen Sahte/Şablon Olan Değerler:

"extendedRequestId": "JJbxmplHYosFVYQ=" → Her request için benzersiz olur
"requestTime": "10/Mar/2020:00:03:59 +0000" → Gerçek zaman gelir
"domainName": "70ixmpl4fl.execute-api..." → Gerçek API domain gelir
"apiId": "70ixmpl4fl" → Gerçek API Gateway ID'si gelir
"accountId": "123456789012" → Gerçek AWS Account ID gelir

🔧 Gerçek Değerlerle Değiştirilen Bölümler:

httpMethod, path, body, headers → Event'ten alınan gerçek değerler

🎯 Production'da Değişmesi Gerekenler:

"Access-Control-Allow-Origin": "*" → Gerçek domain'iniz
"stage": "Prod" → Gerçek stage name'iniz

💡 Sonuç:
Bu kodda şablon olan her şey sadece test amaçlı. Gerçek API Gateway ile çalıştığında AWS bu değerleri otomatik olarak gerçek verilerle değiştirir. Siz sadece FastAPI kodunuza odaklanın! 🚀
"""












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
