# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Set of utilities."""

import os
import click
import subprocess
from collections import OrderedDict

command_dict = OrderedDict(
    [
        (".rar", "unrar x"),
        (".gz", "gunzip"),
        (".tbz2", "tar xvjf"),
        (".tgz", "tar xvzf"),
        (".zip", "unzip "),
        (".tar", "tar xvf"),
        (".tar.gz", "tar xvzf"),
        (".tar.bz2", "tar xvjf"),
        (".7z", "7za -p{password} x"),
    ]
)

load_cmd = (
    "docker run --rm --volume {0}:/mybackup -v {1}:/backup " 'alpine sh -c "cd /mybackup && {2} /backup/{3} --strip 1"'
)
load_cmd_with_passwd = (
    "docker run --rm --volume {volume}:/mybackup -v {path}:/backup "
    'alpine sh -c "apk --update --no-cache add p7zip '
    '&& cd /mybackup && {extraction_command} /backup/{filename}"'
)

save_cmd = "docker run --rm --volume {0}:/mybackup -v {1}:/backup alpine tar czvf /backup/{2} /mybackup"
save_cmd_with_passwd = (
    "docker run --rm --volume {volume}:/mybackup -v {path}:/backup "
    "alpine sh -c 'apk --update --no-cache add p7zip "
    "&& 7za -p{password} a /backup/{filename} /mybackup'"
)


def allowed_files(filename):
    """Check if the uploaded file is allowed in the extensions."""
    allowed_extensions = command_dict.keys()
    if_allowed = False
    file_ext = None
    for ext in allowed_extensions:
        if ext in filename:
            if_allowed = True
            file_ext = ext
    return if_allowed, file_ext


def get_filename_from_path(path):
    """Get the correct path + filename from an absolute path."""
    if not os.path.isabs(path):
        raise Exception("`path` should be absolute path.")
    return path.rsplit("/", 1)


def execute_subprocess(cmd):
    """Execute a subprocess and return its exit status."""
    try:
        return subprocess.check_call(cmd, shell=True)
    except Exception as ex:
        return ex.returncode


def echo(msg, color):
    """Print a given message to stdout with a given color."""
    click.echo(click.style(msg, fg=color))


def success_msg(msg):
    """Print a successful message in green color."""
    echo(msg, color='green')


def error_msg(msg):
    """Print an error message in red color."""
    echo(msg, color='red')


def error_msg_and_exit(msg, exit_status=1):
    """Print an error message in red color and exit."""
    error_msg(msg)
    import sys
    sys.exit(exit_status)


def docker_volume_exist(volume):
    """Check if the docker-volume exists."""
    cmd = "docker volume inspect {0}".format(volume)
    status = execute_subprocess(cmd)
    return status == 0
