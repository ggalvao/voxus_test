# [START vendor]
from google.appengine.ext import vendor

import os.path


def patched_expanduser(path):
    return path

os.path.expanduser = patched_expanduser
# Add any libraries installed in the "lib" folder.
vendor.add('lib')
# [END vendor]

