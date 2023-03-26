from kabbes_menu import Menu

class AttributeOption ( Menu ):

    _OVERRIDE_OPTIONS = {1: ['','do_nothing']}

    _IMP_ATTS = [ 'field','label' ]
    _ONE_LINE_ATTS = ['field','label']

    def __init__( self, dictionary ):
        Menu.__init__( self )
        self.set_atts(dictionary)

    def get_attr( self, att ):

        if self.has_attr( att ):
            return getattr( self, att )
        else:
            return None
