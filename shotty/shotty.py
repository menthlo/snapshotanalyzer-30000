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
        tags = {t['Key']:t['Value'] for t in i.tags or []}
        print(', '.join((
            i.id,
            i.instance_type,
            i.placement['AvailabilityZone'],
            i.state['Name'],
            i.public_dns_name,
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

if __name__ == "__main__":
    instances()
