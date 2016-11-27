# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Set of utilities."""

import subprocess
import click
from collections import OrderedDict
command_dict = OrderedDict((('.rar', 'unrar x'),
                            ('.gz', 'gunzip'),
                            ('.tbz2', 'tar xvjf'),
                            ('.tgz', 'tar xvzf'),
                            ('.zip', 'unzip '),
                            ('.tar', 'tar xvf'),
                            ('.tar.gz', 'tar xvzf'),
                            ('.tar.bz2', 'tar xvjf'))
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
    return path.rsplit('/', 1)


def execute_subprocess(cmd):
    """Execute a subprocess and return its exit status."""
    status = 0
    try:
        status = subprocess.check_call(cmd, shell=True)
    except Exception as ex:
        status = ex.returncode
    return status


def echo(msg, color):
    """Print a given message to stdout with a given color."""
    click.echo(click.style(msg, fg=color))


def docker_volume_exist(volume):
    """Check if the docker-volume exists."""
    cmd = "docker volume inspect {0}".format(volume)
    status = execute_subprocess(cmd)
    return status == 0