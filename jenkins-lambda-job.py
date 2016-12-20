import yaml
import argparse
import jenkins
from xml.etree import ElementTree as et

def set_default_value(config, parameter, default_value):
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


parser = argparse.ArgumentParser(description="Create python lambda jobs in Jenkins")
parser.add_argument('--configyaml', help='full path of the --configyaml')
parser.add_argument('--jobname', help='name of the job')
parser.add_argument('--parameters', help='job custom parameters')
parser.add_argument('command', nargs='?', help='run,update')
args = parser.parse_args()
config={}
job_configs={}
username=""
password=""
url=""
with open(args.configyaml, 'r') as stream:
    try:
        config = yaml.load(stream)
        username=config["auth"]["username"]
        password=config["auth"]["password"]
        url=config["jenkins_url"]
        job_configs=config["jobs"]
    except yaml.YAMLError as exc:
        print(exc)
server = jenkins.Jenkins(url, username=username, password=password)
if args.command=='run':
   print('Running job %s' % (args.jobname))
   job = server.get_job_config(args.jobname)
   server.build_job(args.jobname, json.loads(args.parameters))
   quit()

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

print "Invalid option -- nothing to do"

