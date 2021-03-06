import requests
import urllib3
import json
from .models import TestSuite, TestCase, VariablesGlobal,TaskExcuteRecord,RunSuiteRecord
from .serializers import SerialTestSuite, SerializerTestCase,TaskExcuteSerializer,RunTestSuiteSerializer
from .request_util import RequestUtil
from django.forms.models import model_to_dict
urllib3.disable_warnings()
from mysite.function_plugin import hook_replace

def run_suites(suite_ids,taskid=None):
    """
    sync block run each test suite
    :param suite_ids:
    :return: None
    """
    if not taskid:
        for suite_id in suite_ids:
            run_suite(suite_id)
    else:

        for suite_id in suite_ids:
            run_suite(suite_id,taskid=taskid)

        # judge task status
        task_items = TaskExcuteRecord.objects.filter(taskid=taskid)
        status_list = [task_item.status for  task_item in task_items]
        inst = RunSuiteRecord.objects.filter(taskid=taskid).first()
        if status_list.count('0') == len(status_list):
            serial = RunTestSuiteSerializer(instance=inst,data={'status':'0'},partial=True)
        elif status_list.count('2') == len(status_list):
            serial = RunTestSuiteSerializer(instance=inst, data={'status': '2'},partial=True)
        else :
            serial = RunTestSuiteSerializer(instance=inst, data={'status':'1'},partial=True)
        if serial.is_valid():
            serial.save()



    # write  task record of taskid,suiteid ,caseid ,method ,url  ,response,error status ,runtime


def run_suite(suite_id,taskid=None):
    """
    :param suite_id:
    :return: None
    test case status enum: {"0":"全部未执行","1":"全部失败","2":"成功","3":"部分失败"}
    """
    # get one test suite
    inst = TestSuite.objects.filter(id=suite_id).first()
    serial = SerialTestSuite(instance=inst, many=False)
    data = serial.data
    # get one suite all cases
    cases_list = data.get("cases_list")
    caseIds = []
    for case in cases_list:
        case_id = case.get("id")
        caseIds.append(case_id)
        run_test_case(case_id)

    objs = TestCase.objects.filter(id__in=caseIds)
    status_all = [obj.status for obj in objs]
    # all fail
    if status_all.count('1') == len(status_all):
        TestSuite.objects.filter(id=suite_id).update(status='1')
    # all success
    elif status_all.count('2') == len(status_all):
        TestSuite.objects.filter(id=suite_id).update(status='2')
    # all not run
    elif status_all.count('0') == len(status_all):
        TestSuite.objects.filter(id=suite_id).update(status='0')
    # partial failed
    else:
        # status_all.count('1')>1 and status_all.count('1') <len(status_all)
        TestSuite.objects.filter(id=suite_id).update(status='3')
    if taskid:
        objs = TestCase.objects.filter(id__in=caseIds)
        # write suite_id,taskid, obj.data
        querysets = []
        for obj in objs :
            extra_kwarg = model_to_dict(obj)
            extra_kwarg["case_id"]=extra_kwarg.pop("id")
            task_obj= {"suite_id":suite_id,"taskid":taskid,**extra_kwarg}
            print(task_obj)
            querysets.append(task_obj)
        serial_task_execute = TaskExcuteSerializer(data= querysets,many=True)
        if serial_task_execute.is_valid(raise_exception=True):
            serial_task_execute.save()




def run_test_case(case_id):
    case_inst = TestCase.objects.filter(id=case_id).first()
    serial_test_case = SerializerTestCase(instance=case_inst, many=False)
    test_case_data = serial_test_case.data
    extract_data = test_case_data.get("extract")
    assert_express = test_case_data.get("assert_express")

    try:
        ret = execute_requests(case_id)
        response = ret.text
    except Exception as e:
        response = {"error": str(e)}
    if response:
        try:
            if not isinstance(response, dict):
                response = json.loads(response)
        except json.decoder.JSONDecodeError:
            pass
        serial_update = SerializerTestCase(instance=case_inst,
                                           partial=True, data={"response": response}, many=False)
        if serial_update.is_valid():
            serial_update.save()
        if extract_data:
            for name, path in extract_data.items():
                if isinstance(response, (dict, list, str)):
                    value = RequestUtil.jsonpath_extractor(path, response) or ''  # 没有提取到怎么办value为""
                    VariablesGlobal.objects.update_or_create(defaults={"variable_value": value}, name=name)
        if assert_express:
            assert_result = []
            for item in assert_express:
                extract_path = item.get("key")
                # todo type str true
                actual = RequestUtil.jsonpath_extractor(extract_path, response)
                actual = bool(actual) if actual == True or actual == False else actual
                v = item.get("value")
                # todo True
                expect = bool(v) if v == "true" or v == "false" else v

                flag = item.get("operator")
                if isinstance(expect, bool) or isinstance(actual, bool):
                    res = RequestUtil.assert_result(expect, actual)

                else:
                    res = RequestUtil.assert_result(expect=str(expect), actual=str(actual), flag=flag)
                # True bool
                if not res:
                    msg = str(actual) + " " + str(flag) + " " + str(expect) + " is " + str(res)

                    assert_result.append(msg)

            if len(assert_result) > 0:
                serial_test_case = SerializerTestCase(many=False, partial=True, instance=case_inst,
                                                      data={"error_msg": assert_result, "status": "1"})
            if len(assert_result) == 0 and response:
                serial_test_case = SerializerTestCase(many=False, partial=True, instance=case_inst,
                                                      data={"status": "2", "error_msg": []})
            if serial_test_case.is_valid():
                serial_test_case.save()
        else:
            serial = SerializerTestCase(many=False, partial=True, instance=case_inst,
                                        data={"status": "0", "error_msg": []})
            if serial.is_valid():
                serial.save()

    else:
        pass


