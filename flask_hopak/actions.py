class ActionItem(object):
    """ ActionItem provides container for admin interface menus.
    Params:

    * name - item callable name, id
    * title —  text title, for users
    * view — where is action point to
    * category — way to group actions
    * visible — is action visible to user
    * rule — is meet condition?
    * permission? — OK this is not ready
    """
    def __init__(self, name, view, visible=True):
        """ Action item initialisation
        """
        self.name = name
        self.view = view
        self.children = []
        self.children_urls = set()
        self.cached_url = None
        self.visible = visible

    def get_url(self):
        if self.cached_url:
            return self.cached_url

        self.cached_url = url_for('%s.%s' % (self.view.endpoint, self.view._default_view))
        return self.cached_url

    def is_active(self, view):
        if view == self.view:
            return True

    def is_accessible(self):
        if self.view is None:
            return False

        return self.view.is_accessible()

class ActionRegistry(object):
    """ Action items registry with access. """

    def __init__(self):
        self._items = {}

    def add(self, action, replace=True):
        assert isinstance(action, ActionItem)
        if not self._items.has_key(action.name):
            self._items[action.name] = action


