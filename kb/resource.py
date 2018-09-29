import os
import shutil

from kb.resources import list_resources
from kb.utils import die, open_with_editor

def copy(current_resource_path, new_resource_path):
    """ Copies a resource to a new path """

    # attempt to copy the resource to KB_EX_PATH
    try:
        shutil.copy(current_resource_path, new_resource_path)

    # fail gracefully if the resource cannot be copied. This can happen if
    # KB_EX_PATH does not exist
    except IOError:
        die('Could not copy resource for editing.')


def create_or_edit(resource):
    """ Creates or edits a resource """

    # if the resource does not exist
    if not exists(resource):
        create(resource)

    # if the resource exists but not in the example_path, copy it to the
    # default path before editing
    elif exists(resource) and not exists_in_example_path(resource):
        copy(path(resource), os.path.join(resources.example_path(), resource))
        edit(resource)

    # if it exists and is in the default path, then just open it
    else:
        edit(resource)


def create(resource):
    """ Creates a resource """
    new_resource_path = os.path.join(resources.example_path(), resource)
    open_with_editor(new_resource_path)


def edit(resource):
    """ Opens a resource for editing """
    open_with_editor(path(resource))


def read(resource):
    """ Returns the contents of the resource as a String """
    for r, p in list_resources('all'):
        if r == resource and os.path.exists(p):
            with open(p) as f:
                return f.read()
