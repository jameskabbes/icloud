from parent_class import ParentClass, ParentPluralList 
import py_starter as ps

class ICloudContact( ParentClass ):

    ID_COL = 'contactId'

    def __init__( self, dictionary = {}, json_string = None ):

        ParentClass.__init__( self )

        if dictionary != {}:
            self._import_from_dict( dictionary )

        elif json_string != None:
            self._import_from_json( json_string )

        self._check_for_Attribute_Options()
        self.display = self.get_display()

    def get_display( self ):

        return ' '.join( [ str(self.get_attr( 'firstName' )), str( self.get_attr('lastName')) ] )

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

        options_att = att + Attribute_Options.suffix

        if self.has_attr( options_att ):
            return options_att
        else:
            return None

    def _check_for_Attribute_Options( self ):

        vars_to_check = vars(self).copy() #define this here otherwise the vars(self) changes length

        for key in vars_to_check:
            value = self.get_attr(key)
            if type( value ) == list:
                new_att = key + Attribute_Options.suffix
                self.set_attr( new_att, Attribute_Options(key, value) )

    def update( self, dictionary = {}, json_string = None ):

        if json_string != None:
            dictionary = ps.json_to_dict( json_string )

        self.set_atts( dictionary )
        self._check_for_Attribute_Options()

    def print_imp_atts( self, print_off = True):

        return self._print_imp_atts_helper( atts = ['firstName','lastName','phones'], print_off = print_off )

    def print_one_line_atts( self, print_off = True, leading_string = '\t' ):

        return self._print_one_line_atts_helper( atts = ['firstName', 'lastName'], print_off = print_off, leading_string = leading_string )

    def _import_from_dict( self, dictionary ):

        self.set_atts( dictionary )

    def _import_from_json( self, json_string ):

        dictionary = ps.json_to_dict( json_string )
        self._import_from_dict( dictionary )

    def export_to_dict( self ):

        atts_dict = {}
        for att in vars(self):
            if not att.endswith( Attribute_Options.suffix ):
                atts_dict[ att ] = self.get_attr( att )

        return atts_dict

    def export_to_json( self ):

        dictionary = self.export_to_dict()
        return ps.dict_to_json( dictionary )

    def user_select_Option( self, att ):

        '''only works for attributes which have a list of options'''

        viable_Options = self.get_attr( att + Attribute_Options.suffix )

        ps.print_for_loop( [ Option.print_one_line_atts(print_off = False) for Option in viable_Options ] )
        ind = ps.get_int_input( 1, len(self.get_attr(att)), 'Select the ' + str(att) + ' option: ' ) - 1

        Option = viable_Options.Options[ ind ]
        return Option, viable_Options

    def check_has_iMessage( self ):

        if self.has_attr('phones'):
            for Option in self.get_attr( 'phones' + Attribute_Options.suffix ):
                if Option.label == 'IPHONE':
                    return True

        return False

    def get_multi_preffered_Option( self, att, list_pref_atts, list_pref_values, index_pref = 0 ):

        '''att = "phones", list_pref_atts = ['label','other_field'], list_pref_values = [['IPHONE','MOBILE'],['OTHER_VALUE']] '''

        viable_Options = self.get_attr( att + Attribute_Options.suffix )

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
            att_Options = self.get_attr( att + Attribute_Options.suffix )

        viable_Options = Attribute_Options( att_Options.name, [] )

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


class Attribute_Options (ParentPluralList) :

    suffix = '_Options'

    def __init__(self, name, list_of_options):

        ParentPluralList.__init__( self, 'Options' )
        self.name = name

        for dictionary in list_of_options:
            self.add_Option( Attribute_Option(dictionary) )

    def add_Option( self, new_Option ):

        self._add( new_Option )

class Attribute_Option (ParentClass):

    def __init__( self, dictionary ):

        ParentClass.__init__( self )
        self.set_atts(dictionary)

    def get_attr( self, att ):

        if self.has_attr( att ):
            return getattr( self, att )
        else:
            return None

    def print_imp_atts( self, print_off = True ):

        string = self.print_class_type( print_off = False ) + '\n'
        string += ('Field:\t' + str(self.get_attr('field')) + '\n' )
        string += ('Label:\t' + str(self.get_attr('label')) + '\n' )
        string = string[:-1]
        return self.print_string( string, print_off = print_off )

    def print_one_line_atts( self, print_off = True, leading_string = '\t' ):

        string = leading_string
        string += 'Field:\t' + str(self.get_attr('field')) + ', '
        string += 'Label:\t' + str(self.get_attr('label')) + ', '

        string = string[:-2]
        return self.print_string( string, print_off = print_off )
