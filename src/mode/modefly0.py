from .modefly import ModeFly


class ModeFly0(ModeFly):
    __slots__ = (
    )

    def __init__(self):
        super().__init__()

    def _getSpawnWait(self):
        return 3000
