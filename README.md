# Autona

## Introduction
Automate machines from your browser. Send UI commands like keystrokes, simulate mouse clicks, run apps and more, with a simple HTTP server you can customize.

## UI Automation

### Syntax
Write text to be typed and special commands inside braces {}. 

For example, to open notepad (in Windows), wait 5 seconds for the application to show up, and type "Hello World!":
```
{open notepad}{wait 5}Hello World!
```

Move the mouse cursor to a position in the screen (x, y in pixels):
```
{move 720 480}
```

Left click twice at current cursor position:
```
{clk_lft}{clk_lft}
```

Send a special keystroke or hotkey:
```
{cmd tab}
```

Customize commands to your own language and preferences.

### Supported libraries
Different automation libraries have advantages and drawbacks in various systems, check their documentation and issues:

* [AutoPy](https://github.com/autopilot-rs/autopy#installation) (Linux/MacOS/Windows)
* [PyAutoGUI](https://github.com/asweigart/pyautogui) (Linux/MacOS/Windows)
* [AutoIt](https://www.autoitscript.com/site/autoit/downloads/) (Windows with standalone application)

Or add your preferred library.