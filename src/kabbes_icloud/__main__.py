import kabbes_icloud
import py_starter as ps

conn = kabbes_icloud.Connection( account_email = input('Input your Apple account email: '),
                                 account_password = ps.get_secret_input('Enter your Apple account password: ')  )

Contacts = kabbes_icloud.ICloudContacts( conn = conn )
Contacts.run()

