> # BWB
###### Ball & Wall & Ball

![icon](ico.ico)

> ### Description
Simple physics and graphics.
The first implementation of the light shader, a simplified kernel file, but everything you need to create a regular plane for rendering with almost no polygons\
It is a simple window with balls bouncing not only off the walls, but also from each other. All the logic of bounces is built in the model, the balls themselves as a class in py are used for calculations and data storage, and in glsl rendering\
##### Control keys
LMB - add ball on mouse position\
Space - add ball on vec2(100) position\
Esc - exit

> ### command on compilation
* pyinstaller:
```shell
pyinstaller --name "BWB" --icon="ico.ico" --add-data "C:/Program Files/Python311/Lib/site-packages/glcontext;glcontext" main.py
```
