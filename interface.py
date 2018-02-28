# UGLYHACK
import sys, os
mgba_root = "/home/joel/Documents/pokemon/mgba"
mgba_python_path = mgba_root + "/src/platform/python"
assert os.path.isdir(mgba_python_path), \
    "You must set the mgba_root manually ATM."
sys.path.append(mgba_python_path)
# ENDOFUGLYHACK

import mgba.core
import mgba.image

class Gameboy():
    def __init__(self, rom_path):
        core = mgba.core.loadPath(rom_path)
        core.reset()
        self._core = core

    def saveState(self, slot_int):
        flags = 0  # more options at mgba/include/mgba/core/serialize.h
        # https://github.com/mgba-emu/mgba/blob/master/src/core/core.c
        self._core._core.saveState(slot_int, flags)

    def loadState(self, slot_int):
        flags = 0
        self._core._core.loadState(slot_int, flags)

    def reset(self):
        self._core.reset()

    # run a few frames of the loaded game and store a screenshot
    def demo(self):
        image = mgba.image.Image(*self._core.desiredVideoDimensions())
        self._core.setVideoBuffer(image)
        self._core.reset()  # important step
        
        print('Running 800 frames.')
        for i in range(800):
            self._core.runFrame()
            
        print('Taking screenshot.')
        handle = open('demo.png', 'wb')
        image.savePNG(handle)
        handle.close()
            
        print('Success! Look in demo.png.')

    def setKeys(self, *keys):
        self._core.setKeys(*keys)
