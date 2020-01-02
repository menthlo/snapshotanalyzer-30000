import boto3
import click

session = boto3.Session(profile_name='shotty')
ec2 = session.resource('ec2')

# filter ec2 instances by project
def filter_instances(project):
    instances = []
    if project:
        filters = [{'Name':'tag:Project','Values':[project]}]
        instances = ec2.instances.filter(Filters=filters)
    else:
        instances = ec2.instances.all()
    return instances

@click.group()
def instances():
    '''commands for instances'''

@instances.command('list')
@click.option('--project',default=None,
    help="only instances of project (tag:<project>)")
# list the instance with filter
def list_instances(project):
    "list ec2 instances"
    instances = filter_instances(project)
    for i in instances:
        #put the tags of the instance into a dict
        tags = {t['Key']:t['Value'] for t in i.tags or []}
        if i.state['Code'] == 16 or i.state['Code'] == 80:
            print(', '.join((
                i.id,
                i.instance_type,
                i.placement['AvailabilityZone'],
                i.state['Name'],
                str(i.private_ip_address),
                tags.get('Project','<no project>'))))
    return
#stop the filtered instances
@instances.command('stop')
@click.option('--project',default=None,
    help="stop the instance of project (tag:<project name>)")
def stop_instances(project):
    "stop ec2 instances"
    instances = filter_instances(project)
    for i in instances:
        print("stopping instance {0}".format(i.id))
        i.stop()
    return

#start the filtered instances
@instances.command('start')
@click.option('--project',default=None,
    help="start the instance of project (tag:<project name>)")
def start_instances(project):
    "star ec2 instances"
    instances = filter_instances(project)
    for i in instances:
        print("starting instance {0}".format(i.id))
        i.start()
    return

#terminate the filtered instances
@instances.command('terminate')
@click.option('--project',default=None,
    help="terminate the instance of project (tag:<project name>)")
def start_instances(project):
    "terminate ec2 instances"
    instances = filter_instances(project)
    for i in instances:
        print("terminating instance {0}".format(i.id))
        i.terminate(False)
    return

#lanuch specified count of instances
@instances.command('launch')
@click.option('--min',default=1,
    help="the minimum instances you want to launch")
@click.option('--max',default=5,
    help="the maximum instances you want to launch")

def launch_instances(min,max):
    "launch ec2 instances"

    instances = ec2.create_instances(
        MaxCount = max,
        MinCount = min,
        SubnetId = 'subnet-241a366e',
        LaunchTemplate = {
            'LaunchTemplateId':'lt-0c5a087717163cdaa',
            'Version':'$Latest'
        }
    )

    for i in instances:
        print("Launching instance {0}".format(i.id))
    return

if __name__ == "__main__":
    instances()
