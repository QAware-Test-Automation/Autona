# AUTONA - UI automation server (Python 3)
# Copyright (C) 2021 Marco Alvarado
# Visit http://qaware.org

from automator import Automator

import autopy
from language_en_autopy import languageButtons, languageKeys, languageModifierKeys

screenFile = 'screen.png'



class AutomatorAutoPy(
    Automator):

    def MovePointer(
        self,
        x, y,   # pixels
        smooth = True):

        # Adjust position to screen size.
        scale = autopy.screen.scale()
        width = autopy.screen.size()[0] * scale
        height = autopy.screen.size()[1] * scale
        if x < 0: x = 0
        if y < 0: y = 0
        if x >= width: x = width - 1
        if y >= height: y = height - 1

        if smooth:
            autopy.mouse.smooth_move(x / scale, y / scale)
        else:
            autopy.mouse.move(x / scale, y / scale)



    def ClickButton(
        self,
        button,
        toggle = False, down = True):

        _button = self.Button(button)
        if toggle:
            autopy.mouse.toggle(_button, down)
        else:
            autopy.mouse.click(_button)



    def TapKeys(
        self,
        keys,   # : array
        toggle = False, down = True):

        # Get main key from the end.
        key = self.Key(keys[-1])

        # Add modifier keys from the beginning.
        modifiers = []

        if len(keys) > 1:
            for i in range(len(keys) - 1):
                modifier = self.ModifierKey(keys[i])
                if modifier: modifiers.append(modifier)
            
        if toggle:
            autopy.key.toggle(key, down, modifiers)
        else:
            autopy.key.tap(key, modifiers)



    def CaptureScreen(
        self):

        bitmap = autopy.bitmap.capture_screen()
        bitmap.save(screenFile, 'png')
        bytes = open(screenFile, 'rb').read()
        return bytes



    def ScreenSize(
        self):

        scale = autopy.screen.scale()
        width = autopy.screen.size()[0] * scale
        height = autopy.screen.size()[1] * scale
        return (int(width), int(height))



    def Button(
        self,
        name):

        try:
            return languageButtons[name]
        except:
            pass



    def Key(
        self,
        name):

        try:
            return languageKeys[name]
        except:
            return name



    def ModifierKey(
        self,
        name):

        try:
            return languageModifierKeys[name]
        except:
            pass