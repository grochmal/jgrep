README for unixjsons
====================

unixjsons - tools to operate on JSON logs as streams.


Copying
-------

Copyright (C) 2014 Michal Grochmal

This file is part of unixjsons.

unixjsons free software; you can redistribute and/or modify all or some of the
snippets under the terms of the GNU General Public License as published by the
Free Software Foundation; either version 3 of the License, or (at your option)
any later version.

unixjsons is distributed in the hope that they will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

The COPYING file in the root directory of the project contains a copy of the
GNU General Public License. If you cannot find this file, see
<http://www.gnu.org/licenses/>.


Project wise TODOs
------------------

Thing that would be useful to have.

* Add a configure script (`setup.py`) to check for correct python version, and
  provide PREFIX installation
* Add make to build symlinks (i.e. jgrep instead of jgrep.py)
* Add make install command


The tools
---------

There are implementations of `grep`, `cut`, `sed`, `echo` and `join` to work on
JSON formatted logs or any other files that have a JSON encoded on each line.

`jgrep` is an implementation of `grep` and `egrep`.  Instead of a single
regular expression to search for in a stream, it uses two separate regular
expressions: one to match against the *key* in the stream and one to match
against the *value* of matched keys.

`jcut` is an implementation of `cut`.  But contrary to the `cut` command the
`-f` flag receives the names of the *keys* in the stream, instead of numbers of
the fields.

`jsed` is a simplified implementation of the `sed` command.  It implements the
`s///` substitution command for several key and value pair combinations.  Both
keys and values can be matched and/or changed using substitution regular
expressions.

`jecho` is a combination of the `echo` and `cat` commands.  `jecho` can both
concatenate streams (as `cat` does) and add new *keys* and *values* to the
stream (as `echo` does).

`jjoin` is a combination of the `join` and `paste` commands.  It works as
`paste` if the *keys* in the two streams are all different, but if a *key* is
found in both streams the *values* for that key from both streams are joined
(this is behaviour similar to `join`).

