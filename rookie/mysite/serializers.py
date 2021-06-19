import datetime
import re
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import (RunSuiteRecord, User,ProjectConfig,
                     TestCase, TestSuite, VariablesGlobal,ScheduleTrigger)
from utils.func_tools import iso2timestamp
from rest_framework.validators import UniqueValidator



class UserSerializer(serializers.ModelSerializer):
    # style表示前台输入是密文，write_only表示序列化时不会序列化该字段
    password = serializers.CharField(write_only=True, max_length=256)

    class Meta:
        model = User
        fields = ('uuid', 'username', 'password', 'mobile', 'email')
        extra_kwargs = {
            "password": {"write_only": True}
        }

    # 创建用户时更新密码为密文
    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    # 更新用户时更新密码为密文
    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        if 'password' in validated_data.keys():
            user.set_password(validated_data['password'])
        user.save()
        return user

    # 重写to_representation方法，自定义响应中的json数据
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['uuid'] = ret['uuid'].replace('-', '')
        return ret




class SerializerTestCase(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    case_name = serializers.CharField(max_length=50, required=True,
                                      validators=[UniqueValidator(queryset=TestCase.objects.all())])
    project_id = serializers.IntegerField(required=True,min_value=1)
    project_name = serializers.SerializerMethodField()
    method = serializers.CharField(max_length=10, required=True)
    url = serializers.CharField(max_length=500, required=True)
    params = serializers.CharField(max_length=500, allow_blank=True, allow_null=True)
    headers = serializers.JSONField()
    mine_type = serializers.CharField(max_length=5, required=True)
    body = serializers.JSONField()
    response = serializers.JSONField(required=False)
    extract = serializers.JSONField(required=False)
    assert_express = serializers.JSONField(required=False)
    error_msg = serializers.JSONField(required=False)
    status = serializers.CharField(max_length=20, required=False)
    create_time = serializers.DateTimeField(read_only=True)
    update_time = serializers.DateTimeField(read_only=True)

    class Meta:
        model = TestCase
        fields = ("id", "case_name","project_id","project_name" ,"method", "url", "params", "headers",
                  "mine_type", "body", "response", "extract", "assert_express", "error_msg",
                  "status", "create_time", "update_time")

    def get_project_name(self,obj):
          proejct_obj = ProjectConfig.objects.filter(id=obj.project_id).first()

          return proejct_obj.project_name



class SerialTestSuite(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    suite_name = serializers.CharField(max_length=50, required=True, allow_null=False, allow_blank=False)
    cases_list = serializers.JSONField(required=True)
    status = serializers.CharField(max_length=20, required=False)

    class Meta:
        model = TestSuite
        fields = ("id", "suite_name", "cases_list", "status")


class SerialVaribales(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=50, required=True,
                                 validators=[UniqueValidator(queryset=VariablesGlobal.objects.all())]
                                 )
    variable_value = serializers.CharField(max_length=3000)
    create_time = serializers.DateTimeField(read_only=True)
    update_time = serializers.DateTimeField(read_only=True)

    class Meta:
        model = VariablesGlobal
        fields = ("id", "name", "variable_value", "create_time", "update_time")


class RunTestSuiteSerializer(serializers.ModelSerializer):
    suite_ids = serializers.ListField(child=serializers.IntegerField(min_value=1, max_value=999999), max_length=100)

    class Meta:
        model = RunSuiteRecord
        fields = "__all__"


class ScheduleSerializer(serializers.ModelSerializer):
    choices = [('1', '按日期执行'), ('2', '间隔周期执行'), ('3', "cron 定时器执行")]
    id = serializers.IntegerField(read_only=True)
    schedule_args=serializers.ListField(required=True,child=serializers.IntegerField(min_value=1, max_value=999999), max_length=100)
    schedule_type = serializers.ChoiceField(choices=choices,required=True)
    schedule_time = serializers.CharField(max_length=50,required=True,
                                          allow_null=False, allow_blank=False
                                          )
    enable =serializers.BooleanField(required=True)
    create_time = serializers.DateTimeField(read_only=True)
    update_time = serializers.DateTimeField(read_only=True)

    class Meta:
        model = ScheduleTrigger
        fields="__all__"


class ProjectSerializer(serializers.ModelSerializer):
    id =serializers.IntegerField(read_only=True)
    project_name = serializers.CharField(max_length=50,required=True,
                                         validators=[UniqueValidator(queryset=ProjectConfig.objects.all())]
                                         )
    create_time = serializers.DateTimeField(read_only=True)
    update_time = serializers.DateTimeField(read_only=True)


    class Meta:
        model = ProjectConfig
        fields="__all__"
