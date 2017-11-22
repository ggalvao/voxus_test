# [START vendor]
from google.appengine.ext import vendor

import os.path

# Add any libraries installed in the "lib" folder.
vendor.add('lib')
# [END vendor]

