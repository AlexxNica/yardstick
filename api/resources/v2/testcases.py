import logging
import errno
import os

from api import ApiResource
from yardstick.common.utils import result_handler
from yardstick.common import constants as consts
from yardstick.benchmark.core import Param
from yardstick.benchmark.core.testcase import Testcase

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)


class V2Testcases(ApiResource):

    def get(self):
        param = Param({})
        testcase_list = Testcase().list_all(param)
        return result_handler(consts.API_SUCCESS, testcase_list)

    def post(self):
        return self._dispatch_post()

    def upload_case(self, args):
        try:
            upload_file = args['file']
        except KeyError:
            return result_handler(consts.API_ERROR, 'file must be provided')

        case_name = os.path.join(consts.TESTCASE_DIR, upload_file.filename)

        LOG.info('save case file')
        upload_file.save(case_name)

        return result_handler(consts.API_SUCCESS, {'testcase': upload_file.filename})


class V2Testcase(ApiResource):

    def get(self, case_name):
        case_path = os.path.join(consts.TESTCASE_DIR, '{}.yaml'.format(case_name))

        try:
            with open(case_path) as f:
                data = f.read()
        except IOError as e:
            if e.errno == errno.ENOENT:
                return result_handler(consts.API_ERROR, 'case does not exist')

        return result_handler(consts.API_SUCCESS, {'testcase': data})

    def delete(self, case_name):
        case_path = os.path.join(consts.TESTCASE_DIR, '{}.yaml'.format(case_name))

        try:
            os.remove(case_path)
        except IOError as e:
            if e.errno == errno.ENOENT:
                return result_handler(consts.API_ERROR, 'case does not exist')

        return result_handler(consts.API_SUCCESS, {'testcase': case_name})
