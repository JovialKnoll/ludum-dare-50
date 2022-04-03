import jovialengine

import constants
import mode


class ModeFailDeath(mode.ModeOpeningPause):
    __slots__ = (
    )

    def __init__(self):
        super().__init__()
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
        self.next_mode = mode.ModeFly0()

    def _whenReady(self):
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
