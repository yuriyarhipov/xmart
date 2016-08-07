#install packages:
sudo apt-get install unzip unrar p7zip-full
sudo apt-get install libxml2-dev libxslt1-dev
pip install -r req.txt

#start app
guicorn xmart_parser.wsgi
