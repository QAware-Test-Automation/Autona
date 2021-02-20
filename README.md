# Autona
Automate machines from your browser. Send UI commands such as keystrokes, simulate mouse clicks, run apps and more, with a simple HTTP server.

**Languages**: backend in Python 3, frontend in JavaScript (HTML5), AutoIt standalone in BASIC-like scripting

## Syntax
Write text to be typed and special commands inside braces {}. Examples:

Open notepad (in Windows), wait 5 seconds for the application to show up, and type "Hello World!":
```
{open notepad}{wait 5}Hello World!
```

Move the mouse cursor to a position in the screen (x, y in pixels) and left-click twice:
```
{move 720 480}{clk_lft}{clk_lft}
```

Send special keystrokes or hotkeys:
```
{ctrl a}{ctrl c}{alt tab}{ctrl v}
```

Customize commands to your own language and preferences.

## Supported libraries
Different automation libraries have advantages and drawbacks in various systems, check their documentation and Issues section:

* [AutoPy](https://github.com/autopilot-rs/autopy#installation) (Linux/MacOS/Windows)
* [PyAutoGUI](https://github.com/asweigart/pyautogui) (Linux/MacOS/Windows)
* [AutoIt](https://www.autoitscript.com/site/autoit/downloads/) (Windows with standalone executable)

Or add your preferred library.