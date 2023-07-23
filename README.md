# Carpool-Creator

A basic python application created to solve the issue of assinging drivers and riders when organizing carpooling large groups. 

![Pylint Status](https://github.com/github/docs/actions/workflows/pylint.yml/badge.svg?event=push)
![Test Status](https://github.com/github/docs/actions/workflows/unittest.yml/badge.svg?event=push)

_Note: In this readme all python commands use python3 as this project was developed in a Linux environment. This project should execute in other operating systems provided the proper keyword for running python is used._

## To Use
Create a csv file with columns named 'Driver', 'Capacity' and 'Rider'. Fill the spreadsheet with the names of the drivers, how many riders they can carry, and the name of every rider. 

Then, run the command `python3 src/main.py <input_csv_file_path> <output_csv_file_path>` from within the root directory of the project. 

The script will pair up riders and then write the result to the specified output csv file. The output csv file will have driver's names as columns and the entries below will be the people riding with that driver. 

## To Setup For Development
Begin by cloning this repository using `git clone https://github.com/Sn00pyW00dst0ck/Carpool-Creator.git`. 

The `src` directory contains the project's main executable code, and the `test` directory contains all unit tests. 

### Running Unit Tests
To run unit tests, execute the command `python3 -m unittest` from within the terminal of the root directory of the project. 
