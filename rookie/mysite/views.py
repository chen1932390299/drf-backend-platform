import uuid
from django.core.cache import cache
from rest_framework import filters, exceptions
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import  (UserSerializer, SerializerTestCase,ProjectSerializer,
    SerialVaribales, SerialTestSuite,RunTestSuiteSerializer,ScheduleSerializer)
from .models import (User, TestCase, VariablesGlobal,ProjectConfig,
                     TestSuite, RunSuiteRecord,ScheduleTrigger)
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .runtest import batch_run_test_case
from utils.viewsets import CustomViewSet
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser, FormParser
from rest_framework import filters
from asgiref.sync import sync_to_async
from .runtest import run_suites
from utils.custom_response import CustomResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ViewSetMixin
from utils.authenticate import CustomerAuthentication
from utils.permission import IsOwnerCheck
from rest_framework.versioning import URLPathVersioning
from django.http.response import HttpResponse
from django.middleware.csrf import CsrfViewMiddleware
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.utils.decorators import method_decorator
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.generics import GenericAPIView, ListAPIView, CreateAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.viewsets import ModelViewSet
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_job
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.date import DateTrigger

scheduler = BackgroundScheduler()  # 创建一个调度器对象
scheduler.add_jobstore(DjangoJobStore(), "default")  # 添加一个作业

if not scheduler.state:
    scheduler.start()

def test(*user_args):
     import  time
     print(user_args)
@api_view(http_method_names=['GET', 'POST'])
def trigger_view(request):
    if request.method == 'GET':
        print(request.data)
        return Response({"message": "Got some data GET !", "data": request.data})
    if request.method == 'POST':
        print(request.data)


        # scheduler = BackgroundScheduler()  # 创建一个调度器对象
        # scheduler.add_jobstore(DjangoJobStore(), "default")  # 添加一个作业
        try:

            scheduler.remove_job(job_id='15')
            scheduler.remove_job(job_id='24')
            scheduler.remove_job(job_id='12')
            scheduler.remove_job(job_id='hello world')
            ids= scheduler.get_jobs()
            print(ids)
            print("开始任务")
        except Exception as e:
            print(e)
            # scheduler.shutdown()

        return Response({"message": "Got some data POST!", "data": request.data})


class ScheduleView(CustomViewSet):
   lookup_field = 'id'
   queryset = ScheduleTrigger.objects.all()
   serializer_class = ScheduleSerializer
   parser_classes =  [JSONParser, FormParser]

   def destroy(self, request, *args, **kwargs):
       instance = self.get_object()
       job_id = str(instance.id)
       if scheduler.get_job(job_id=job_id) :
           scheduler.remove_job(job_id=job_id)
       self.perform_destroy(instance)
       return CustomResponse(data=[],status=200,msg="删除ok",success=True)


   def create(self, request, *args, **kwargs):
       """  cron tigger need rewrite ,default */10"""
       serializer = self.get_serializer(data=request.data)
       serializer.is_valid(raise_exception=True)
       self.perform_create(serializer)
       try:

           job_id =serializer.data.get('id')
           if serializer.data.get("enable"):
               if serializer.data.get('schedule_type') == '1':
                   scheduler.add_job(test,
                                     trigger=DateTrigger(run_date=serializer.data.get('schedule_time')),
                                     id=str(job_id),
                                     max_instances=1, replace_existing=True, args=serializer.data.get('schedule_args'))
               if serializer.data.get('schedule_type') == '2':
                   scheduler.add_job(test,
                                     trigger=IntervalTrigger(seconds=int(serializer.data.get('schedule_time'))),
                                     id=str(job_id),
                                     max_instances=1, replace_existing=True, args=serializer.data.get('schedule_args'))

               if serializer.data.get('schedule_type') == '3':
                    scheduler.add_job(test,
                                 trigger=CronTrigger(second="*/10"),
                                 id=str(job_id),
                                 max_instances=1, replace_existing=True, args=serializer.data.get('schedule_args'))
               register_job(scheduler)


       except Exception:
           pass
       headers = self.get_success_headers(serializer.data)
       return CustomResponse(data=serializer.data, code=200,
                             msg='ok', success=True,headers=headers)



   def patch(self, request, *args, **kwargs):
       """  cron tigger need rewrite ,default */10"""
       instance = self.get_object()
       job_id =  instance.id
       enable = request.data.get("enable")
       if scheduler.get_job(job_id=str(job_id)):
           if not enable:
                scheduler.pause_job(job_id=str(job_id))
           if enable:
               scheduler.resume_job(job_id=str(job_id))
       else:
           if enable:
               if instance.schedule_type =='1':
                   scheduler.add_job(test,
                                     trigger=DateTrigger(run_date=instance.schedule_time),
                                     id=str(job_id),
                                     max_instances=1, replace_existing=True, args=instance.schedule_args)
               if instance.schedule_type == '2':
                   scheduler.add_job(test,
                                     trigger=IntervalTrigger(seconds=int(instance.schedule_time)),
                                     id=str(job_id),
                                     max_instances=1, replace_existing=True, args=instance.schedule_args)
               if instance.schedule_type == '3':

                   scheduler.add_job(test,
                                 trigger=CronTrigger(second="*/10"),
                                 id=str(job_id),
                                 max_instances=1, replace_existing=True, args=instance.schedule_args)
               register_job(scheduler)


       kwargs['partial'] = True
       response =  self.update(request, *args, **kwargs)
       return CustomResponse(data=response.data, code=200,
                             msg='ok', success=True)


