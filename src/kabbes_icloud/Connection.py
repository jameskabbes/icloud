from parent_class import ParentClass
from pyicloud import PyiCloudService
import sys

class Connection( ParentClass ):

    def __init__( self, *args, **kwargs ):

        ParentClass.__init__( self )
        self.get_connection( *args, **kwargs )

    def get_connection( self, *args, account_email = None, account_password = None ):

        connection = PyiCloudService( account_email, account_password )

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

        self.conn = connection

