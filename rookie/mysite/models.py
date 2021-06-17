import uuid
from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class UUIDTools(object):
    @staticmethod
    def uuid4_hex():
        return uuid.uuid4().hex


class User(models.Model):
    uuid = models.UUIDField(default=UUIDTools.uuid4_hex)
    username = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=256)
    mobile = models.CharField(max_length=11, blank=True, unique=True)  # 可选
    email = models.EmailField(max_length=64, blank=True, unique=True)

    # role = models.ManyToManyField(to=Roles, related_name='role')

    def set_password(self, password):
        self.password = make_password(password)
        return None

    def check_pwd(self, password):
        # password 入参原始密码，数据库密码
        db_pwd = self.password
        return check_password(password, db_pwd)

    class Meta:
        db_table = "tbl_user"
        verbose_name = 'user信息表'


class BaseModel(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True



def default_body():
    return {}




class TestCase(models.Model):
    case_name = models.CharField(max_length=50, null=False, unique=True)
    project_id =models.IntegerField(null=False)
    method = models.CharField(max_length=10, null=False)
    url = models.CharField(max_length=500, null=False)
    params = models.CharField(max_length=500, null=True)
    headers = models.JSONField(null=True)
    mine_type = models.CharField(max_length=5)
    body = models.JSONField(null=True)
    response = models.JSONField(null=True)
    extract = models.JSONField(null=True)
    assert_express = models.JSONField(null=True)
    error_msg = models.JSONField(null=True)
    status = models.CharField(max_length=20, default="0")
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tbl_case_info"
        verbose_name = "接口用例表"
        ordering = ["id"]


class TestSuite(models.Model):
    suite_name = models.CharField(max_length=50, null=False, default="0")
    case_id = models.JSONField()
    status = models.CharField(max_length=20, default="0")

    class Meta:
        db_table = "tbl_test_suite"
        verbose_name = "接口套件表"
        ordering = ["id"]


class VariablesGlobal(models.Model):
    name = models.CharField(unique=True, max_length=50, null=False)
    variable_value = models.CharField(null=True,max_length=3000)
    create_time = models.DateTimeField(auto_now_add=True, )
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tbl_global_variables"
        verbose_name = "全局变量表"
        ordering = ["id"]


class RunSuiteRecord(models.Model):
    suite_ids = models.JSONField()

    class Meta:
        db_table = "tbl_runsuite_record"


class ScheduleTrigger(models.Model):
     choices = [('1','按日期执行'),('2','间隔周期执行'),('3',"cron 定时器执行")]
     schedule_name = models.CharField(null=False,max_length=50)
     schedule_args = models.JSONField(null=False)
     schedule_type = models.CharField(choices=choices,max_length=10)
     schedule_time  = models.CharField(max_length=50,null=False)
     enable = models.BooleanField(null=False,default=False)
     create_time = models.DateTimeField(auto_now_add=True, )
     update_time = models.DateTimeField(auto_now=True)

     class Meta:
         db_table='tbl_schedule'
         verbose_name="定时任务表"
         ordering =["id"]

class ProjectConfig(models.Model):
    project_name = models.CharField(max_length=50,null=False,unique=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tbl_project_config'
        verbose_name = "项目配置表"
        ordering = ["id"]




