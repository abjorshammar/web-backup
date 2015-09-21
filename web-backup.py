#!/usr/bin/python
#
# -*- coding: utf-8 -*-
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
import os
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

print('\nWeb Backup started!\n')

# Read configuraion file
config = ConfigObj(args.config)

# General settings
generalSettings = config['general']

# Backup jobs
backupJobs = config['jobs']


# Variables
backupDir = generalSettings['backup_dir']
tempDir = generalSettings['temp_dir']
logDir = generalSettings['log_dir']
logFile = generalSettings['log_dir'] + '/web-backup.log'
if generalSettings['log_level'] == 'debug':
    logLevel = logging.DEBUG
elif generalSettings['log_level'] == 'warning':
    logLevel = logging.WARNING
else:
    logLevel = logging.INFO

errors = []

# Check log dir
if not os.path.exists(logDir):
    try:
        os.makedirs(logDir)
    except OSError:
        print('Unable to create "' + logDir + '"!\n')
        sys.exit(1)


# Setup logging
logging.basicConfig(
    filename=logFile,
    format='%(asctime)s:%(levelname)s:%(message)s',
    datefmt='%Y-%m-%d %T',
    level=logLevel,
    )

logging.info('Starting backup run')
logging.debug('Running with settings:')
logging.debug('backupDir: ' + backupDir)
logging.debug('tempDir:' + tempDir)
logging.debug('logDir: ' + logDir)
logging.debug('logFile: ' + logFile)
logging.debug('logLevel: ' + str(logLevel))


# Functions

def checkDirectory(directory):
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
            logging.debug('Created "' + directory + '"')
            return 0
        except OSError:
            logging.critical('Unable to create "' + directory + '"!')
            return 1
    else:
        logging.debug('Directory "' + directory + '" already exists')
        return 0


# Classes

class webBackup:
    def __init__(self, name, stopCmd, startCmd, dumpCmd, webRoot, extraDirs):
        self.name = name
        self.stopCmd = stopCmd
        self.startCmd = startCmd
        self.dumpCmd = dumpCmd
        self.webRoot = webRoot
        self.extraDirs = extraDirs

        # Sanity check

        # Debug log settings
        logging.debug('Backup job name: ' + self.name)
        logging.debug('Stop command: ' + self.stopCmd)
        logging.debug('Start command: ' + self.startCmd)
        logging.debug('DB dump command: ' + self.dumpCmd)
        logging.debug('Web root dir: ' + self.webRoot)
        logging.debug('Extra dirs: ' + self.extraDirs)

        return

    def run_backup(self):
        timeStamp = time.strftime("%Y-%m-%d_%H-%M-%S")
        return(0, 'Success!')


# Main

# Run backups

for job in backupJobs.keys():

    logging.info('Running ' + job + ' job')

    # Set variables
    name = job

    jobParams = {
        'service_stop_command': '',
        'service_start_command': '',
        'web_root': '',
        'db_dump_command': '',
        'extra_dirs': '',
        }

    for param, val in jobParams.iteritems():
        try:
            jobParams[param] = backupJobs[job][param]
        except KeyError:
            logging.debug('Setting "' + param + '" not set')
            pass

    # Run backup
    backup = webBackup(
        name,
        jobParams['service_stop_command'],
        jobParams['service_start_command'],
        jobParams['db_dump_command'],
        jobParams['web_root'],
        jobParams['extra_dirs'],
        )
    status = backup.run_backup()

    if status[0] != 0:
        print('Backup failed! Job: "' + name + '"')
        print('Error: ' + status[1])
        # Add error to errors list
        errors.append('Job : "' + name + '"' + ' Error: ' + status[1])
    else:
        print('Job: "' + name + '" successful\n')


# Check for errors and exit
if errors:
    print('Finished with errors')
    logging.warning('Backup run finished with errors!')
    for error in errors:
        print(error)
        logging.info(error)
    print('\n')
    sys.exit(1)
else:
    print('Finished without errors\n')
    logging.info('Backup run finished without errors')
    sys.exit(0)
