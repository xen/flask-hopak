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
    def __init__(self, name, title, view, rule, category, visible=True):
        """ Action item initialisation
        """
        self.name = name
        self.title = title
        self.view = view
        self.rule = rule
        self.category = category
        self.visible = visible

class ActionRegistry(object):
    """ Action items registry with access. """

    def __init__(self):
        self._items = {}

    def add(self, action, replace=True):
        assert isinstance(action, ActionItem)
        if not self._items.has_key(action.name):
            self._items[action.name] = action


