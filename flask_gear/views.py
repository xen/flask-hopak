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



# class ModelView(HandlerView):
#     name = 'model'
#     def dispatch_request(self, *args, **kwargs):
#         if not hasattr(self, 'model'):
#             assert 'model' in kwargs
#             name = kwargs.pop('model', None) or self.model_name
#             self.model = ModelRegistry.resolve(name, False)

#         if not self.model:
#             return "No", 404

#         return super(ModelView,self).dispatch_request(*args, **kwargs)

#     def next_args(self, kw):
#         kw['model'] = self.model
#         return super(ModelView, self).next_args(kw)

#     tpl_create = partial(render_template, 'gearviews/model_add.html')
#     @view("/+add")
#     def add(self,):
#         return self.tpl_create(form=self.model, model=self.model)

#     @view("/+add", methods=["POST"])
#     def add_post(self):
#         obj = self.model(request.form)

#         if not obj.validate():
#             return self.tpl_create(model=self.model, form=obj)

#         key = obj.save()
#         return redirect(url_for('formgear.model.one',
#             model=obj._name, key=key))

#     @view('/<key>')
#     def one(self, key, **kw):
#         obj= self.model.get(key = key)
#         if not obj:
#             return "no %s" % (self.model._name,), 404

#         return self.show(obj)

#     tpl_edit = partial(render_template, 'gearviews/model_edit.html')
#     def show(self, obj):
#         return self.tpl_edit(object=obj, model=self.model, form=obj)

#     @view('/<key>', methods=['POST'])
#     def edit(self, key,):
#         obj= self.model.get(key = key)
#         obj.update(request.form, raw=False)
#         if not obj.validate():
#             return self.show(obj)

#         obj.save()
#         return redirect(url_for('formgear.model.one',
#             model=obj._name, key=key))

#     tpl_list = partial(render_template, 'gearviews/model_list.html')
#     @view('/')
#     def all(self,):
#         obj_list = self.model.all()
#         return self.tpl_list(objects=obj_list, model=self.model)

#     @view('/', methods=['POST'])
#     def all_edit(self,):
#         many = form_dict(request.form.items())
#         err = False
#         obj_list = []
#         for key,data in many['table'].items():
#             obj = self.model.get(key)
#             obj.update(data)

#             if obj.validate():
#                 obj.save()
#             else:
#                 err = True

#             obj_list.append(obj)

#         if err:
#             return self.tpl_list(objects=obj_list, model=self.model)

#         flash("Saved")
#         return redirect(url_for('formgear.model.all', model=self.model._name))

# ModelView.register('/<model>')

# # XXX app.before_request (bluprint context) is broken
# @app.before_app_request
# def check_user(*args, **kwargs):
#     if not request.url_rule:
#         return

#     # XXX: ya black magic
#     if not request.url_rule.endpoint.startswith('formgear.'):
#         return

#     from flaskext.auth.auth import get_current_user_data, not_logged_in
#     if get_current_user_data() is None:
#         return not_logged_in(None, *args, **kwargs)

# @app.app_context_processor
# def ep_name_ctx():
#     if not request.url_rule:
#         return {}

#     return {
#         "me": _me,
#     }

# class Me(object):
#     def __call__(self, f=None):
#         ep = request.url_rule.endpoint
#         #print(ep)
#         ep = ep[:ep.rindex('.')]
#         if f:
#             ep = str.join(".", [ep,f])
#         return ep

#     def __getattr__(self, name):
#         return self(name)

# _me = Me()


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
