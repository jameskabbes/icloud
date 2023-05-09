import kabbes_menu

class AttributeOption ( kabbes_menu.Menu ):

    _OVERRIDE_OPTIONS = {"1": ['','do_nothing']}

    _IMP_ATTS = [ 'field','label' ]
    _ONE_LINE_ATTS = ['field','label']

    menu_client = kabbes_menu.Client( _OVERRIDE_OPTIONS=_OVERRIDE_OPTIONS )
    cfg_menu = menu_client.cfg_menu

    def __init__( self, dictionary ):
        kabbes_menu.Menu.__init__( self )
        self.set_atts(dictionary)

    def get_attr( self, att ):

        if self.has_attr( att ):
            return getattr( self, att )
        else:
            return None
