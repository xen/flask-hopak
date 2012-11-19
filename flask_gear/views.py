# -*- coding: utf-8 -*-
#
from flask import render_template, g, request, redirect, url_for, flash
from functools import partial
from flask.views import View, MethodView
from formgear.models import ModelRegistry
from formgear.utils import form_dict

from . base import BaseView, expose

def view(*a, **kw):
    def view(f):
        f.rule_args = a, kw
        return f

    if a and callable(a[0]):
        f = a[0]
        a = a[1:]
        return view(f)

    return view

class HandlerView(View):
    @classmethod
    def register(cls, url_prefix=''):
        for fname in dir(cls):
            func = getattr(cls, fname)
            rule_args = getattr(func, 'rule_args', None)
            if rule_args is None:
                continue

            cls.add_rule(fname, url_prefix, *rule_args)

    @classmethod
    def add_rule(cls, fname, url_prefix, rule_a, rule_kw):
        defaults = rule_kw.get('defaults', {})
        defaults['_func'] = fname
        rule_kw['defaults'] = defaults

        mr_view = cls.as_view('%s.%s' % (cls.name,fname))
        url = url_prefix + rule_a[0]
        rule_a = rule_a[1:]
        app.add_url_rule(url, view_func=mr_view, *rule_a, **rule_kw)

    def dispatch_request(self, *args, **kwargs):
        fname = kwargs.pop('_func')
        func = getattr(self, fname, None)
        if func is None:
            return "No", 401

        if isinstance(func, type):
            func = func.as_view(fname, **self.next_args({}))

        return func(*args, **kwargs)

    def next_args(self, kw):
        return kw

def method_template(method = None, **kw):
    assert method is not None
    return render_template('form/%s.html' % method, **kw)


class ModelView(BaseView):
    """ Base model admin view """

    list_per_page = 20
    relation = []

    add_template = 'admin/form/add.html'
    edit_template = 'admin/form/edit.html'
    list_template = 'admin/form/list.html'
    delete_template = 'admin/form/delete.html'

    actions = None

    @expose('/', methods=('GET','POST',))
    def list(self):
        return "list"

    @expose('/+add/', methods=('GET', 'POST'))
    def add(self):
        return "add"

    @expose('/<pkid>/view', methods=('GET', 'POST'))
    def view(self, pkid):
        return "view %s" % pkid

    @expose('/<pkid>/delete', methods=('GET', 'POST'))
    def delete(self, pkid):
        return "delete"

    @expose('/<pk>/', methods=('GET', 'POST'))
    def edit(self, pkid):
        return "edit %s" % pkid

class RootView(BaseView):
    @expose('/root/')
    def index(self, models = []):
        if not models:
            models = ModelRegistry.list()
        self.models = map(
                ModelRegistry.resolve,
                models
        )
        return render_template('form/root_view.html', models=self.models)
