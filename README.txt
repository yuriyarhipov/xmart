#install packages:
pip install -r req.txt

#start app
guicorn xmart_parser.wsgi
