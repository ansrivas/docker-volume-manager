# docker-volume-manager
Manage your named docker volumes using this simple script.


### Managing docker-volumes with a simple script.
-----
### Usage:

1. Clone this repository:

  `git clone https://github.com/ansrivas/docker-volume-manager.git`

2. Go to the directory and install this locally:

  `cd docker-volume-manager && pip install -e .`

3. To save a named-docker-volume:

  `docker-volume-manager save --volume <existing_named_volume>`

4. To load an already saved local volume to a named-docker-volume:

  `docker-volume-manager load --volume <new_volume_name> --path <absolute_path_to_your_saved_volume>`

5. More options can be seen by using the help:

  `docker-volume-manager --help`

###### Disclaimer: Do not use it directly in a production environment. Test it locally before using it out there.
