# UGLYHACK
import sys, os
mgba_root = "/home/joel/Documents/pokemon/mgba"
mgba_python_path = mgba_root + "/src/platform/python"
assert os.path.isdir(mgba_python_path), \
    "You must set the mgba_root manually ATM."
sys.path.append(mgba_python_path)
# ENDOFUGLYHACK

import mgba, mgba.core, mgba.image, mgba.gb

class Gameboy():
    def __init__(self, rom_path):
        core = mgba.core.loadPath(rom_path)
        core.reset()
        self._core = core

    def saveState(self, slot_int):
        flags = 0  # more options at mgba/include/mgba/core/serialize.h
        # https://github.com/mgba-emu/mgba/blob/master/src/core/core.c
        return mgba.lib.mCoreSaveState(self._core._core, slot_int, flags)

    def loadState(self, slot_int):
        flags = 0
        return mgba.lib.mCoreLoadState(self._core._core, slot_int, flags)

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

def _bytes_to_int(xs):
    return int.from_bytes(xs, byteorder='big')

def _int_to_bytes(n, length):
    return tuple(int.to_bytes(n, length=length, byteorder='big'))

def read_pokemon_state(gameboy):
    raw = gameboy._core.memory.u8
    info = {}
    info['money'] = _bytes_to_int(raw[0xd84e:0xd851])
    # refer to https://github.com/pret/pokecrystal/blob/master/wram.asm
    return info

KEY_A = mgba.gb.GB.KEY_A
KEY_B = mgba.gb.GB.KEY_B
KEY_UP = mgba.gb.GB.KEY_UP
KEY_LEFT = mgba.gb.GB.KEY_LEFT
KEY_DOWN = mgba.gb.GB.KEY_DOWN
KEY_RIGHT = mgba.gb.GB.KEY_RIGHT
KEY_SELECT = mgba.gb.GB.KEY_SELECT
KEY_START = mgba.gb.GB.KEY_START
