import kabbes_menu
from parent_class import ParentPluralList
from kabbes_icloud import AttributeOption

class AttributeOptions( ParentPluralList, kabbes_menu.Menu ):

    _OVERRIDE_OPTIONS = {"1": ['Open Attribute Option', 'run_Child_user']}

    _IMP_ATTS = [ 'name' ]
    _ONE_LINE_ATTS = [ 'name' ]
    SUFFIX = '_Options'

    menu_client = kabbes_menu.Client( _OVERRIDE_OPTIONS=_OVERRIDE_OPTIONS )
    cfg_menu = menu_client.cfg_menu

    def __init__( self, name, list_of_options ):
        ParentPluralList.__init__( self, 'Options' )
        kabbes_menu.Menu.__init__( self )

        self.name = name

        for dictionary in list_of_options:
            self.add_Option( AttributeOption(dictionary) )

    def add_Option( self, new_Option ):
        self._add( new_Option )

