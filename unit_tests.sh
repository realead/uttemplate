

export PYTHONPATH="${PYTHONPATH}:.."

echo "Testing Python2:"
(cd tests && python2 -m unittest discover -s . -v)


echo "Testing Python3:"
(cd tests && python3 -m unittest discover -s . -v)

