#!/usr/bin/python
#
# web-backup.py
#
# This script iterates through a config file of web services/apps
# that needs backing up, using the workflow:
#
#   # mkdir /tmp/webservice
#   # service stop webservice
#   # dbdump db_name /tmp/webservice/db_name.sql
#   # rsync -a /var/www/webservice /tmp/webservice/web-root
#   # tar cjpf /backup/webservice/webservice-date.tar.bz2 /tmp/webservice
#

# Imports
import sys
import time
from configobj import ConfigObj
import argparse
import logging

# Read arguments
parser = argparse.ArgumentParser()
parser.add_argument('--config',
                    help='Config file, defaults to "./web-backup.cfg"',
                    type=argparse.FileType('r'),
                    default='web-backup.cfg'
                    )

# Check for config file
try:
    args = parser.parse_args()
except argparse.ArgumentError:
    parser.print_help()
    sys.exit(1)


# Read configuraion file
config = ConfigObj(args.config)

# General settings
generalSettings = config['general']

# Backup jobs
backupJobs = config['jobs']


# Variables
backupDir = generalSettings['backup_dir']
logDir = generalSettings['log_dir']
logFile = generalSettings['log_dir'] + '/web-backup.log'
if generalSettings['log_level'] == 'debug':
    logLevel = logging.DEBUG
else:
    logLevel = logging.WARNING
errors = []

# Setup logging
logging.basicConfig(
    filename=logFile,
    format='%(asctime)s:%(levelname)s:%(message)s',
    datefmt='%Y-%m-%d %T',
    level=logLevel
    )

logging.info('Starting backup run')


# Classes

class web-backup:
    def __init__(self, name, stopCmd, startCmd, dumpCmd, webRoot):
        self.name = name
        self.stopCmd = stopCmd
        self.startCmd = startCmd
        self.dumpCmd = dumpCmd
        self.webRoot = webRoot

        # Sanity check

        return()

    def run_backup(self):
        timeStamp = time.strftime("%Y-%m-%d_%H-%M-%S")
        return()


# Main

for job in backupJobs.keys():

    # Set variables
    name = job

    jobParams = {
        'service_stop_command': '',
        'service_start_command': '',
        'web_root': '',
        'db_dump_command': '',
        }

    for param, val in jobParams.iteritems():
        ẗry:
            jobParams[param] = backupJobs[job][param]
        except KeyError:
            logging.info('Setting "' + param + '" not set')
            pass

    # Run backup
    backup = web-backup(
        name,
        service_stop_command,
        service_start_command,
        db_dump_command,
        web_root
        )
    status = backup.run_backup()

    if status[0] != 0:
        print('Backup failed! Job: "' + name + '"')
        print('Error: ' + status[1])
        # Add error to errors list
        errors.append('Job : "' + name + '"' + ' Error: ' + status[1])
    else:
        print('Job: "' + name + '" successful')


# Check for errors and exit
if errors:
    print('Finished with errors')
    for error in errors:
        print(error)
    print('\n\n')
    sys.exit(1)
else:
    print('Finished without errors\n\n')
    sys.exit(0)
