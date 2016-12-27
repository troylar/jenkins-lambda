import unittest
import jenkins
from mock import MagicMock, patch
import sys
import os
import exceptions
import json
sys.path.insert(0, os.path.abspath('..'))

from lambda_templates import constants
from lambda_templates import exceptions
from lambda_templates import jenkins_lambda
from lambda_templates.jenkins_lambda import JenkinsLambda

class CommandLineTestCase(unittest.TestCase):

   def test_no_arguments_shows_help(self):
      with self.assertRaises(SystemExit) as cm:
         parser = jenkins_lambda.parse_args([])
 
   def test_create_with_no_job_name(self):
      with self.assertRaises(SystemExit) as cm:
         parser = jenkins_lambda.parse_args(['create'])
      self.assertEqual(cm.exception.code, constants.ARGPARSE_ERROR_INVALID_ARGUMENTS)

   def test_single_argument_throws_error (self):
      with self.assertRaises(SystemExit) as cm:
         parser = jenkins_lambda.parse_args(['badcommand'])
      self.assertEqual(cm.exception.code, constants.ARGPARSE_ERROR_INVALID_ARGUMENTS)

#   def test_valid_arguments (self):
#      parser = jenkins_lambda.parse_args(['badcommand'])

class JenkinsTestCase(unittest.TestCase):

   @patch.object(jenkins.Jenkins, 'jenkins_open')
   @patch.object(jenkins.Jenkins, 'create_job')
   @patch.object(jenkins.Jenkins, 'get_job_info')
   def test_create_job_creates_folder(self, get_job_info_mock, create_job_mock, jenkins_mock):
      jenkins_mock.return_value=None
      get_job_info_mock.return_value=None
      jenkins_lambda = JenkinsLambda("a","b","c")
      jenkins_lambda.create_job("test_job_name")
      create_job_mock.assert_called_with("test_job_name", constants.EMPTY_FOLDER_XML)

   @patch.object(jenkins.Jenkins, 'jenkins_open')
   @patch.object(jenkins.Jenkins, 'get_job_info')
   def test_gracefully_handle_error_if_folder_already_exist(self, get_job_info_mock, jenkins_mock):
      jenkins_mock.return_value=None
      get_job_info_mock.return_value=json.loads('{"job": "test"}')
      jenkins_lambda = JenkinsLambda("a","b","c")
      with self.assertRaises(exceptions.JenkinsException) as context:
         jenkins_lambda.create_job("test_job_name")
      print context.exception
      self.assertTrue("exists" not in context.exception)

if __name__ == '__main__':
   unittest.main()
