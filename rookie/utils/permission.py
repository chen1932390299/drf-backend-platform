from rest_framework import permissions
from rest_framework.reverse import reverse


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.owner == request.user


class IsOwnerCheck(permissions.BasePermission):

    def has_permission(self, request, view):
        """
        map={"view_name":{"path_info","method "}
        }
        """

        maps = {
            'book_list': {'url': '/demo-service/api/v1/book/', 'method': 'GET'},
            'book_create': {'url': '/api/v1/book/', 'method': 'POST'}
        }
        results = False
        view_name = view.get_view_name()
        print(view_name,"xxxxxxxxxxx")

        if view_name in maps.keys() and request.method in permissions.SAFE_METHODS:
            mapper = maps.get(view_name)
            user_role_url = mapper.get('url',None)
            user_role_url_method = 'GET'
            # user_role_url = request.user.permission.url
            # user_role_url_method = request.user.permission.method.upper()
            print(request.method,request.path_info)
            if user_role_url == request.path_info and user_role_url_method ==request.method:
                return True
            else:
                return False
        else:
            return False

    def has_object_permission(self, request, view, obj):
        """  view表示当前视图， obj为数据对象 """
        return True