def batch_run_test_case(case_ids: list):
    for case_id in case_ids:
        run_test_case(case_id)


def execute_requests(case_id):
    """
    send request according to method and mine-type
    :param case_id:
    :return: None
    get and delete method  execute priority is params first ,then form-data
    if both params and form-data ,use params to send request .
    :file upload api now we depend on s3 file storage : oss,minio,qiniuyun,fastdfs etc .
    we get bytes of s3 file object's content with  request.get(url).content method
    """
    instance = TestCase.objects.filter(id=case_id).first()
    case_serial = SerializerTestCase(instance=instance, many=False)
    serial_data = case_serial.data
    url = serial_data.get("url")
    method = serial_data.get("method")
    headers = serial_data.get("headers")
    params = serial_data.get("params")
    mine_type = serial_data.get("mine_type")
    body = serial_data.get("body")
    # todo  prepare url ,params ,headers ,body
    ret = None
    if url :
        # 准备url参数化和函数助手替换
        if RequestUtil.get_variable(url):
            url = prepare_dict_or_str(url)
            url = prepare_func(url)
        else:
            url =prepare_func(url)

    if headers:
        if RequestUtil.get_variable(headers):
            headers = prepare_dict_or_str(headers)
            headers=prepare_func(headers)
        else:
            headers =  prepare_func(headers)
    if method.upper() == "GET":

        ret = requests.request(method="get", url=url, headers=headers or {}, verify=False)

    elif method.upper() == "POST" or method.upper() == "PATCH" or method.upper() == "PUT":

        if mine_type == '2':  # multi-form-data
            data = {}
            file_urls = []
            for value in body:
                if value.get("keyType") == 'text':
                    k = value.get('key')
                    v = value.get("value")
                    data[k] = v
                if value.get('keyType') == 'file':
                    k = value.get("key")
                    file_list = value.get("fileList")
                    for file in file_list:
                        f_url = file.get("url")
                        file_urls.append((k, f_url))
            files = [(k, requests.get(v).content) for k, v in file_urls]
            if RequestUtil.get_variable(data):
                data = prepare_dict_or_str(data)
                data = prepare_func(data)
            else:
                data = prepare_func(data)
            ret = requests.request(method="post", url=url,
                                   data=data, files=files, headers=headers or {}, verify=False)
        elif mine_type == '3':  # form-data
            data = {}
            for value in body:
                for k, v in value.items():
                    data[k] = v
            # if exists  ${var} in post data body use substituted data
            if RequestUtil.get_variable(data):
                data = prepare_dict_or_str(data)
                data =prepare_func(data)
            else :
                data =prepare_func(data)
            ret = requests.request("post", url, data=data, headers=headers or {}, verify=False)
        elif mine_type == '4' or 4:  # json
            if RequestUtil.get_variable(body):

                body = prepare_dict_or_str(body)
                body = prepare_func(body)
            else :
                body = prepare_func(body)

            ret = requests.request("post", url, json=body, headers=headers or {}, verify=False)
        else:
            pass

    elif method.upper() == "DELETE":
        if params and mine_type == '1':

            # if RequestUtil.get_variable(url):
            #     url = prepare_dict_or_str(url)
            ret = requests.request(method="delete", url=url, verify=False, headers=headers or {})
        # delete form-data or json
        if mine_type in ['3', '4'] and not params:
            if mine_type == '3':

                data = {}
                for value in body:
                    k = value.get('key')
                    v = value.get("value")
                    data[k] = v

                if RequestUtil.get_variable(data):
                    data = prepare_dict_or_str(data)
                    data = prepare_func(data)
                else:
                    data = prepare_func(data)
                ret = requests.request("delete", url, data=data, headers=headers or {}, verify=False)

            if mine_type == '4':
                if RequestUtil.get_variable(body):
                    body = prepare_dict_or_str(body)
                    body = prepare_func(body)
                else:
                    body = prepare_func(body)
                ret = requests.request("delete", url, json=body, headers=headers or {}, verify=False)

        if mine_type in ['3', '4'] and params:
            # if RequestUtil.get_variable(url):
            #     url = prepare_dict_or_str(url)
            ret = requests.request(method="delete", url=url, verify=False, headers=headers)

    return ret


def prepare_dict_or_str(data):
    var_list = RequestUtil.get_variable(data)
    if var_list:
        objs = VariablesGlobal.objects.filter(name__in=var_list)
        queryset = objs.values("name", "variable_value")
        const_kwargs = {item.get("name"): item.get("variable_value") for item in queryset}
        if isinstance(data, dict):
            data = RequestUtil.substitute_variable(data, const_kwargs=const_kwargs)

        if isinstance(data, str):
            data = RequestUtil.replace_str(data, const_kwargs)
        return data


def prepare_func(data):
    if "${{" not in json.dumps(data):
       return data
    else:
        type = 1
        if isinstance(data, str):
            type = 0
        if isinstance(data, dict):
            type = 1
        serial = hook_replace(data, type)
    return serial