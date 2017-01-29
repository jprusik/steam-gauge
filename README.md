Steam Gauge
===========
[Steam Gauge](https://www.mysteamgauge.com) is a Python-based web app driven by [Flask](http://flask.pocoo.org/) that produces data-rich Steam account summaries. It makes use of Steam's Web API, Big Picture API, and metadata gathered using a (presently closed-source) Python app that scrapes data from the Steam Store pages (when necessary). That metadata is stored in a SQL database for easy retrieval by the Steam Gauge app. The app has undergone several revisions, including a migration from Python 2 to 3 and has subsequently been open-sourced. This repository represents work going forward from that migration (for security reasons, it does not include the full history of the original repo), and is presently being refactored to use better software design patterns.


Requirements
------------
- Python 3.4.5 or higher (earlier versions of Python 3 have not been tested)
- Package requirements can be found in `requirements.txt` and installed using pip (note, if you opt to use MySQL, you may have to download and make [`mysql-connector-python`](https://dev.mysql.com/downloads/connector/python/) manually)


Usage
-----
- create `config.py` in the app directory and give values to your app constants (see `config-example.py`)
- if you're running locally, run app.py from the app directory. Otherwise, refer to documentation on setting up and using [Passenger](https://www.phusionpassenger.com/) with your server.
- access with your client at `http://127.0.0.1:5000` by default


Limitations/Known Issues
------------------------
- The code is still a bit hairy in some places and can definitely benefit from some refactoring/optimization.
- Currently, there is no unit testing to mitigate regressions.
- User data accuracy reporting has external dependencies and is also a bit hacky.


Author
------
Jonathan Prusik @jprusik [www.classynemesis.com]
