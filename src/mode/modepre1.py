import jovialengine

import constants
import mode


class ModePre1(mode.ModeOpeningPause):
    __slots__ = (
    )

    def __init__(self):
        super().__init__()
        self._background.fill(constants.BLACK)
        jovialengine.shared.font_wrap.renderToInside(
            self._background,
            (constants.SCREEN_SIZE[0] // 8, constants.SCREEN_SIZE[1] // 8),
            constants.SCREEN_SIZE[0] // 2 + constants.SCREEN_SIZE[0] // 4,
            "WAVE 1 COMPLETED\n\nGood work out there pilot.\nAre you ready for wave 2?",
            constants.WHITE,
            constants.BLACK
        )

    def _switchMode(self):
        self.next_mode = mode.ModeFly1()

    def _whenReady(self):
        jovialengine.shared.font_wrap.renderToCentered(
            self._background,
            (
                constants.SCREEN_SIZE[0] // 2,
                constants.SCREEN_SIZE[1] // 2 + constants.SCREEN_SIZE[1] // 4 + constants.FONT_SIZE // 2
            ),
            "press any key to proceed",
            constants.WHITE,
            constants.BLACK
        )
