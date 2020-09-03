****************************
Mopidy-ChoosMoos
****************************

.. image:: https://img.shields.io/pypi/v/Mopidy-ChoosMoos.svg?style=flat
    :target: https://pypi.python.org/pypi/Mopidy-ChoosMoos/
    :alt: Latest PyPI version

.. image:: https://img.shields.io/circleci/build/gh/doronhorwitz/mopidy-choosmoos/master.svg?style=flat
    :target: https://app.circleci.com/pipelines/github/doronhorwitz/mopidy-choosmoos
    :alt: CircleCI build status

.. image:: https://img.shields.io/codecov/c/github/doronhorwitz/mopidy-choosmoos/master.svg?style=flat
   :target: https://codecov.io/gh/doronhorwitz/mopidy-choosmoos
   :alt: Test coverage

Mopidy extension to support the ChoosMoos NFC Raspberry PI Spotify Music Player


Installation
============

1) Install mopidy `as per the mopidy docs <https://docs.mopidy.com/en/latest/installation/>`_

2) Install dependencies::

    sudo apt-get install libasound2-dev

3) Install Mopidy-ChoosMoos::

    pip install Mopidy-ChoosMoos


Configuration
=============

Before starting Mopidy, you must add configuration for
Mopidy-ChoosMoos to your Mopidy configuration file::

    [choosmoos]
    enabled = true
    nfc_demo_app_location =
    next_pin_number = 3
    previous_pin_number = 4
    volume_up_pin_number = 1
    volume_down_pin_number = 2
    play_pause_pin_number = 5


Project resources
=================

- `Source code <https://github.com/doronhorwitz/mopidy-choosmoos>`_
- `Issue tracker <https://github.com/doronhorwitz/mopidy-choosmoos/issues>`_


Credits
=======

- Original author: `Doron Horwitz <https://github.com/doronhorwitz>`_
- Current maintainer: `Doron Horwitz <https://github.com/doronhorwitz>`_
- `Contributors <https://github.com/doronhorwitz/mopidy-choosmoos/graphs/contributors>`_