class TestCaseView(CustomViewSet):
    def get_queryset(self):
        queryset = TestCase.objects.all()
        status = self.request.query_params.get('status','')
        project_id= self.request.query_params.get('project_id','')
        if status or project_id:
            if status and not project_id:
                queryset = queryset.filter(status=status)
            if not status and project_id:
                queryset = queryset.filter(project_id=project_id)
            if status and project_id:
                queryset = queryset.filter(project_id=project_id,status=status)
        return queryset

    lookup_field = 'id'
    queryset =get_queryset
    serializer_class = SerializerTestCase
    parser_classes = [JSONParser, FormParser]
    filter_backends = [DjangoFilterBackend]  # filters.SearchFilter
    filterset_fields = ['project_id','status']




class ResultStatusView(CustomViewSet):
    lookup_field = 'id'
    queryset = TestCase.objects.all()
    serializer_class = SerializerTestCase
    parser_classes = [JSONParser, FormParser]
    project_id = openapi.Parameter(name='project_id', in_=openapi.IN_QUERY, description="project_id",
                                    type=openapi.TYPE_STRING)
    @swagger_auto_schema(method='get', manual_parameters=[project_id])
    @action(methods=['get'], detail=False)
    def get_status(self, request, *args, **kwargs):
        project_id = request.query_params.get('project_id', '')
        if not project_id:
            query_set = self.get_queryset()
        else: query_set =self.get_queryset().filter(project_id=project_id)
        serial = SerializerTestCase(many=True, instance=query_set)
        serial_data = serial.data
        if not serial_data:
            return CustomResponse(data=[], msg="not found data", code=200, success=False)
        success_count = len(list(filter(lambda item: item.get("status") == '2', serial_data)))
        failed_count = len(list(filter(lambda item: item.get("status") == '1', serial_data)))
        undefined_count = len(list(filter(lambda item: item.get("status") == '0', serial_data)))
        data = {
            "success": success_count,
            "false": failed_count,
            "undefined": undefined_count
        }
        return CustomResponse(data=data, msg="ok", code=200, success=True)


class FailedCaseView(CustomViewSet):
    lookup_field = 'id'
    # pagination_class = [ListPagination]
    queryset = TestCase.objects.all()
    serializer_class = SerializerTestCase
    parser_classes = [JSONParser, FormParser]
    status = openapi.Parameter(name='status', in_=openapi.IN_QUERY, description="case status",
                                    type=openapi.TYPE_STRING)
    project_id = openapi.Parameter(name='project_id', in_=openapi.IN_QUERY, description="project_id",
                                    type=openapi.TYPE_STRING)
    @swagger_auto_schema(method='get', manual_parameters=[status,project_id])
    @action(methods=['get'], detail=False)
    def get_status_detail(self, request,*args,**kwargs):
        status = request.query_params.get('status', '')
        project_id = request.query_params.get('project_id', '')
        if not status and status not in ['0', '1', '2']:
            return CustomResponse(data=[], success=False,
                                  code=400, msg="请求参数错误: status must be in ['0','1','2']")
        inst = self.get_queryset().filter(status=status)
        if project_id:
            inst = self.get_queryset().filter(status=status,project_id=project_id)
        queryset = self.filter_queryset(inst)
        page = self.paginate_queryset(queryset)
        response =None
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response =  self.get_paginated_response(serializer.data)
        page_param={'page':response.data.get('page'),'page_size':response.data.get('page_size')
            ,'totals':response.data.get('totals')}
        data = [{"id": item.get('id', ''), "name": item.get("case_name", ''),
                 "response": item.get('response', ''), "error_msg": item.get('error_msg', '')}
                for item in response.data.get('data','')]
        return CustomResponse(data={'data':data,**page_param}, code=200, msg='ok', success=True)


