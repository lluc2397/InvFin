from rest_framework.pagination import LimitOffsetPagination


class LargeResultsSetPagination(LimitOffsetPagination):
    default_limit = 100
    limit_query_param = 'limit'
    limit_query_description = ('Number of results to return per page.')
    offset_query_param = 'offset'
    offset_query_description = ('The initial index from which to return the results.')
    max_limit = None
    template = 'rest_framework/pagination/numbers.html'


class StandardResultsSetPagination(LimitOffsetPagination):
    default_limit = 50
    limit_query_param = 'limit'
    limit_query_description = ('Number of results to return per page.')
    offset_query_param = 'offset'
    offset_query_description = ('The initial index from which to return the results.')
    max_limit = None
    template = 'rest_framework/pagination/numbers.html'