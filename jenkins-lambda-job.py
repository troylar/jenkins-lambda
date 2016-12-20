import yaml
import argparse
import jenkins

parser = argparse.ArgumentParser(description="Create python lambda jobs in Jenkins")
parser.add_argument('--configyaml', help='full path of the --configyaml')
parser.add_argument('--jobname', help='name of the job')
parser.add_argument('--parameters', help='job custom parameters')
parser.add_argument('command', nargs='?', help='run,info,create')
args = parser.parse_args()
config={}
username=""
password=""
url=""
with open(args.configyaml, 'r') as stream:
    try:
        config = yaml.load(stream)
        username=config["auth"]["username"]
        password=config["auth"]["password"]
        url=config["jenkins_url"]
    except yaml.YAMLError as exc:
        print(exc)
server = jenkins.Jenkins(url, username=username, password=password)
if args.command=='run':
   print('Running job %s' % (args.jobname))
   job = server.get_job_config(args.jobname)
   server.build_job(args.jobname, json.loads(args.parameters))
   quit()

if args.command=='info':
   job = server.get_job_config(args.jobname)
   print(job)
   quit()

print "Invalid option -- nothing to do"

#plugins = server.get_plugins()
#for plugin in plugins.keys():
#   info = server.get_plugin_info(plugin[0])
#   print info 
