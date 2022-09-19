# A-level Project
## Online multiplayer poker website

This is a online poker muliplayer game which uses the http.server.BaseHTTPServer library to respond to HTTP requests from clients, the poker game is controlled and managed by events which define the next action for the specific table. All the data of the project is stored in a SQL table hosted on PostgreSQL with multiple normaslised tables.

## Setup
The main file for the package is locted in the poker folder, in the server.py script. However before you can run this script you will need to install some external modules and complete the following setup procedures.

To read further dicumentation about the package's modules view the full phinx documentation under /docs/_build/index.html.

### Prerequisits

The program is writen in the Python 3 programming language. You will need a working copy of a python interpretor which is avalaible at https://www.python.org/downloads/. In particular your python version must include the pip module which will be used to dowload othe neccessary requirements (more infomaton below).

The program also needs the PostgreSQL appication to be dowloaded to allow the program to access and create tables in a database. This software is avaliable at https://www.postgresql.org/download/. There is more infomatio under Settu about using this softwar in correlation with the project.
### Setup

To access this project on your computer you need to clone this repository to your device, this can be achieved by either:

1) Clone using the Git userinterface on the website https://github.com/TreeveWhite/alevel-project-online-poker.

2) Clone using commands.

```bash
$ git clone https://github.com/TreeveWhite/alevel-project-online-poker
```

Once you have the project on your local system, install the requirements.

```bash
$ cd alevel-project-online-poker
$ py -m pip install -r requiremets.txt
```

Once you have the requirements, run the database sdk which will initialise the tables and fill them with the neccessary infomation for the program to be run.

```bash
$ cd alevel-project-online-poker
$ cd poker
$ py DDL.py
```
### Running the Program

Ensure you have installed all the requirements discussed above before running the app using:

```bash
$ cd alevel-project-online-poker
$ cd poker
$ py server.py
```

Once the program is running your can view the application by navigating to http://localhost:8080/. If your wish for connections to be made with the server from outside our local machine then you will need to redrect this local port through toa public one. (A simple yet basic slution for this is using ngrok).

## License

The package is licensed using the MIT license, see LOCENSE doc for further details.

Author: Treeve G. White
