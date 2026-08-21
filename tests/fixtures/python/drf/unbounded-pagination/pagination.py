class PageNumberPagination:
    page_size = 20
    page_size_query_param = None
    max_page_size = None

class UnsafePagination(PageNumberPagination):
    # VULNERABLE: Client-controlled page size without maximum ceiling
    page_size = 20
    page_size_query_param = 'page_size'
