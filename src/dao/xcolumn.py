class SqlModeColumnClass():

    def __init__(self, _type, _limit, _default):
        self._type = _type
        self._limit = _limit
        self._default = _default

    def _json(self):
        return dict(_type=self._type, _limit=self._limit, _default=self._default)

    @staticmethod
    def get_verchar255():
        return SqlModeColumnClass(_type="verchar", _limit=255, _default="")

    @staticmethod
    def get_int9():
        return SqlModeColumnClass(_type="int", _limit=10, _default=0)

