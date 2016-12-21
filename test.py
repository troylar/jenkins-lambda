import unittest
import jenkins_lambda
import constants
import jenkins
from mock import MagicMock, patch
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

   def test_valid_arguments (self):
      parser = jenkins_lambda.parse_args(['badcommand'])
      self.assertEqual(cm.exception.code, constants.ARGPARSE_ERROR_INVALID_ARGUMENTS)

class JenkinsTestCase(unittest.TestCase):

   @patch.object(jenkins.Jenkins, 'create_job')
   def test_create_job_creates_folder(self, create_job_mock):
      parser = jenkins_lambda.parse_args(['create', '--jobname', 'test_job_name'])
      jenkins_mock = jenkins.Jenkins ('url', 'username', 'password')
      create_job_mock.assert_called_with('test_job_name')

if __name__ == '__main__':
   unittest.main()
