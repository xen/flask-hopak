from hopak.widgets import WidgetRegistry, Widget


class WYSIWYGWidget(Widget):
    alter_names = ('wysiwyg',)
    template = 'wysiwyg'
    _type = 'wysiwyg'
    # resourses = (
    #     'wysihtml5/bootstrap-wysihtml5-0.0.2.css',
    #     'wysihtml5/bootstrap-wysihtml5-0.0.2.min.js',
    #     'wysihtml5/wysihtml5-0.3.0_rc2.min.js'
    #     )
