from parent_class import ParentClass
from pyicloud import PyiCloudService
import kabbes_account_manager
import sys

class Connection( ParentClass ):

    def __init__( self, **kwargs ):

        ParentClass.__init__( self )
        if self.cfg['load_credentials']:
            email, password = self.load_credentials()
            self.conn = self.get_connection( email = email, password = password )

        else:
            self.conn = self.get_connection( **kwargs )

    def load_credentials( self ):

        if self.cfg['accounts_manager.client.inst'] == None:
            args, kwargs = self.cfg['accounts_manager.client'].get_args(), self.cfg['accounts_manager.client'].get_kwargs()
            self.cfg.get_node('accounts_manager.client.inst').set_value( kabbes_account_manager.Client( *args, **kwargs ) )

        AppleAccount = self.cfg['accounts_manager.client.inst'].Accounts.Accounts[ self.cfg['accounts_manager.id'] ]

        email = AppleAccount.Entries.get_Entry( 'email' ).Value.val
        password = AppleAccount.Entries.get_Entry( 'password' ).Value.val
        return email, password

    @staticmethod
    def get_connection( email=None, password=None ):

        connection = PyiCloudService( email, password )
        if connection.requires_2fa:

            print ('Two-factor authentication required.')
            code = input("Enter the code you received of one of your approved devices: ")
            result = connection.validate_2fa_code(code)

            print('Code validation result: ' + str(result))

            if not result:
                print('Failed to verify security code')
                sys.exit(1)

            if not connection.is_trusted_session:
                print('Session is not trusted. Requesting trust...')
                result = connection.trust_session()
                print('Session trust result: '  + str(result) )

                if not result:
                    print('Failed to request trust. You will likely be prompted for the code again in the coming weeks')

        elif connection.requires_2sa:
            import click
            print('Two-step authentication required. Your trusted devices are: ')

            devices = connection.trusted_devices
            for i, device in enumerate(devices):
                print ("  %s: %s" % (i, device.get('deviceName',"SMS to %s" % device.get('phoneNumber'))) )

            device = click.prompt('Which device would you like to use?', default=0)
            device = devices[device]
            if not connection.send_verification_code(device):
                print ("Failed to send verification code")
                sys.exit(1)

            code = click.prompt('Please enter validation code')
            if not connection.validate_verification_code(device, code):
                print ("Failed to verify verification code")
                sys.exit(1)

        return connection

