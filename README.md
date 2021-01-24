# ChromaPython


## What is different from the original chroma-python repo?


Better code tracing & debugging with allogate, as well as generally easier to maintain code using proper class and inheritance structure.

For example, compare these two files which share the same functionality
- https://github.com/FlameOfIgnis/better-chroma-python/blob/master/ChromaPython/ChromaDevices.py
- https://github.com/chroma-sdk/chroma-python/blob/master/ChromaPython/ChromaDevices.py

I've seen that original repo has stopped responding to issues and pull requests about a year ago, so I've decided to create a fork an maintain it, rather than send a pull request.


## Example Use
```python
from chromasdk.ChromaPython import ChromaApp, ChromaAppInfo, ChromaColor, Colors, ChromaGrid

info = ChromaAppInfo()
info.DeveloperName = 'Ignis'
info.DeveloperContact = "Please don't"
info.Category = 'application'
info.SupportedDevices = ['keyboard', 'mouse', 'mousepad', 'headset']
info.Description = 'Sync Razer device colors with other components'
info.Title = 'A cool RGB toy'

app = ChromaApp(self.info)

c = ChromaColor(123,123,123)
app.Mouse.setStatic(c)
app.Headset.setStatic(c)
time.sleep(10)

```

## Extra features of this fork (so far)
- Await session
    Wait for session to fully open before finishing ChromaApp constructor, so that there is no race condition that can crash the application.
- Renegotiate bad connections
    When a session id and URL is given but does not work, re-negotiate the connection up to 3 times. 
- Better code all around in general.

### Rest of the readme from original repo
**###################################################################**

[![Build status](https://ci.appveyor.com/api/projects/status/5ihmbuppv3g29or2/branch/master?svg=true)](https://ci.appveyor.com/project/Vaypron/chroma-python-ee89l/branch/master)

## Disclaimer
This project is still in active development!

## Support

### Devices
```
Keyboard
Headset
Mouse
Headset
Keypad
ChromaLink
```

### BCA
#### Read
```
Keyboard
```
#### Write
```
.
```

## How to install

### Auto-Install with pip

```
Coming soon.
```

### Install with pip (currently recommended)

1. Clone the repository
2. Navigate into the directory and run:
```
pip install .
```

Pip should now install all necessary dependencies, as well as ChromaPython itself.

### By using the Source files:

Requirements:
```
requests
```
Can be installed by 
```
pip install requests
```

After installing requests, clone the repository and copy all files of the ChromaPython folder into your working directory. 


## Contributing
Feel free to contribute by reporting issues and/or extending the current code. You can do this by forking this project
and creating a pull request. Unfinished tasks can be found as "enhancement" issues.
Also, please always add comments to your changes/new code.

## How to use 

Take a look at ```Tests\checkall.py```. It should give you a good example on how to use it.
An example on how to use the BCA feature can be found in```Test\checkBinary.py```.
