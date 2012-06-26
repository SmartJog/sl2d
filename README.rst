====
sl2d
====

sl2d is a dummy command line launcher monitoring tool written in Python.

It is used internally at SmartJog to stream audiovisual content from or
to the SmartJog Content Delivery Network.

sl2d was first designed to only take care of ffmpeg but it is not meant
to be locked to ffmpeg only.


License
=======

sl2d is released under the `GNU LGPL 2.1 <http://www.gnu.org/licenses/lgpl-2.1.html>`_.


Build and installation
=======================

Bootstrapping
-------------

sl2d uses autotools for its build system.

If you checked out code from the git repository, you will need
autoconf and automake to generate the configure script and Makefiles.

To generate them, simply run::

    $ autoreconf -fvi

Building
--------

sl2d builds like a typical autotools-based project::

    $ ./configure && make && make install


Development
===========

We use `semantic versioning <http://semver.org/>`_ for
versioning. When working on a development release, we append ``~dev``
to the current version to distinguish released versions from
development ones. This has the advantage of working well with Debian's
version scheme, where ``~`` is considered smaller than everything (so
version 1.10.0 is more up to date than 1.10.0~dev).


Authors
=======

sl2d was started at SmartJog by Gilles Dartiguelongue in 2009 as a full
rewrite or a shell script based solution running in screen sessions.
Various employees and interns from SmartJog fixed bugs and added
features since then.

* Clément Bœsch <clement.boesch@smartjog.com>
* Gilles Dartiguelongue <gilles.dartiguelongue@smartjog.com>
* Guillaume Camera <guillaume.camera@smartjog.com>
* Julien Castets <julien.castets@smartjog.com>
* Mathieu Dupuy <mathieu.dupuy@smartjog.com>
* Maxime Mouial <maxime.mouial@smartjog.com>
* Nicolas Noirbent <nicolas.noirbent@smartjog.com>
* Rémi Cardona <remi.cardona@smartjog.com>
* Thomas Meson <thomas.meson@smartjog.com>
