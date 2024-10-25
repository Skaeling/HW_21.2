from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

hostName = "localhost"
serverPort = 8080


class MyServer(BaseHTTPRequestHandler):
    """Класс для отправки запросов к серверу"""
    @staticmethod
    def __open_page(filename: str):
        """Считывает код html из заданного файла возвращает содержимое страницы"""
        with open(filename, 'r') as f:
            return f.read()

    def __get_menu_content(self, page_address: str):
        """Возвращает содержимое страницы в соответствии с запросом, в случае ошибки возвращает уведомление"""
        if page_address == 'category1':
            return self.__open_page("category1.html")
        elif page_address == 'contacts':
            return self.__open_page("contacts.html")
        elif page_address == 'catalog':
            return self.__open_page("catalog.html")
        elif page_address == 'home':
            return self.__open_page('home.html')

        return 'Page not found!'

    def do_GET(self):
        query_components = parse_qs(urlparse(self.path).query)
        page_address = query_components.get('page')
        page_content = self.__open_page('contacts.html')
        if page_address:
            page_content = self.__get_menu_content(page_address[0])
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(page_content, "utf-8"))


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
