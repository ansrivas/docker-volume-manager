# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Load and save your docker-volumes."""

import os
import app
import sys
import click
import datetime
from app import utils
from app.uploader import upload_to_s3
from future.utils import raise_with_traceback as rwt


@click.group()
@click.version_option(app.__version__)
def cli():
    """Showcase different options to backup and load docker volumes."""
    pass


@cli.command()
@click.option("--volume", required=True, type=click.STRING, help="The named volume to save locally. ")
@click.option(
    "--path",
    default=".",
    type=click.Path(exists=True, file_okay=False, resolve_path=True, writable=True),
    help="The path to save the docker volume as .tar.gz",
)
@click.option("--interactive", default=True, type=click.BOOL, help="Run the script interactively")
@click.option(
    "--to-s3",
    is_flag=True,
    help=(
        "Upload the downloaded volume to s3. This expects a .env file with ACCESS_KEY, SECRET and BUCKET"
        "name variables"
    ),
)
@click.option(
    "--env-path",
    default="./.env",
    type=click.Path(exists=True, file_okay=True, resolve_path=True),
    help=("Path to the .env file which contains ACCESS_KEY, SECRET and BUCKET and optional FILE_PASSWORD"),
)
def save(volume, path, interactive, to_s3, env_path):
    """Save your docker volume locally."""
    exporting_time = str(datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
    filename = volume + "_" + exporting_time + ".tar.gz"

    if env_path:
        from dotenv import load_dotenv
        load_dotenv(dotenv_path=env_path, verbose=True)

    compressed_file_passwd = os.getenv("FILE_PASSWORD")
    if compressed_file_passwd:
        # Only 7zip is supporting compressed password protected files
        filename = volume + "_" + exporting_time + ".7z"
        save_cmd = utils.save_cmd_with_passwd.format(
            volume=volume, path=path, filename=filename, password=compressed_file_passwd
        )
    else:
        save_cmd = utils.save_cmd.format(volume, path, filename)

    if not utils.docker_volume_exist(volume):
        msg = "docker volume '{}' does not exist. ".format(volume)
        utils.error_msg_and_exit(msg)

    if interactive:
        click.confirm("Do you want to continue", abort=True)

    ret_status = utils.execute_subprocess(save_cmd)
    if ret_status != 0:
        utils.error_msg_and_exit("Failed to save the docker volume", ret_status)

    # Handle upload to s3
    if to_s3:
        endpoint_url = os.getenv("URL")
        access_key = os.getenv("ACCESS_KEY")
        secret = os.getenv("SECRET")
        bucket = os.getenv("BUCKET")
        local_file_path = os.path.join(path, filename)
        filename_on_s3 = filename
        if not all([endpoint_url, access_key, secret, bucket]):
            utils.error_msg_and_exit(("One of the environment variables is missing. "
                                      "Options are : \n- URL\n- ACCESS_KEY\n- SECRET\n- BUCKET\n"
                                      "Please populate it or give a path to .env"))
        upload_to_s3(endpoint_url, access_key, secret, bucket, local_file_path, filename_on_s3)

    utils.success_msg(
        msg="\nSuccessfully exported docker volume at: {0}\n".format(os.path.join(path, filename))
    )


@cli.command()
@click.option(
    "--volume",
    required=True,
    type=click.STRING,
    help="The named volume where the zip is to be uploaded. for eg. /my_saved_volume.tar.gz ",
)
@click.option(
    "--path",
    required=True,
    type=click.Path(exists=True, file_okay=True, dir_okay=False, resolve_path=True, readable=True),
    help="The path to load the zip or tar or tar.gz from.",
)
@click.option("--interactive", default="True", type=click.BOOL, help="Run the script interactively")
@click.option(
    "--password",
    default=None,
    type=click.STRING,
    help=(
        "An optional password if your 7zipped file was password protected. "
        "Avoid using this as this accepts password in plain text."
    ),
)
@click.option(
    "--env-path",
    default=None,
    type=click.Path(exists=True, file_okay=True, resolve_path=True),
    help="Path to the .env file which contains FILE_PASSWORD. For e.g. /mnt/data/test.env",
)
def load(volume, path, interactive, password, env_path):
    """Load the locally saved volume to named docker-volume."""
    if env_path and password:
        utils.error_msg_and_exit("Providing both env_path and password is restricted.")

    path, filename = utils.get_filename_from_path(path)
    allowed, extension = utils.allowed_files(filename)
    extraction_command = utils.command_dict[extension]
    if not allowed:
        rwt("File extension not allowed", traceback=Ellipsis)

    if env_path:
        # If env file is provided
        from dotenv import load_dotenv
        load_dotenv(dotenv_path=env_path, verbose=True)

    def create_load_cmd(volume, path, extraction_command, filename):
        return utils.load_cmd_with_passwd.format(
            volume=volume, path=path, extraction_command=extraction_command, filename=filename
        )

    # priority goes to command line password override
    if password:
        extraction_command = extraction_command.format(password=password)
        load_cmd = create_load_cmd(
            volume, path, extraction_command, filename
        )
    else:
        # then it tries to read from the environment
        file_password = os.getenv("FILE_PASSWORD")
        if file_password:
            extraction_command = extraction_command.format(password=file_password)
            load_cmd = create_load_cmd(
                volume, path, extraction_command, filename
            )
        else:
            extraction_command = extraction_command.format(password="")
            load_cmd = utils.load_cmd.format(volume, path, extraction_command, filename)

    confirm_msg = "The named volume already exists.\nDo you wish to overwrite?"
    if utils.docker_volume_exist(volume):
        click.confirm(confirm_msg, abort=True)

    if interactive:
        click.confirm("Safe to upload the named volume. Do you want to continue", abort=True)

    ret_status = utils.execute_subprocess(load_cmd)
    if ret_status != 0:
        raise Exception("Failed to load the docker volume")

    msg = "\nSuccessfully imported docker volume at: {0} as {1}\n".format(os.path.join(path, filename), volume)
    utils.success_msg(msg)
