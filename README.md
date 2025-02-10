# Common repo for creating new DRF projects

To create a .env file, you need to create a virtual environment first:

`python -m venv venv`

Then activate it:

`.\venv\Scripts\activate` — for Windows;

`source venv/bin/activate` — for Linux/MacOS.

(Or you can just google it 😉)

Next, install the requirements:

`pip install -r requirements.txt`

This file contains the most useful libraries for working. If you need to add your own, do so and then run the command above again.

After that, to create the .env file, run:

`python .\configure.py`

and follow the instructions.