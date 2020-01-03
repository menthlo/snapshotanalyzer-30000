import boto3
import click

session = boto3.Session(profile_name='shotty')
ec2 = session.resource('ec2')

# filter ec2 instances by project
def filter_instances(project):
    instances = []
    if project:
        filters = [
            {'Name':'tag:Project','Values':[project]},
            {'Name':'instance-state-code','Values':['0','16','32','64','80']}
        ]
        instances = ec2.instances.filter(Filters=filters)
    else:
        instances = ec2.instances.all()
    return instances

# function of removal of a specified snapshot
def remove_snapshot(id):
    client = boto3.client('ec2')
    print('deleting the snapshot {0}'.format(id))
    client.delete_snapshot(SnapshotId=id)

@click.group('cli')
def cli():
    ''' commands for click'''

@cli.group('instances')
def instances():
    '''commands for instances'''

@cli.group('volumes')
def volumes():
    ''' commands for volumes'''

@cli.group('snapshots')
def snapshots():
    ''' commands for snapshots'''

# list the filtered instances snapshots of volumes
@snapshots.command('list')
@click.option('--project',default=None,
    help="only snapshots of project (tag:<project>)")
# list the instance with filter
def list_snapshots(project):
    "list ec2 snapshots"
    instances = filter_instances(project)

    for i in instances:
        for v in i.volumes.all():
            for s in v.snapshots.all():
                print(', '.join((
                    s.id,
                    v.id,
                    i.id,
                    s.state,
                    s.progress,
                    s.start_time.strftime('%c')
                )))
    return


# list the filtered instances volumes
@volumes.command('list')
@click.option('--project',default=None,
    help="only volumes of project (tag:<project>)")
# list the instance with filter
def list_volumes(project):
    "list ec2 volumes"
    instances = filter_instances(project)

    for i in instances:
        for v in i.volumes.all():
            print(', '.join((
                i.id,
                v.id,
                v.state,
                str(v.size) + "GiB",
                v.encrypted and "Encrypted" or "NotEncrypted")))
    return

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
@click.option('--delsnappy',default='yes',
    help="remove related snapshots of the instances,yes or no")

def terminate_instances(project,delsnappy):
    "terminate ec2 instances"
    instances = filter_instances(project)
    for i in instances:
        if delsnappy == 'yes':
            for v in i.volumes.all():
                for s in v.snapshots.all():
                    remove_snapshot(s.id)
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

#create snapshots of all the volumes of each instance
@instances.command('snapshots')
@click.option('--project',default=None,
    help="create snapshots of the instance filtered by project (tag:<project name>)")


def create_snapshots(project):
    "create snapshots of  EC2 instances"
    instances = filter_instances(project)

    for i in instances:
        for v in i.volumes.all():
            v.create_snapshot(Description='snapshots created from analyzer 30000')

    return





if __name__ == "__main__":
    cli()
