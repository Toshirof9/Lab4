import http.server
import socketserver
import requests
import urllib.parse

PORT = int(input("Введіть порт: "))

class MyHttpRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            # Відповідь на запит GЕТ / - повертаємо сторінку з клієнтською частиною
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('index.html', 'rb') as file:
                self.wfile.write(file.read())
        elif self.path.endswith('.css'):
            # Відповідь на запит GЕТ /style.css - повертаємо вміст файлу style.css
            self.send_response(200)
            self.send_header('Content-type', 'text/css')
            self.end_headers()
            with open('style.css', 'rb') as file:
                self.wfile.write(file.read())
        elif self.path.endswith('.js'):
            # Відповідь на запит GЕТ /script.js - повертаємо вміст файлу script.js
            self.send_response(200)
            self.send_header('Content-type', 'text/javascript')
            self.end_headers()
            with open('script.js', 'rb') as file:
                self.wfile.write(file.read())
        elif self.path.startswith("/API"):
            # Відповідь на запит GЕТ /API - повертаємо дані з зовнішнього API
            query = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(query)
            if 'date' in params:
                date = params['date'][0]
                api_url = f"https://bank.gov.ua/NBUStatService/v1/statdirectory/res?date={date}"
                response = requests.get(api_url)
                if response.status_code == 200:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(response.content)
                else:
                    self.send_response(500)
                    self.end_headers()
            else:
                self.send_response(400)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"Missing 'date' parameter")
        else:
            # Інші запити - повертаємо статус 404
            self.send_response(404)
            self.end_headers()

# Створюємо об'єкт HTTP сервера
with socketserver.TCPServer(("", PORT), MyHttpRequestHandler) as httpd:
    print("Використовується порт:", PORT)
    print(f"Переходьте за посиланням: http://localhost:{PORT}/")
    print(f"Або за цим: http://127.0.0.1:{PORT}/")
    # Запускаємо сервер
    httpd.serve_forever()