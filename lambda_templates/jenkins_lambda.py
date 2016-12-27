import yaml
import sys
import argparse
import jenkins
import constants
import exceptions
from xml.etree import ElementTree as et

class JenkinsLambda(object):

	def __init__(self, url, username, password):
		self.jenkins_server = jenkins.Jenkins(url, username, password)

	def set_default_value(self, config, parameter, default_value):
	   parameter_definitions = config.findall('.//parameterDefinitions/hudson.model.StringParameterDefinition')
	  
	   for node in parameter_definitions:
	      name = node.findall('.//name')
	      is_match=False
	      for e in name:
	         if (e.text == parameter):
	            is_match=True
	      if not is_match:
	         continue

	      for child in node.getiterator():
	         if(child.tag=='defaultValue'):
	            child.text = default_value

	def create_folder_name(self, job_name):
	   return ('%s' % (job_name))

	def does_job_exist(self, job_name):
	   print self.jenkins_server.get_job_info(job_name)
	   return (self.jenkins_server.get_job_info(job_name) is not None)

	def create_job(self, job_name):
	   full_folder_name = self.create_folder_name(job_name)
	   if (self.does_job_exist(full_folder_name)):
	      raise exceptions.JenkinsException ("Unable to create job: Folder %s already exists" % (full_folder_name))

	   print 'Creating folder %s' % (full_folder_name)
	   self.jenkins_server.create_job('%s' % (full_folder_name), constants.EMPTY_FOLDER_XML)

def throw_argument_error(parser, message, code=2):
   print "ERROR: %s" % (message)
   parser.print_help()
   sys.exit(code)

def validate_arguments(args):
   if args.command not in ['create', 'update', 'run']:
      throw_argument_error (parser, "Invalid command", constants.ARGPARSE_ERROR_INVALID_COMMAND)

def parse_args(args):
   parser = argparse.ArgumentParser(description="Create python lambda jobs in Jenkins")
   parser.add_argument('--configyaml', help='full path of the --configyaml')
   parser.add_argument('--jobname', help='name of the job')
   parser.add_argument('--parameters', help='job custom parameters')
   parser.add_argument('--folder', help='name of the folder')
   parser.add_argument('command', nargs='?', help='run,update,info')
   print(args)
   if len(args) < 2:
      throw_argument_error(parser, "Invalid arguments", constants.ARGPARSE_ERROR_INVALID_ARGUMENTS)

   return parser.parse_args(args)

def read_config(config_yaml):
   with open(config_yaml, 'r') as stream:
      try:
         config = yaml.load(stream)
      except yaml.YAMLError as exc:
         print "ERROR LOADING %s" % (config_yaml)
         print(exc)

   return config

def main():
   args = parse_args(sys.argv[1:])
   validate_arguments(args)
   config = read_config(args.configyaml)
   jenkins_lambda = JenkinsLambda (config["jenkins_url"], username=config["auth"]["username"], password=config["auth"]["password"])

   if args.command=='create':
      jenkins_lambda.create_job(args.jobname)

   if args.command=='run':
      print('Running job %s' % (args.jobname))
      job = server.get_job_config(args.jobname)
      server.build_job(args.jobname, json.loads(args.parameters))
      
   if args.command=='update':
      for job_config in job_configs:
      	 job = server.get_job_config(job_config["name"])
      	 tree = et.fromstring(job)
      	 print "Updating %s" % (job_config["name"])
      	 print job_config
      	 for parameter in job_config["parameters"]:
      	    set_default_value(tree, parameter["name"], parameter["value"])
            print et.tostring(tree, encoding='utf8', method='xml')
            quit()

if __name__ == '__main__':
   main()     
