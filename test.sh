# This is a little script that runs the test file from a directory up, as Python requires.

cp test.py ..
cd ..
python test.py
rm test.py
