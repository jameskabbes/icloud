import kabbes_menu 
import py_starter as ps
from kabbes_icloud import AttributeOptions, AttributeOption

class ICloudContact( kabbes_menu.Menu ):

    firstName = ''
    lastName = ''

    ID_COL = 'contactId'
    _SEARCHABLE_ATTS = [ 'firstName','lastName', 'fullName' ]

    _ONE_LINE_ATTS = [ 'firstName','lastName' ] 
    _IMP_ATTS = [ 'firstName','lastName','phones' ]

    _OVERRIDE_OPTIONS = {"1": ['Open Attribute Options', 'run_Child_user']}

    menu_client = kabbes_menu.Client( _OVERRIDE_OPTIONS=_OVERRIDE_OPTIONS )
    cfg_menu = menu_client.cfg_menu

    def __init__( self, dictionary = {}, json_string = None ):

        kabbes_menu.Menu.__init__( self )

        if dictionary != {}:
            self._import_from_dict( dictionary )

        elif json_string != None:
            self._import_from_json( json_string )

        self.fullName = ' '.join( [self.firstName, self.lastName] )

        self._check_for_Attribute_Options()

    def get_id_col( self ):
        return self.ID_COL

    def get_id( self ):
        return self.get_attr( self.get_id_col() )

    def get_attr( self, att ):

        if self.has_attr( att ):
            return getattr( self, att )
        else:
            return None

    def get_atts( self, atts ):

        return [ str(self.get_attr(att)) for att in atts ]

    def att_has_Options( self, att ):

        options_att = att + AttributeOptions.SUFFIX

        if self.has_attr( options_att ):
            return options_att
        else:
            return None

    def _check_for_Attribute_Options( self ):

        vars_to_check = vars(self).copy() #define this here otherwise the vars(self) changes length



        for key in vars_to_check:
            value = self.get_attr(key)
            if type( value ) == list:
                new_att = key + AttributeOptions.SUFFIX

                new_AttributeOptions = AttributeOptions(key, value)
                self.set_attr( new_att, new_AttributeOptions )

                self._Children.append( new_AttributeOptions )

    def update( self, dictionary = {}, json_string = None ):

        if json_string != None:
            dictionary = ps.json_to_dict( json_string )

        self.set_atts( dictionary )
        self._check_for_Attribute_Options()

    def _import_from_dict( self, dictionary ):

        self.set_atts( dictionary )

    def _import_from_json( self, json_string ):

        dictionary = ps.json_to_dict( json_string )
        self._import_from_dict( dictionary )

    def export_to_dict( self ):

        atts_dict = {}
        for att in vars(self):
            if not att.endswith( AttributeOptions.SUFFIX ):
                atts_dict[ att ] = self.get_attr( att )

        return atts_dict

    def export_to_json( self ):

        dictionary = self.export_to_dict()
        return ps.dict_to_json( dictionary )

    def check_has_iMessage( self ):

        if self.has_attr('phones'):
            for Option in self.get_attr( 'phones' + AttributeOptions.SUFFIX ):
                if Option.label == 'IPHONE':
                    return True

        return False

    def get_multi_preffered_Option( self, att, list_pref_atts, list_pref_values, index_pref = 0 ):

        '''att = "phones", list_pref_atts = ['label','other_field'], list_pref_values = [['IPHONE','MOBILE'],['OTHER_VALUE']] '''

        viable_Options = self.get_attr( att + AttributeOptions.SUFFIX )

        for i in range(len(list_pref_atts)):

            pref_att = list_pref_atts[i]
            pref_values = list_pref_values[i]

            viable_Options = self.get_preffered_Option( att, pref_att, pref_values, index_pref = None, att_Options = viable_Options )
            viable_Options.print_atts()

        # if they don't want an index returned, return all viable options
        if index_pref == None:
            return viable_Options

        # if they specify an index, return the given index
        else:
            if len(viable_Options) > index_pref:
                return viable_Options.Options[index_pref]
            else:
                return viable_Options.Options[0]

    def get_preffered_Option( self, att, pref_att, pref_values, index_pref = 0, att_Options = None ):

        ''' att = "phones", pref_att = 'label', pref_values = ['IPHONE', 'MOBILE'], index_pref = 0 '''

        if att_Options == None:
            att_Options = self.get_attr( att + AttributeOptions.SUFFIX )

        viable_Options = AttributeOptions( att_Options.name, [] )

        # loop through each preffered value ['IPHONE','MOBILE']
        for pref_value in pref_values:

            # loop through each Phone number option
            for Option in att_Options:

                # and the attribute matches the preferred value: Option.field == 'IPHONE'
                if Option.get_attr( pref_att ) == pref_value:
                    viable_Options.add_Option( Option )

            # as soon as a pref_att/pref_value combo is found, exit the loop
            if len(viable_Options) > 0:
                break

        # if nothing satisfied the conditions, reset to the original
        if len(viable_Options) == 0:
            viable_Options = att_Options

        # the user wants a instance of Attribute_Options ranked in order of feasibilty
        if index_pref == None:
            return viable_Options

        # the user wants a specific Option class returned
        else:
            # If there are enough Options to return the preffered index
            if len(viable_Options) > index_pref:
                return viable_Options.Options[index_pref]

            # Otherwise just return the first one
            else:
                return viable_Options.Options[0]

