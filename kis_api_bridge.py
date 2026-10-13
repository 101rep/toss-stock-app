"""
한국투자증권(KIS) & 야후 파이낸스(Yahoo Finance) 통합 로컬 브릿지 서버
국내 주식 및 미국 주식 실시간 시세, 과거 히스토리 캔들/라인 데이터 프록시
"""

import http.server
import socketserver
import json
import urllib.request
import urllib.parse
import urllib.error
import webbrowser
import os

PORT = 8092
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

# 한국투자증권 실전투자 및 모의투자 도메인
KIS_PROD_URL = "https://openapi.koreainvestment.com:9443"
KIS_MOCK_URL = "https://openapivts.koreainvestment.com:29443"

class MultiBridgeHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        # 1. Yahoo Finance API 프록시 엔드포인트
        if self.path.startswith("/api/yahoo/chart"):
            parsed_url = urllib.parse.urlparse(self.path)
            query_params = urllib.parse.parse_qs(parsed_url.query)

            symbol = query_params.get("symbol", ["NVDA"])[0]
            interval = query_params.get("interval", ["1d"])[0]
            chart_range = query_params.get("range", ["1mo"])[0]

            yahoo_url = f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(symbol)}?range={chart_range}&interval={interval}"

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'application/json'
            }

            req = urllib.request.Request(yahoo_url, headers=headers)
            try:
                with urllib.request.urlopen(req, timeout=10) as resp:
                    resp_data = resp.read()
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(resp_data)
                    return
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
                return

        return super().do_GET()

    def do_POST(self):
        # 2. 한국투자증권 OAuth 토큰 발급 프록시
        if self.path == "/api/kis/token":
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))

            app_key = data.get("app_key")
            app_secret = data.get("app_secret")
            is_mock = data.get("is_mock", False)

            base_url = KIS_MOCK_URL if is_mock else KIS_PROD_URL
            token_url = f"{base_url}/oauth2/tokenP"

            req_body = json.dumps({
                "grant_type": "client_credentials",
                "appkey": app_key,
                "appsecret": app_secret
            }).encode('utf-8')

            req = urllib.request.Request(token_url, data=req_body, headers={'Content-Type': 'application/json'})

            try:
                with urllib.request.urlopen(req, timeout=10) as resp:
                    resp_data = json.loads(resp.read().decode('utf-8'))
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps(resp_data).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, authorization, appkey, appsecret, tr_id')
        self.end_headers()

if __name__ == "__main__":
    print(f"================================================================")
    print(f" 토스 증권 스타일 뷰어 & KIS / 야후 파이낸스 브릿지 서버 가동")
    print(f" 주소: http://localhost:{PORT}")
    print(f"================================================================")
    webbrowser.open(f"http://localhost:{PORT}/index.html")
    with socketserver.TCPServer(("", PORT), MultiBridgeHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n브릿지 서버를 종료합니다.")
