# mpr

This is my Web Engineering Master Project at CVUT University.

The project is divided in 3 parts. The first one makes predictions about the Wikipedia links using their attributes to create the training model. This part is done and it was commited.

The second and the third part should be done as follows: The second one should be base on the structure of the Wiki pages. The third one should recognize some key workds from the Wiki page to create the model.

How to execute the Python script for the first part of the project from the command line.

python3 mprEx.py -t <traininginputfile> -p <predictioninputfile> -w
traininginputfile is the file with the entities that should be used to create the model associated with a domain. predictioninputfile is the file with the entitis that should have their domains predicted.
