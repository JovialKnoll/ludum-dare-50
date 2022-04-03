import jovialengine

import constants
import mode


class ModeFailDeath(mode.ModeOpening):
    __slots__ = (
        '_time',
        '_ready',
    )

    def __init__(self):
        super().__init__()
        self._time = 0
        self._ready = False
        self._background.fill(constants.BLACK)
        jovialengine.shared.font_wrap.renderToInside(
            self._background,
            (constants.SCREEN_SIZE[0] // 4, constants.SCREEN_SIZE[1] // 4),
            constants.SCREEN_SIZE[0] // 2,
            "death fail string",
            constants.WHITE,
            constants.BLACK
        )

    def _switchMode(self):
        if self._ready:
            self.next_mode = mode.ModeOpening1()

    def _update(self, dt):
        self._time += dt
        if self._time >= 2000 and not self._ready:
            jovialengine.shared.font_wrap.renderToCentered(
                self._background,
                (
                    constants.SCREEN_SIZE[0] // 2,
                    constants.SCREEN_SIZE[1] // 2 + constants.SCREEN_SIZE[1] // 4 + constants.FONT_SIZE // 2
                ),
                "press any key to try again",
                constants.WHITE,
                constants.BLACK
            )
            self._ready = True
