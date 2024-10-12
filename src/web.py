from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import os


class MyServer(BaseHTTPRequestHandler):
    """
    Специальный класс, который отвечает за
    обработку входящих запросов от клиентов
    """

    @staticmethod
    def __get_file(filepath):
        """ Получение кода запрашиваемого файла """
        with open(filepath, "rb") as file:
            return file.read()

    def __get_index(self):
        """ Получение кода главной страницы """
        return self.__get_file("site/index.html")

    @staticmethod
    def __get_filepath(page_address):
        """
        Метод для получения пути возвращаемой страницы

        :param page_address: Название запрашиваемой страницы
        :return: Путь HTML-страницы
        """
        # Проверка существования запрашиваемой страницы
        if page_address in ["index", "categories", "catalog", "contacts"]:
            filename = page_address + ".html"
        else:
            filename = "404.html"

        # Формирование пути к файлу, содержащему код HTML-страницы
        return os.path.join("site", filename)

    def do_GET(self):
        """ Метод для обработки входящих GET-запросов """
        content_type = "text/html; charset=utf-8"
        query_components = parse_qs(urlparse(self.path).query)
        page_content = self.__get_index()

        # Если есть параметры запроса
        if "page" in query_components:
            page_address = query_components.get("page")
            if page_address and page_address[0]:
                filepath = self.__get_filepath(page_address[0])
                page_content = self.__get_file(filepath)
                if not page_content:
                    page_content = self.__get_file("site/404.html")  # 404 страница
            else:
                page_content = self.__get_file("site/404.html")  # 404 страница
        else:
            # Если параметры отсутствуют, проверка на статику (css, js, svg) или главная страница
            path = self.path.lstrip("/")  # Удаление начального слэша
            filepath = os.path.join("site", path)

            if os.path.isfile(filepath):
                # Определяем тип содержимого
                if filepath.endswith(".css"):
                    content_type = "text/css"
                elif filepath.endswith(".js"):
                    content_type = "application/javascript"
                elif filepath.endswith(".svg"):
                    content_type = "image/svg+xml"
                elif filepath.endswith(".png"):
                    content_type = "image/png"
                page_content = self.__get_file(filepath)

        self.send_response(200)  # Отправка кода ответа
        self.send_header("Content-type", content_type)  # Отправка типа данных
        self.end_headers()  # Завершение формирования заголовков ответа
        self.wfile.write(page_content)  # Тело ответа
