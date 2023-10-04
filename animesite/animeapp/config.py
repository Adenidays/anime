from rest_framework.pagination import PageNumberPagination
from rest_framework import permissions


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
    page_query_param = 'page'


class IsAdminOrStaffUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_staff or request.user.is_superuser
