from rest_framework.authentication import BaseAuthentication
from django.core.cache import cache
from mysite.models import User
from rest_framework import exceptions


class CustomerAuthentication(BaseAuthentication):
    """自定义认证,redis存在token通过，不存在直接认证失败"""
    def authenticate(self, request):
        # TODO 获取自定义头参数需要sufiix_key的大写才可以获取到
        token = request.META.get("HTTP_TOKEN", '')  # 检验传过来的和缓存等不等
        user_id = cache.get(token)  # todo 查缓存
        if user_id:
            user = User.objects.filter(id=user_id).first()
            print("开始鉴权userid is {},token is {} ".format(user_id,token))
            return user, token
        else:
            raise exceptions.AuthenticationFailed('无效token')

    def authenticate_header(self, request):
        pass
