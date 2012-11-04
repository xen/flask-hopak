# -*- coding: utf-8 -*-
#
import formgear
from flask import Blueprint
from .views import *
from .widgets import *

from flask import _app_ctx_stack as ctx


class Admin(object):

    def __init__(self, app=None, prefix='/admin/'):
        if app is not None:
            self.app = app
            #self.init_app(self.app)
            self.prefix = prefix
            self.tree = []
        else:
            self.app = None

    def add_model(self, model):
        assert(isinstance(model, formgear.models.Model))


