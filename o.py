import firebase_admin
from firebase_admin import credentials, db
import threading
import time
from datetime import datetime
from colorama import init, Fore

# Inicializar a colorama
init(autoreset=True)

# Configuração do Firebase
firebase_config = {
    "type": "service_account",
    "project_id": "reflu-4db9e",
    "private_key_id": "318eaae02914abd4e8aba047e8aa9462261ddb35",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCz5AKLbtLtAhKM\nGe+B8xNEKJhQU4oqlqfhDkTMhag3bzgVh8b7XB77SMxdQmVmXHIe3jAUdEjVNGfo\n4F69mIiEgGHiOuzn10+08+heBaccFc2NI8gJj6HypzgsodXbQfbB1x98WZyMomIN\nJZbWfoNm7ATvMDDXfVVzet5nxoQSy1TTz+OkqIr4xPcn95OQzxCRCV9T29drC17n\nC+j54gOcQt8YUFSWQkEKlPM1/7LyCL5ZW3Ie1F/koXmztgytcpdZSE5CMMx2u8u3\n/M2zc4Rj3MupDE4xI5hY/l1Orw86VaN5fkORpaQzMBFy5jgFuOOL5jkQAL6om5I6\n+KO8Xlj5AgMBAAECggEAD1X7ysCtPH8sO9BsODzHFczy+AofLprlMs0OG9q0wnRG\njwm7v3fh7+DYnbmIca3Y6f1dxcI7tIPN7GI2zkM/0P5ggEv77WODZcHtCEyQEgqT\nzJmfA9DaAn9NM5Tgz/SzYWDoslrk+zvoT9M2cd1oPP2xb/8nDGZT3IJX9Cq0dyUq\nzF1HrhBiItuMaFB5rzylfCXGdzds3Dgo5SS+MM/ww+XHgHAh4Vh+2HRt/322K23e\neRF3UGoUnXIdxQO4hpbeYolSShWdAS5CWdfuNFPhaRNn8l7GDESpiij+X+9c52iU\ngf84WOkhUZJ1hFf0av2ctvs+SJ2rPSHc4cYdhknz1wKBgQD84Wxm/ni1YEh8YdmZ\nEA5DU69l6IFji7TD7z2WOEScOoqXvm4eMMCfSI9EkhwTv6a1gxpmOJrMZoo0PJuw\nWhLxsokQ7llVTT6GxcZHkKQ2H3DKX/2EDhvpGEF+HSFCOk0NK6ytfhLejBnHhcXk\nHun769XNqg/lGUj8EsGj8zryowKBgQC2HBcabFTyy3T51FTJy7/nE+Zrr2tK4Bfp\n+sTM4vTezzMgVbCHechjI2GeBTgdjWN2yNTobAKJN/GiXRGOizNlPNM059I/Qe+V\ncmdrsylKII2pyfY3MNJCH2zcEmm79NqvHv1S5gniTJSF3h8f23rtCpxlaVMSQdwJ\nRxokU6qbswKBgQCNHNHcC2aad/cbCZNeeXosEdfPu1XwkbY2nBs254FJ2NUb5lUW\nncfvWpMwBYSLdKf3pAgoQLAJHbNDgQqz9x+ZJjKccxUAp9EbbeO+bbVkylirZbNX\nbHQgt7tcP68egOAcWGHMkoy/CVkdYMXUDXgubyTo1lx2UIzMtT6/WWxslwKBgH39\njypTuq3Dfyl88jAui5T2Wpsz4NoLkd/qA4/wkRM5bJi5UAlagv27s8ScvccMU70R\nkuM+Hr8Kel0nYIcq3SL0YvceT4I+PuA5Jz4G1NEZFolaVcK3PzBKB4l2H7rO2yD/\nIqngxwPOkY7QLt5efXxTtAIhTTy7Xdz5WSe6zrUrAoGAP0fg8DUtgOZEbQtONOx3\nWsC4O2QcYfIRcwpuPJakuWKOSFrqG85NJbyTAWAbOITLv6+tOeL7sfpd+fSbOxlp\nYaPgfx+x4gqh1fDwE/YS4cRyw0NaQNflbS+LMcSRKyXq6RkFz+Nc/Kv9mBy6okFi\n0O/+Hp6/d6wKDCIHviPf8FI=\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-fxgrh@reflu-4db9e.iam.gserviceaccount.com",
    "client_id": "106837373430524925236",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fxgrh@reflu-4db9e.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
}

# Inicializar o Firebase Admin SDK
cred = credentials.Certificate(firebase_config)
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://reflu-4db9e-default-rtdb.firebaseio.com/'
})

chat_ref = db.reference('chat')

def listen_for_messages():
    def listener(event):
        if event.event_type == 'put' and event.path != '/':
            timestamp = event.data["timestamp"]
            message = event.data["message"]
            print(Fore.GREEN + f'\n[{timestamp}] Mensagem: {message}')

    chat_ref.listen(listener)

def fetch_and_display_messages():
    messages = chat_ref.get()
    if messages:
        for key, value in messages.items():
            timestamp = value.get("timestamp", "N/A")
            message = value.get("message", "N/A")
            print(Fore.GREEN + f'\n[{timestamp}] Mensagem: {message}')

def send_message():
    while True:
        message = input(Fore.CYAN + "\nDigite sua mensagem: ").strip()  # Remove espaços em branco extras
        if message:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            chat_ref.push({
                'message': message,
                'timestamp': timestamp
            })

if __name__ == '__main__':
    fetch_and_display_messages()
    threading.Thread(target=listen_for_messages, daemon=True).start()
    threading.Thread(target=send_message, daemon=True).start()

    # Mantém o script rodando
    while True:
        time.sleep(1)
