import datetime
import re
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import (RunSuiteRecord, User,ProjectConfig,
                     TestCase, TestSuite, VariablesGlobal,ScheduleTrigger,TaskExcuteRecord)
from  . import models
from rest_framework.validators import UniqueValidator,UniqueTogetherValidator


class UserSerializer(serializers.ModelSerializer):
    # style表示前台输入是密文，write_only表示序列化时不会序列化该字段
    password = serializers.CharField(write_only=True, max_length=256)
    uuid = serializers.UUIDField(read_only=True)
    create_time = serializers.DateTimeField(read_only=True)
    update_time = serializers.DateTimeField(read_only=True)
    class Meta:
        model = User
        fields = ('id','uuid', 'username', 'password', 'mobile', 'email','create_time','update_time')
        extra_kwargs = {
            "password": {"write_only": True}
        }

        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['username', 'mobile']
            )
        ]

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

class RoleSerializer(serializers.ModelSerializer):

    role_type_value = serializers.CharField(source="get_role_type_display",max_length=10,read_only=True)
    status_value = serializers.CharField(source="get_status_display",max_length=10,read_only=True)

    class Meta:
        model = models.RoleInfo
        fields= ['id','role_name','role_type','role_type_value',
                 'status','status_value','create_time','update_time']
        validators = [
            UniqueTogetherValidator(
                queryset=models.RoleInfo.objects.all(),
                fields=['role_name']
            )
        ]

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
    items = serializers.SerializerMethodField()
    status = serializers.CharField(max_length=20, required=False)
    # obj represent TestSuite object
    def get_items(self,testsuite_obj):
        instances = TestCase.objects.filter(id__in=[item.get("id") for item in testsuite_obj.cases_list])
        data = []
        for instance in  instances:
            data.append({"id":instance.id,"name":instance.case_name,"status":instance.status})
        return data
    class Meta:
        model = TestSuite
        fields = ("id", "suite_name", "cases_list", "status","items")


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
    taskid = serializers.UUIDField(read_only=True)
    suite_ids = serializers.ListField(child=serializers.IntegerField(min_value=1, max_value=999999), max_length=100)
    suite_items = serializers.SerializerMethodField()
    status =  serializers.ChoiceField(choices=[('0',"未执行"),('1','执行失败'),('2',"执行成功")],required=False)
    status_name = serializers.CharField(source="get_status_display",read_only=True)
    create_by = serializers.CharField(max_length=50,required=False)
    create_time = serializers.DateTimeField(read_only=True)
    update_time = serializers.DateTimeField(read_only=True)

    def get_suite_items(self,obj):
        serial  = SerialTestSuite(instance=TestSuite.objects.filter(id__in=obj.suite_ids),many=True)
        return  serial.data
    class Meta:
        model = RunSuiteRecord
        fields = ['taskid','suite_ids','suite_items','status','status_name','create_by','create_time','update_time']


class TaskExcuteList(serializers.ListSerializer):
    def update(self, instance_queryset, validated_data_list):
        queryset=[]
        for index, validated_data in enumerate(validated_data_list):
            inst=self.child.update(instance_queryset[index], validated_data)
            queryset.append(inst)
        return queryset

class TaskExcuteSerializer(serializers.ModelSerializer):
    params = serializers.CharField(max_length=500, allow_blank=True, allow_null=True)
    create_time = serializers.DateTimeField(read_only=True)
    update_time = serializers.DateTimeField(read_only=True)
    class Meta:
        model = TaskExcuteRecord
        fields = "__all__"
        list_serializer_class = TaskExcuteList

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
