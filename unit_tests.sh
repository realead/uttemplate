

export PYTHONPATH="${PYTHONPATH}:.."

(cd tests && python -m unittest discover -s . -v)



