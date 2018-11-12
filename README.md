# docker-volume-manager
Manage your named docker volumes using this simple script.

#### Disclaimer: Do not use it directly in a production environment. Test it locally before using it out there.


### Managing docker-volumes with a simple script.
-----

### Installation:

`pip install docker-volume-manager`

### Usage:

```bash
$ docker-volume-manager --help
Usage: docker-volume-manager [OPTIONS] COMMAND [ARGS]...

  Showcase different options to backup and load docker volumes.

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  load  Load the locally saved volume to named...
  save  Save your docker volume locally.
```

### Examples:
- Upload to s3 ( or similarly compatible storage )

  ```bash
  $ docker volume ls
  DRIVER              VOLUME NAME
  local               my-named-docker-volume

  $ docker-volume-manager save --path=. --env-path=.env --volume=my-named-docker-volume --to-s3  --interactive=False
  ```

- Optionally create a password protected volume using .env or populate it in the environment variable
  ```bash
  $ cat .env

  URL=url-to-connect-to
  ACCESS_KEY=my-s3-access-key
  SECRET=my-s3-compatible-secret
  SPACE=my-bucket-to-write-to
  FILE_PASSWORD=my-file-will-be-7zipped-with-this-password
  ```

#### A simple use case could be to backup named docker-volumes:
  ```bash
  # cat backup_script.py
  import os
  import subprocess
  import time

  files = os.listdir('./')
  tars = [f for f in files if f.endswith('.tar.gz')]
  to_keep = sorted(tars)[-7:]
  for tar in tars:
      if tar not in to_keep:
          os.remove(tar)

  command = ["/usr/bin/docker-volume-manager", "save", "--volume", "your_docker_data_volume", "--interactive","False"]
  subprocess.check_output(command )
  ```
