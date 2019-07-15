import time
from http.server import HTTPServer
from server import Server

Host = 'localhost'
Port = 8004


if __name__ == '__main__':
    httpd = HTTPServer((Host, Port), Server)
    print(f"{time.asctime()} Server up - {Host} {Port}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print(f"{time.asctime()} Server down - {Host} {Port}")
