
from pages.home_page import HomePage


class Pages:
    home = HomePage

    def __init__(self, page, request):
        self.page = page
        self.request = request
        self.home = HomePage(page, request)
