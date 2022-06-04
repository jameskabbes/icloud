###
#
###

import iCloud_Contacts

import user_profile
import icloud_support_functions as icsf
import py_starter as ps

###

connection = icsf.get_connection( user_profile.profile.email, icsf.get_apple_password() )
Contacts = iCloud_Contacts.iCloud_Contacts( connection=connection )

selected_Contacts, final_string = Contacts.get_Contacts_from_input()
selected_Contacts.print_atts()

for Contact in selected_Contacts:
    Contact.print_all_atts()
