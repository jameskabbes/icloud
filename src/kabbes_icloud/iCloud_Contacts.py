from parent_class import ParentClass 
from real_time_input import RealTimeInput as RTI
import iCloud_Contact
import pandas as pd
import random
import icloud_support_functions as icsf
import py_starter as ps


class iCloud_Contacts( ParentClass ):

    TABLE_NAME = 'iCloud_Contacts'
    DATA_COL = 'data'
    COLS = [iCloud_Contact.iCloud_Contact.ID_COL, DATA_COL]

    def __init__( self, connection = None, df = pd.DataFrame(), json_string = None, dictionary = {} ):

        ParentClass.__init__( self )

        self.connection = connection

        self.Contacts = {} #the contactId is the key
        self.RTI = iCloudRealTimeInput( self )

        if not df.empty:
            self._import_from_df( df )

        elif json_string != None:
            self._import_from_json( json_string )

        elif dictionary != {}:
            self._import_from_dict( dictionary )

        elif self.connection != None:
            self._get_Contacts_from_iCloud()

    def _get_Contacts_from_iCloud( self ):

        list_of_dictionaries = self.connection.contacts.all()
        for dictionary in list_of_dictionaries:
            self.add_iCloud_Contact( iCloud_Contact.iCloud_Contact( dictionary ) )

    def _import_from_dict( self, dictionary ):

        '''Given a dictionary, populate the Contacts'''

        for contactId in dictionary:
            new_Contact = iCloud_Contact.iCloud_Contact( dictionary[contactId] )
            self.add_iCloud_Contact( new_Contact )

    def _import_from_json( self, json_string ):

        '''Given a json string, populate the Contacts '''

        dictionary = ps.json_to_dict( json_string )
        self._import_from_dict( dictionary )

    def _import_from_df( self, df ):

        '''Given a DataFrame, populate the Contacts '''

        json_strings = df[ self.DATA_COL ]
        for i in range(len( json_strings )):
            new_Contact = iCloud_Contact.iCloud_Contact( json_string = json_strings[i] )
            self.add_iCloud_Contact( new_Contact )

    def export_to_dict( self ):

        '''export all contacts to a dictionary'''

        dictionary = {}
        for Contact in self:
            dictionary.update({ Contact.ID_COL : Contact.export_to_dict() })

        return dictionary

    def export_to_json( self ):

        '''export all contacts to a json format'''

        dictionary = self.export_to_dict()
        return ps.dict_to_json( dictionary )

    def export_to_df( self ):

        '''export all contacts to a pandas DataFrame'''

        df = pd.DataFrame( columns = self.COLS )

        for Contact in self:

            new_df = pd.DataFrame( columns = self.COLS )
            for col in self.COLS:

                if col == self.DATA_COL:
                    value = Contact.export_to_json()
                else:
                    value = Contact.get_attr( col )

                new_df[ col ] = [ value ]

            df = df.append( new_df, ignore_index = True )

        return df

    def __len__( self ):

        return len(self.Contacts)

    def __iter__( self ):

        self.i = -1
        return self

    def __next__( self ):

        self.i += 1

        if self.i >= len(self.Contacts):
            raise StopIteration
        else:
            return self.Contacts[ list(self.Contacts.keys())[self.i] ]

    def print_imp_atts( self, print_off = True ):

        string = 'Contacts: ' + str(len(self)) + '\n'
        for Contact in self:
            string += Contact.print_one_line_atts( print_off = False ) + '\n'

        return self._print_imp_atts_helper( override_string = string, print_off = print_off )

    def print_one_line_atts( self, leading_string = '\t', print_off = True ):

        string = 'iCloud_Contacts: ' + str(len(self))
        return self._print_one_line_atts_helper( override_string = string, leading_string = leading_string, print_off = print_off )

    def add_iCloud_Contacts( self, list_of_Contact_insts ):

        '''Add a list of Contact classes to the Contacts dictionary '''

        for Contact_inst in list_of_Contact_insts:
            self.add_iCloud_Contact( Contact_inst )

    def merge_iCloud_Contacts( self, Contacts_inst, how = 'left', overwrite = False ):

        if how == 'right':
            left = Contacts_inst
            right = self

        else: #left, there are only two merge options
            left = self
            right = Contacts_inst

        ### Perform the merge
        merged_Contacts = iCloud_Contacts()
        left_ids = [ Contact.get_id() for Contact in list(left)  ]
        right_ids = [ Contact.get_id() for Contact in list(right)  ]

        for j in range(len(right)):
            id = right_ids[j]

            # if this contact is also present in the left, update the Contact with the info from the left
            if id in left_ids:
                right.Contacts[ id ].update( dictionary = left.Contacts[id].export_to_dict() )

            merged_Contacts.add_iCloud_Contact( right.Contacts[ id ] )

        # add all contacts which are present in the left but not in the right
        for i in range(len(left)):
            id = left_ids[i]

            if id not in right_ids:
                merged_Contacts.add_iCloud_Contact( left.Contacts[ id ] )

        if overwrite:
            self = merged_Contacts

        return merged_Contacts

    def add_iCloud_Contact( self, Contact_inst ):

        '''Add a singular iCloud_Contact to the Contacts dictionary'''

        self.Contacts[ Contact_inst.contactId ] =  Contact_inst

    def remove_iCloud_Contact( self, Contact_inst ):

        '''Remove a singular iCloud_Contact from the Contacts dictionary'''

        self.Contacts.pop( Contact_inst.contactId, None )

    def get_random_Contact( self ):

        '''Select a random Contact class instance from the Contacts dictionary '''

        rand_ind = random.randrange( len(self.Contacts) )
        return self.Contacts[ list(self.Contacts.keys())[rand_ind] ]

    def select_Contacts_where( self, dictionary = {} ):

        '''Returns an iCloud_Contacts instance where all Contacts have keys=values in the dictionary
        dictionary = {'firstName': 'James', 'lastName': 'Kabbes'} returns an instance with all Contacts that contain James Kabbes'''

        # use recursion to select Contacts where keys=values
        Valid_Contacts = iCloud_Contacts()
        Valid_Contacts.Contacts = self.Contacts.copy()

        for att in dictionary:

            boolean_dict = Valid_Contacts.lambda_on_Contacts( lambda Contact: Contact.get_attr( att ) == dictionary[att] )

            for contactId in boolean_dict:
                if not boolean_dict[ contactId ]:
                    Valid_Contacts.remove_iCloud_Contact( Valid_Contacts.Contacts[contactId] )

        # returns an iCloud_Contacts class instance
        return Valid_Contacts

    def update_Contacts( self, dictionary = {}, json_string = None ):

        ''' { contactId1: Dictionary1, contactId2: Dictionary2 }  '''

        if json_string != None:
            dictionary = ps.json_to_dict( json_string )

        ids = [ Contact.get_attr(Contact.ID_COL) for Contact in list(self) ]
        for id in dictionary:
            if id in ids:
                self.update( dictionary[id] )

    def lambda_on_Contacts( self, lambda_func ):

        '''given a lambda function (lambda Contact: Contact.get_attr("firstName")), put each return statement in a dict'''

        results = {}
        for contactId in self.Contacts:
            results[contactId] = lambda_func( self.Contacts[contactId] )

        return results

    def show_attribute_breakdown( self ):

        values_and_counts = {}

        for contactId in self.Contacts:
            Contact_inst = self.Contacts[contactId]

            for key in vars(Contact_inst):

                if key not in values_and_counts:
                    values_and_counts[key] = 1
                else:
                    values_and_counts[key] += 1

        df_breakdown = pd.DataFrame( {'Key': list(values_and_counts.keys()), 'Frequency': list(values_and_counts.values()) } )
        df_breakdown['Proportion'] = df_breakdown['Frequency'] / len(self.Contacts)
        df_breakdown.sort_values( 'Frequency', inplace = True, ascending = False )

        self.df_breakdown = df_breakdown
        return df_breakdown

    def prepare_autocomplete( self, contactIds, string, index_value, atts_to_display = ['firstName','lastName'] ):

        '''prepare the autocomplete for the Contact search function'''

        if len(contactIds) == 0:
            display = string + ' - (0)'

        elif len(contactIds) >= 1:
            Contact_display_value = ' '.join( self.Contacts[contactIds[index_value]].get_atts( atts_to_display ) )
            display = string + ' - (' + str(index_value + 1)+ '/' + str(len(contactIds)) + ') - ' + Contact_display_value

        return display

    def get_Contacts_from_input( self ):

        print ('Begin searching for Contacts...')
        list_of_Contacts, final_string = self.RTI.get_multiple_inputs()

        Contacts = iCloud_Contacts()
        for Contact in list_of_Contacts:
            Contacts.add_iCloud_Contact( Contact )

        return Contacts, final_string


class iCloudRealTimeInput( RTI ):

    def __init__( self, Contacts ):

        RTI.__init__( self )
        self.Contacts = Contacts

    def search( self ):

        '''search for given string in the Contacts '''

        self.suggestions = []
        if len(self.string) > 1:

            for Contact in self.Contacts:

                name = Contact.display.lower()
                if self.string.lower() in name:
                    self.suggestions.append( Contact )

    def prepare_autocomplete( self ):

        if len(self.string) > 1:
            if len(self.suggestions) == 0:
                self.display = self.string + ' - (0)'

            else:
                self.suggestion = self.suggestions[ self.suggestion_index ]

                ### Get the suggestion display based on the aself object's method
                suggestion_display = self.suggestion.display

                self.display = '{string} - ({i}/{n}) - {suggestion_display}'.format(
                    string = self.string,
                    i = self.suggestion_index+1,
                    n = len(self.suggestions),
                    suggestion_display = suggestion_display )

        else:
            self.display = self.string
