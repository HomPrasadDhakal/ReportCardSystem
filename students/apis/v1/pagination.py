from rest_framework.pagination import PageNumberPagination

class CustomPageNumberPagination(PageNumberPagination):
    """
    this call is developer for overing drf pagination
    Args:
        - Base call : PageNumberPagination
    Returns:
        - pagination
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
