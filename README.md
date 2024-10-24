# Rhythm Keys
School project rhythm game

## In this document

- Explenation
- System requirements / compatibility
- How to run
- Sources

### Explenation

**Rhythm Keys** is an engaging game developed using **Python** along with the additional **Pygame** module. Here's an overview of its architecture and functionality:

#### Performance and Resolution

- The game runs at a consistent **60 FPS** and supports a fixed **1080p (Full HD)** resolution.
- Users have the flexibility to scale the resolution internally to suit their needs, including options for **720p HD**, **1440p QHD**, and **4K UHD**.

#### Game Architecture

The game is structured in a hierarchical manner, which allows for efficient management of various components. Here's a breakdown of the key systems involved:

1. **Main Loop**
   - The main loop is responsible for orchestrating the gameplay by calling the **Screen Manager**.

2. **Screen Manager**
   - The **Screen Manager** sets up the virtual screen at **1080p**, ensuring that all rendered content is automatically scaled based on the user's selected resolution. This alleviates the need for manual scaling when switching resolutions.

3. **Scene Manager**
   - The **Scene Manager** handles loading, unloading, and managing different scenes throughout the game. It acts as a control center for scene transitions.

4. **Scenes**
   - Each scene is represented by a dedicated class that contains the following methods:
     - `handle_events()`: Responsible for processing user input and events.
     - `draw()`: Responsible for rendering graphics to the virtual screen.

#### Components

Within each scene, there are various **components** designed to represent UI elements such as input fields and buttons. Here are some key features of components:

- **Reusable**: Components can be easily instantiated and reused across different scenes.
- **Methods**:
  - `draw()`: For rendering the component on the screen.
  - `event_handler()`: For handling user interactions. Note that not all components require this method, and it's optional based on the component's functionality.

#### Global Variables and Utilities

To manage global state and utility functions, the game utilizes dedicated modules:

- **global_vars.py**: This module is responsible for handling global variables that need to persist between scenes.
- **utils.py**: This module contains general-purpose functions that assist with various tasks throughout the game.

### Example Code Snippets

Scene class on which all scenes are based on:

```python
# Scene parent class
class Scene:
    def __init__(self, manager):
        self.manager = manager #to allow th scene to call a scene change

    def handle_event(self, event):
        pass

    def update(self):
        pass

    def draw(self, surface):
        pass
```

By structuring the game in this way, **Rhythm Keys** ensures an organized codebase that is both scalable and maintainable, allowing developers to enhance and expand the game effectively.

### System requirements / compatibility

#### Python (not required when running the binary)
- Python 3.8 and up

#### pygame (not required when running the binary)
- pygame 2.x.x

#### TK aka TKinter (not required when running the binary)
- must be present (full package)

#### Windows / NT
- Windows 8.1 and higher

#### Linux
- Supports Linux distros with python 

#### MacOS / Darwin / XNU
- Does currently not support MacOS

#### Other OSes untested

#### Native environment
Thythm Keys was developed on Python 3.12.3 with pygame 2.6.1 on both NT and Unix systems.

### How to run

To get started with the game, choose the appropriate executable based on your operating system. You can either run the **Windows binary** or the **Unix executable**, both located in the root of the project directory. **It's important to keep the directory structure intact.**

#### Running the Project Directly

If you prefer to run the script directly instead of using the precompiled executables, you can execute **main.py**. This script will automatically detect any missing modules and prompt you to attempt the automatic installation.

**Note for Linux Users**: If your Python installation is system-wide, please take the necessary precautions to avoid any potential issues when installing new modules.

### souces
#### arrow icons
- https://www.iconarchive.com/artist/custom-icon-design.html
#### star icon
- https://www.freepik.com/author/smashicons/icons
#### additional icons
- https://iconduck.com/sets/feather-icons