import kabbes_icloud
import py_starter as ps

c = kabbes_icloud.Client()

Contacts = kabbes_icloud.ICloudContacts( conn = c )
Contacts.run()


