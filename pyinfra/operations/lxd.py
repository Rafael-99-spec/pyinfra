'''
The LXD modules manage LXD containers
'''

from __future__ import unicode_literals

from pyinfra.api import operation


def get_container_named(name, containers):
    for container in containers:
        if container['name'] == name:
            return container
    else:
        return None


@operation
def container(
    state, host, id,
    present=True, image='ubuntu:16.04',
):
    '''
    Add/remove LXD containers.

    Note: does not check if an existing container is based on the specified
    image.

    + id: name/identifier for the container
    + image: image to base the container on
    + present: whether the container should be present or absent

    Example:

    .. code:: python

        lxd.container(
            name='Add an ubuntu container',
            id='ubuntu19',
            image='ubuntu:19.10',
        )
    '''

    container = get_container_named(id, host.fact.lxd_containers)

    # Container exists and we don't want it
    if container and not present:
        if container['status'] == 'Running':
            yield 'lxc stop {0}'.format(id)

        # Command to remove the container:
        yield 'lxc delete {0}'.format(id)

    # Container doesn't exist and we want it
    if not container and present:
        # Command to create the container:
        yield 'lxc launch {image} {id}'.format(id=id, image=image)
