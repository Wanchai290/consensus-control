# Consensus control and CBF experiments
## Usage

Python files should be run from the root folder (where `ibuki_lab` and  `src` reside)
and launched in one of the following manners

```bash
# Method 1: Running as module
python3 -m src.discrete

# Method 2: Declaring root folder in `PYTHONPATH` temporarily
## Temporarily
PYTHONPATH=$PYTHONPATH:$PWD python3 src/discrete.py

## During this bash session
export PYTHONPATH=$PYTHONPATH:$PWD
python3 src/discrete.py
```

for the `src/discrete.py` file. This was necessary to be able to use the `src` folder as a module.

# Available scripts
