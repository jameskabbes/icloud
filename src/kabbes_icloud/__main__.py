import kabbes_icloud

conn = kabbes_icloud.Connection( account_email = input('Input your Apple account email: '),
                                 account_password = input('Enter your Apple account password: ')  )

Contacts = kabbes_icloud.ICloudContacts( conn = conn )

selected_Contacts, final_string = Contacts.get_Contacts_from_input()
selected_Contacts.print_atts()

for Contact in selected_Contacts:
    Contact.print_all_atts()