def sync_run_cases(case_ids: list):
    """同步阻塞执行用例任务"""
    batch_run_test_case(case_ids)


class BatchTestCaseView(CustomViewSet):
    """  batch run or delete test case """
    lookup_field = 'id'
    queryset = TestCase.objects.all()
    serializer_class = SerializerTestCase
    parser_classes = [JSONParser, FormParser]

    query_param = openapi.Parameter(name='case_ids', in_=openapi.IN_QUERY, description="用例id",
                                    type=openapi.TYPE_STRING)
    body = openapi.Parameter(name="case_ids", in_=openapi.IN_BODY, description='case_ids'
                             , type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_INTEGER))

    @swagger_auto_schema(method='delete', manual_parameters=[query_param])
    @action(methods=['delete'], detail=False)
    def batch_delete(self, request, *args, **kwargs):
        case_ids_string = request.query_params.get('case_ids', None)
        if not case_ids_string:
            return CustomResponse(data=[], msg="请选择case_id,suite_id不能为空", success=False, code=400)
        case_ids = case_ids_string.split(',')
        self.get_queryset().filter(id__in=case_ids).delete()
        return CustomResponse(data=[], msg='删除成功!', code=200, success=True)

    @swagger_auto_schema(method='post',
                         request_body=openapi.Schema(
                             type=openapi.TYPE_OBJECT,
                             required=['case_ids'],

                             properties={'case_ids': openapi.Schema(type=openapi.TYPE_ARRAY,
                                                                    items=openapi.Schema(type=openapi.TYPE_INTEGER))}
                         ),
                         operation_description='case_ids'

                         )
    @action(methods=['post'], detail=False)
    def batch_run(self, request):
        case_ids = request.data.get('case_ids', None)
        if not case_ids:
            return CustomResponse(data=[], msg="请选择case_id,case_id不能为空", success=False, code=400)

        async_run_cases = sync_to_async(sync_run_cases(case_ids)
                                        , thread_sensitive=True)
        return CustomResponse(data=[], msg='任务提交ok!', code=200, success=True)






