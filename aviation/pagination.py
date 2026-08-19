from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    page_size = 10                  # Default page size
    page_size_query_param = 'size'  # Allow users to change pagination size
    max_page_size = 100             # Protection Against Excessively Large Requests
