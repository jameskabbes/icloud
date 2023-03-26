import kabbes_icloud
import user_profile
from kabbes_account_manager import Accounts

Accs = Accounts.Accounts( database_name = 'jameskabbes' )

conn = kabbes_icloud.Connection( account_email = user_profile.profile.email,
                                        account_password = Accs.get_Acc_by_att_value('name','Apple').get_password()  )

Contacts = kabbes_icloud.ICloudContacts( conn = conn )

selected_Contacts, final_string = Contacts.get_Contacts_from_input()
selected_Contacts.print_atts()

for Contact in selected_Contacts:
    Contact.print_all_atts()
