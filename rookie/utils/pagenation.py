from rest_framework import pagination
from rest_framework.response import Response


class ListPagination(pagination.PageNumberPagination):
    """"user custom pagination class"""
    page_size_query_param = "page_size"
    page_query_param = 'page'
    page_size = 10
    max_page_size = 100

    def get_paginated_response(self, data):
        """
        重写分页response方法，参考原PageNumberPagination class
        """
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'data': data,
            'page_size': self.page.paginator.per_page,
            'page': self.page.start_index() // self.page.paginator.per_page + 1,
            'totals': self.page.paginator.count,
        })
