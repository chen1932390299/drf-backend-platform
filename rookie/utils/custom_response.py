from django.http import QueryDict
from rest_framework.response import Response
from rest_framework.serializers import Serializer


class CustomResponse(Response):

    def __init__(self, msg=None, success=None, code=None, data=None, status=None,
                 template_name=None, headers=None,
                 exception=False, content_type=None):
        """
        Alters the init arguments slightly.
        For example, drop 'template_name', and instead use 'data'.

        Setting 'renderer' and 'media_type' will typically be deferred,
        For example being set automatically by the `APIView`.
        """
        super(CustomResponse, self).__init__(self, None)

        if isinstance(data, Serializer):
            msg = (
                'You passed a Serializer instance as data, but '
                'probably meant to pass serialized `.data` or '
                '`.error`. representation.'
            )
            raise AssertionError(msg)
        self.code = code
        self.msg = msg
        if data :
            if isinstance(data,list):
                data ={'data':data}  # maybe data =  {**data} better
            if isinstance(data,(dict,QueryDict)):
                if 'data' in data.keys():
                    data=data
                else:
                    data = {"data": data}
        else:
            data = {"data": []}
        self.data = {**data, "msg": msg or "", "code": code, "success": success}

        # if isinstance(data,(dict,QueryDict)):
        #     self.data = {**data, "msg": msg or "", "code": code, "success": success,'22':33}
        # else:
        #     self.data = {"data": data, "msg": msg or "", "code": code, "success": success,'11':222}
        self.template_name = template_name
        self.exception = exception
        self.content_type = content_type

        if headers:
            for name, value in headers.items():
                self[name] = value
