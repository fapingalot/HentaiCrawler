# HentaiCrawler
A tool for downloading from hentai sites:
- Thatpervert.con
- Simplyhentai.com
- Shadbase.com
- XCartX.com

# Install
Install the linux dependencies
`` sudo pacman -S wget xclip``

Install the python packages
`` pip install -r requirements.txt ``


# Use
In the /bin folder:
- ``xcartx [<url or url without the hostname>]``            - If the url is empty it will use clipboard
- ``simply-hentai [<url or url without the hostname>]``     - If the url is empty it will use clipboard
- ``thatpervert [<url or url without the hostname>]``       - If the url is empty it will use clipboard
- ``shadbase``

The bin files that accept input save the input in a json in ``saves/`` folder.
And you can download all saved with the scripts in the ``bin/update/`` folder


## ONLY FOR LINUX NEEDES: curl, xclip
