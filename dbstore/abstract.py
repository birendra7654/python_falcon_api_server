"""Abstract interface class."""
# !/usr/bin/env python
#
#
__author__ = 'Sanctum Networks (P) Ltd.'

###
# Asbtract base class
# Inherited classes may implement methods from here
###


class abstract(object):
    """Abstract class."""

    def __init__(self, *args, **kwargs):
        """Undefined init method."""
        pass

    def setup(self, y):
        """Undefined in base class but should be define in child class."""
        pass
