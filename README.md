# Coding Interview Challenge

## How to Run

```bash
python mySolution.py [input_file]
```

Here's the help output:

```bash
usage: mySolution.py [-h] problemFile

positional arguments:
  problemFile  File to process

options:
  -h, --help   show this help message and exit
```

To run with the `evaluateShared.py` test script, run:

```bash
python .\evaluateShared.py --cmd "python .\mySolution.py" --problemDir [DIR]
```

## Troubleshooting

If you encounter an issue with solutions including `\r` characters, edit the `loadSolutionFromString()` function in `evaluateShared.py` to include the following line:

```python
def loadSolutionFromString(solutionStr):
    schedules = []
    buf = io.StringIO(solutionStr)
    while True:
        line = buf.readline()
        if len(line) == 0:
            break
        if ('[' not in line) or (']' not in line):
            return schedules, "Solution format incorrect. Expected all lines to be in format [{load_id}, {load_id}, ...], but got this: " + line
        line = line.replace('[','')
        line = line.replace(']','')
        line = line.replace('\n','')
        line = line.replace(' ','').rstrip() # <-- Changed this line to fix `/r` in solution
        splits = line.split(',')
        schedule = []
        for loadID in splits:
            schedule.append(loadID)
        schedules.append(schedule)
    return schedules, ""
```

This should only be an issue on Windows.

## Sources Used

- https://www.geeksforgeeks.org/traveling-salesman-problem-tsp-implementation/
- https://www.geeksforgeeks.org/traveling-salesman-problem-tsp-in-python/
- https://colab.research.google.com/github/cvxpy/cvxpy/blob/master/examples/notebooks/WWW/mTSP_en.ipynb
- https://github.com/afourmy/pyTSP
- https://medium.com/@suryabhagavanchakkapalli/solving-the-traveling-salesman-problem-in-python-using-the-nearest-neighbor-algorithm-48fcf8db289a
- https://stackoverflow.com/questions/53275314/2-opt-algorithm-to-solve-the-travelling-salesman-problem-in-python
- https://arthur.maheo.net/python-local-tsp-heuristics/
- https://github.com/norvig/pytudes/blob/main/ipynb/TSP.ipynb