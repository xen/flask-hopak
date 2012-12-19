# -*- coding: utf-8 -*-
#
from flask import render_template, g, request, redirect, url_for, flash
from functools import partial
from flask.views import View, MethodView
from hopak.models import ModelRegistry
from hopak.utils import form_dict

from . base import BaseView, expose

class ModelView(BaseView):
    """ Base model admin view """

    list_per_page = 20
    relation = []

    list_template = 'admin/form/list.html'
    add_template = 'admin/form/add.html'
    delete_template = 'admin/form/delete.html'
    edit_template = 'admin/form/edit.html'
    actions = None

    def __init__(self, model=None, name=None, category=None, endpoint=None, url=None):
        self.model = model
        if name is None:
            name = model._name

        if endpoint is None:
            endpoint = ('%s' % model._name).lower()

        super(ModelView, self).__init__(name, category, endpoint, url)

    def get_display_name(self):
        return self.model._name

    @expose('/', methods=('GET','POST',))
    def list(self):
        obj_list = self.model.all()
        return self.render(self.list_template, objects=obj_list, model=self.model)

    @expose('/+add/', methods=('GET', 'POST'))
    def add(self):
        return self.render(self.add_template)

    @expose('/<pkid>/delete', methods=('GET', 'POST'))
    def delete(self, pkid):
        return self.render(self.delete_template, )

    @expose('/<pk>/', methods=('GET', 'POST'))
    def edit(self, pkid):
        return self.render(self.edit_template)


class RootView(BaseView):
    @expose('/root/')
    def index(self, models = []):
        if not models:
            models = ModelRegistry.list()
        self.models = map(
                ModelRegistry.resolve,
                models
        )
        return self.render('form/root_view.html', models=self.models)
