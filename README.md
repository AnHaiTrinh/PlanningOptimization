# CBUS
## Description
There are n passengers *1,2, ...,n*. The passenger *i* want to travel from point *i* to point *i + n* (*i = 1,2, ...,n*). There is a bus located at point *0* and has *k* places for transporting the passengers (it means at any time, there are at most *k* passengers on the bus). You are give the distance matrix *c* in which *c(i, j)* is the travelling distance from point *i* to point *j* (*i,j = 0,1, ...,2n*). Compute the shortest route for the bus, serving n passengers and coming back to point *0*.
### Input 
- The first line contains *n* and *k* (1 &le; n &le; 11, 1 &le; *k* &le; 10).
- Line *i + 1* (*i = 1,2,..., 2n + 1*) contains the *(i - 1)*-th row of the matrix *c* (rows and columns are indexed from *0,1,2,...,2n*).
### Output
- Unique line contains the length of the shortest route.
## Installation
Make sure you have Git and Python3 installed.
```bash
git clone https://github.com/AnHaiTrinh/PlanningOptimization.git

# Create virtual environment
pip3 -m venv venv

# Activate virtual environment
venv\Scripts\activate # Windows
source venv/bin/activate # Linux

# Install required dependencies
pip install -r requirements.txt
```
## Run project
```bash
cd src
python main.py --filename [filename] --solver [solver]
```
For more information, run:
```bash
python main.py --help
```