class BatchFilterVariable(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        """ 重写过滤器...."""
        params = request.query_params
        names = params.dict().get("name", '')
        name_list = names.split(" ") or []
        return queryset.filter(name__in=name_list)


class VariableView(CustomViewSet):
    lookup_field = 'id'
    parser_classes = [JSONParser, FormParser]
    serializer_class = SerialVaribales
    queryset = VariablesGlobal.objects.all()


class BatchVariableView(CustomViewSet):
    lookup_field = 'id'
    parser_classes = [JSONParser, FormParser]
    serializer_class = SerialVaribales
    queryset = VariablesGlobal.objects.all()
    query_param = openapi.Parameter(name='variable_ids', in_=openapi.IN_QUERY, description="变量id",
                                    type=openapi.TYPE_STRING)

    @swagger_auto_schema(method='delete', manual_parameters=[query_param])
    @action(methods=['delete'], detail=False, )
    def batch_delete(self, request):
        variable_ids_string = request.query_params.get('variable_ids', None)
        if not variable_ids_string:
            return CustomResponse(data=[], msg="请选择variable,variable_id不能为空", success=False, code=400)
        variable_ids = variable_ids_string.split(',')
        self.get_queryset().filter(id__in=variable_ids).delete()
        return CustomResponse(data=[], msg='删除成功!', code=200, success=True)


class TestSuiteView(CustomViewSet):


    lookup_field = 'id'
    parser_classes = [JSONParser, FormParser]
    serializer_class = SerialTestSuite
    queryset =TestSuite.objects.all()
    filter_backends = [filters.SearchFilter]  # filters.SearchFilter
    search_fields = ['suite_name']




class BatchTestSuiteView(CustomViewSet):
    """
    custom batch delete or single delete with suite_ids
    :doc 一个用户自定义swagger参数的接口演示,不需要定义模型model和序列化器serializer
   penapi.TYPE Includes:
        TYPE_OBJECT = "object"  #:
        TYPE_STRING = "string"  #:
        TYPE_NUMBER = "number"  #:
        TYPE_INTEGER = "integer"  #:
        TYPE_BOOLEAN = "boolean"  #:
        TYPE_ARRAY = "array"  #:
        TYPE_FILE = "file"  #:
    in_ includes:
        IN_BODY = 'body'  #:
        IN_PATH = 'path'  #:
        IN_QUERY = 'query'  #:
        IN_FORM = 'formData'  #:
        IN_HEADER = 'header'  #:
    with swagger_auto_schema:
    :param str name: parameter name
    :param str in_: parameter location
    :param str description: parameter description
    :param bool required: whether the parameter is required for the operation
    :param schema: required if `in_` is ``body``
    :type schema: Schema or SchemaRef
    :param str type: parameter type; required if `in_` is not ``body``; must not be ``object``
    :param str format: value format, see OpenAPI spec
    :param list enum: restrict possible values
    :param str pattern: pattern if type is ``string``
    :param .Items items: only valid if `type` is ``array``
    :param default: default value if the parameter is not provided; must conform to parameter type
    """
    lookup_field = 'id'
    parser_classes = [JSONParser, FormParser]
    serializer_class = SerialTestSuite
    queryset = TestSuite.objects.all()
    query_param = openapi.Parameter(name='suite_ids', in_=openapi.IN_QUERY, description="套件id",
                                    type=openapi.TYPE_STRING)

    @swagger_auto_schema(method='delete', manual_parameters=[query_param])
    @action(methods=['delete'], detail=False, )
    def batch_delete(self, request, *args, **kwargs):
        suite_ids_string = request.query_params.get('suite_ids', None)
        if not suite_ids_string:
            return CustomResponse(data=[], msg="请选择suite_id,suite_id不能为空", success=False, code=400)
        suite_ids = suite_ids_string.split(',')

        self.get_queryset().filter(id__in=suite_ids).delete()
        return CustomResponse(data=[], msg='删除成功!', code=200, success=True)


class LoginView(CustomViewSet):
    parser_classes = [JSONParser, FormParser]
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = User.objects.filter(username=username).first()
        if not user:
            raise exceptions.ValidationError(detail='username错误')
        if not user.check_pwd(password):
            raise exceptions.ValidationError(detail='密码错误')
        key = uuid.uuid1().hex
        cache.set(key, user.id, 120)
        serial = UserSerializer(instance=user)
        return CustomResponse(data={'token': key, **serial.data}, code=200,
                              msg='ok', success=True)


class UserView(CustomViewSet):
    parser_classes = [JSONParser, FormParser]
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):

        username = request.data.get('username')

        users = User.objects.filter(username=username)

        if not users:
            serial = UserSerializer(data=request.data)
            if serial.is_valid():
                serial.save()
                return CustomResponse(data=serial.data, code=200, msg='ok', success=True)
            else:
                return CustomResponse(data=serial.errors, code=400, msg='', success=False)
        else:
            return CustomResponse(data={}, code=400, msg='用户已存在', success=False)



def sync_function(suite_ids):
    run_suites(suite_ids)


class RunTestSuite(CustomViewSet):
    lookup_field = 'id'
    parser_classes = [JSONParser]
    serializer_class = RunTestSuiteSerializer
    queryset = RunSuiteRecord.objects.all()

    def create(self, request, *args, **kwargs):
        serial = RunTestSuiteSerializer(data=request.data)
        if serial.is_valid():
            serial.save()
            data = serial.data
            async_task = sync_to_async(sync_function(data.get("suite_ids"))
                                       , thread_sensitive=True)
            return CustomResponse(data=data, code=200,
                                  msg='提交任务ok', success=True)
        else:
            return CustomResponse(data=serial.errors,
                                  code=400, msg='创建失败', success=False)


class VariableCheck(CustomViewSet):
    lookup_field = 'id'
    parser_classes = [JSONParser, FormParser]
    serializer_class = SerialVaribales
    queryset = VariablesGlobal.objects.all()
    filter_backends = [BatchFilterVariable]  # filters.SearchFilter
    filterset_fields = ['name']

    def list(self, request, *args, **kwargs):
        params = request.query_params
        names = params.dict().get("name", '')
        name_list = names.split(" ") or []
        objs = VariablesGlobal.objects.filter(name__in=name_list)
        if objs:
            arr = [obj.name for obj in objs]
            return CustomResponse(data=[], code=400, msg=arr, success=False)
        else:
            return CustomResponse(data=[], code=200, msg="重复检验通过", success=True)



class  ProejctConfigView(CustomViewSet):

    lookup_field = 'id'
    serializer_class = ProjectSerializer
    queryset = ProjectConfig.objects.all()
    parser_classes = [JSONParser, FormParser]

    filter_backends = [filters.SearchFilter]  # filters.SearchFilter
    search_fields = ['project_name']


