====================
Is-It-In-RHEL
====================

:Author: Pierre-Yves Chibon
:Contact: pingou@fedoraproject.org
:Version: 1.0
:License: GPLv2 or any later version

`is-it-in-rhel` is a command line utility to find out if a specific package
    is packaged in RHEL or not.

.. contents::

Install Prerequisites
~~~~~~~~~~~~~~~~~~~~~
::
  yum install python-requests


Get and Run the Source
~~~~~~~~~~~~~~~~~~~~~~~~
::
  git clone https://pagure.io/is-it-in-rhel.git
  cd is-it-in-rhel
  python is-it-in-rhel.py

Arguments
~~~~~~~~~

Use the ``--release`` option to restrict searching to a specific RHEL release:

    $ python is-it-in-rhel.py kernel --release 7
    kernel is in RHEL 7;   version: 3.10.0;   archs: noarch, ppc64, x86_64


Use the ``--search`` option to allow imperfect match:

::

    $ python is-it-in-rhel.py turbogears --search --release 6
    TurboGears2 is in RHEL 6;   version: 2.0.3;   arch: noarch


Use the ``--channel`` option to see in which channel the package can be found:

::

    $ python is-it-in-rhel.py gnome-terminal --channel --release 7
    gnome-terminal is in RHEL 7;   version: 3.8.4;   archs: ppc64, x86_64;   channels: rhel-7-for-power-rpms, rhel-7-server-rpms
