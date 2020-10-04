NVIDIA X Skoltech Hackaton Solution by SHREK2 team
--------------------------------------------------


Install
-------

.. code:: bash

    $ git clone https://github.com/sverdoot/search_network.git
    $ cd search_network


Then, you can run the server running these commands:

.. code:: bash

    $ pip install -r requirements.txt
    $ python app.py

We provide two urls by
default:

    -  <localhost>/ : the form of the search engine
    -  <localhost>/database : raw content of the test database

<localhost> is often http://127.0.0.1:5000.


Search filters
--------------

Search by name: "William"

Search with filters: "none, persons True, projects True, ideas False, skills Linux, Automation"
