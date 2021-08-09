from django.urls import path, re_path
from .views import ( UserView, LoginView,TestSuiteView,UserInfo,TaskExecuteView)

from . import views

urlpatterns = [
    path('role/info', views.RoleInfoView.as_view({'get': 'list', 'post': 'create'})),
    path('task/record',TaskExecuteView.as_view({'get':'list'})),
    path('task/record/<str:taskid>',TaskExecuteView.as_view({'get':'get_task_items'})),
    path('regist/', UserView.as_view({'post': 'create'})
         ),
    path('userInfo/', UserInfo.as_view({ 'patch': 'change_password','get':'list'})
         ),
    path('login/', LoginView.as_view({'post': 'create'})
         ),
    path('trigger', views.trigger_view,
         ),
    path('testcase', views.TestCaseView.as_view({"get": 'list', 'post': 'create'})),
    path('testcase/<int:id>', views.TestCaseView.as_view({'get': 'retrieve',
                                                          'patch': 'partial_update', 'delete': 'destroy'})),
    path('variables', views.VariableView.as_view({"get": 'list', 'post': 'create'})),
    path('variables/<int:id>', views.VariableView.as_view({'get': 'retrieve',
                                                           'delete': 'destroy','patch': 'partial_update'})),
    path('variables/batch',views.BatchVariableView.as_view({'delete':'batch_delete'})),

    path('testsuite', views.TestSuiteView.as_view({"get": 'list', 'post': 'create'})),
    path('testsuite/<int:id>', views.TestSuiteView.as_view({'get': 'retrieve',
                                                          'patch': 'partial_update', 'delete': 'destroy'})),
    path('runsuite', views.RunTestSuite.as_view({'post': 'create','get':'list'})),
    path('runsuite/<int:id>', views.RunTestSuite.as_view({'delete': 'destroy'})),
    path('variable/check', views.VariableCheck.as_view({'get': 'list'})),
    path('testsuite/batch',views.BatchTestSuiteView.as_view({'delete':'batch_delete'})),
    path('testcase/batch',views.BatchTestCaseView.as_view({'delete':'batch_delete','post':'batch_run'})),
    path('testcase/status',views.ResultStatusView.as_view({'get':'get_status'})),
    path('testcase/status/detail',views.FailedCaseView.as_view({'get':'get_status_detail'})),

    path('schedule',views.ScheduleView.as_view({'get':'list','post':'create'})),
    path('schedule/<int:id>',views.ScheduleView.as_view(
        {'get': 'retrieve',
         'patch': 'patch', 'delete': 'destroy'}
    )),
    path('projects',views.ProejctConfigView.as_view({'get':'list','post':'create'})),
    path('projects/<int:id>', views.ProejctConfigView.as_view({'delete': 'destroy'})),

]


