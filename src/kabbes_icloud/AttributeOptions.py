from kabbes_menu import Menu
from parent_class import ParentPluralList
from kabbes_icloud import AttributeOption

class AttributeOptions( ParentPluralList, Menu ):

    _OVERRIDE_OPTIONS = {1: ['Open Attribute Option', 'run_Child_user']}

    _IMP_ATTS = [ 'name' ]
    _ONE_LINE_ATTS = [ 'name' ]
    SUFFIX = '_Options'

    def __init__( self, name, list_of_options ):
        ParentPluralList.__init__( self, 'Options' )
        Menu.__init__( self )

        self.name = name

        for dictionary in list_of_options:
            self.add_Option( AttributeOption(dictionary) )

    def add_Option( self, new_Option ):
        self._add( new_Option )

