LightBulb
=========

LightBulb is my latest Python project. When complete, it will enable you to compile a
LAMP stack (well, a web server, a few scripting languages and a database server)
without having to write your own configure parameters and play with Makefiles.

Note: it's still very much in development and is far from being complete. In fact, at
the time of writing, I'm still only just planning out the build profile format and how
we're going to modularise the various different applications and utilities you'll be
able to compile.

Requirements
------------

* CentOS/RHEL 5+, more coming soon
* [Elevator](http://github.com/LukeCarrier/elevator) for permission elevation
* Python 3.x, preferably 3.2.1, I'll extend support soon
* PyYAML, required for profile parsing (available in PyPI as PyYAML)
* Working tarfile module (compile with zlib-devel package and zlib enabled in /Modules/Setup)
* Possibly more, I'll update this list if I find any

Basic usage
-----------

Just a demo of the basic functionality I've implemented so far (building nginx, that's all):

    python3.2 src/__init__.py build -p support/profiles/example-nginx-phpfpm.yaml
