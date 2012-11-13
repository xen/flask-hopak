# -*- coding: utf-8 -*-
#
import formgear
from formgear.ds import register_datasource
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


class Admin(object):
    """
        Collection of the views. Also manages menu structure.
    """
    def __init__(self, app=None, name=None, url=None, index_view=None,
                 translations_path=None):
        """
            Constructor.

            `app`
                Flask application object
            `name`
                Application name. Will be displayed in main menu and as a page title. If not provided, defaulted to "Admin"
            `index_view`
                Home page view to use. If not provided, will use `AdminIndexView`.
            `translations_path`
                Location of the translation message catalogs. By default will use translations
                shipped with the Flask-SuperAdmin.
        """
        self.app = app

        self.translations_path = translations_path

        self._views = []
        self._menu = []
        self._menu_categories = dict()
        self._models = []

        if name is None:
            name = 'Admin'
        self.name = name

        if url is None:
            url = '/admin'
        self.url = url

        # # Index view
        # if index_view is None:
        #     index_view = AdminIndexView(url=self.url)

        # self.index_view = index_view

        # # Add predefined index view
        # self.add_view(index_view)

        # if app:
        #     self._init_extension()

    def add_datasource(self, datasource, connection, alias, **kwargs):
        register_datasource(datasource=datasource,
            connection=connection,
            alias=alias,
            **kwargs)

    def model_backend(self,model):
        for backend in self._model_backends:
            if backend.model_detect(model): return backend
        raise Exception('There is no backend for this model')

    def add_model_backend(self,backend):
        self._model_backends.append(backend)

    def register (self,model, admin_class = None,*args,**kwargs):
        """
            Register model to the collection.

            `model`
                Model to add.
            `admin_class`
                ModelAdmin class corresponding to model.
        """
        from flask_superadmin.model import ModelAdmin

        admin_class = admin_class or ModelAdmin
        model_view = admin_class(self, model,*args,**kwargs)
        self._models.append((model, model_view))
        self.add_view(model_view)


    def add_view(self, view):
        """
            Add view to the collection.

            `view`
                View to add.
        """
        # Add to views
        self._views.append(view)

        # If app was provided in constructor, register view with Flask app
        if self.app is not None:
            self.app.register_blueprint(view.create_blueprint(self))
            self._add_view_to_menu(view)

    def locale_selector(self, f):
        """
            Installs locale selector for current ``Admin`` instance.

            Example::

                def admin_locale_selector():
                    return request.args.get('lang', 'en')

                admin = Admin(app)
                admin.locale_selector(admin_locale_selector)

            It is also possible to use the ``@admin`` decorator::

                admin = Admin(app)

                @admin.locale_selector
                def admin_locale_selector():
                    return request.args.get('lang', 'en')

            Or by subclassing the ``Admin``::

                class MyAdmin(Admin):
                    def locale_selector(self):
                        return request.args.get('lang', 'en')
        """
        if self.locale_selector_func is not None:
            raise Exception('Can not add locale_selector second time.')

        self.locale_selector_func = f

    def _add_view_to_menu(self, view):
        """
            Add view to the menu tree

            `view`
                View to add
        """
        if view.category:
            category = self._menu_categories.get(view.category)

            if category is None:
                category = MenuItem(view.category)
                self._menu_categories[view.category] = category
                self._menu.append(category)

            category.add_child(MenuItem(view.name, view))
        else:
            self._menu.append(MenuItem(view.name, view))

    def init_app(self, app):
        """
            Register all views with Flask application.

            `app`
                Flask application instance
        """
        if self.app is not None:
            raise Exception('Flask-SuperAdmin is already associated with an application.')

        self.app = app

        for view in self._views:
            app.register_blueprint(view.create_blueprint(self))
            self._add_view_to_menu(view)

        self._init_extension()

    def _init_extension(self):
        if not hasattr(self.app, 'extensions'):
            self.app.extensions = dict()

        if 'admin' in self.app.extensions:
            raise Exception('Can not have more than one instance of the Admin class associated with Flask application')

        self.app.extensions['admin'] = self

    def menu(self):
        """
            Return menu hierarchy.
        """
        return self._menu