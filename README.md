# snapshotanalyzer-30000
demo project to manage all EC2 snapshots


# using
'pipenv run python shotty/shotty.py <command> <subcommand> <--project=PROJECT>'

<command> could be instances volumes snapshots
<subcommand> could be list start stop and terminate

<--project > is dependent

'pipenv run python shotty/shotty.py <command> <subcommand> <--min> <--max>'

<command> could be instances
<subcommand> could be launch
--min default 1
--max default 5
