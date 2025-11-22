# Consensus control and CBF experiments
## Requirements
Basic behaviour requirements described in `requirements.txt`.
To use the main script of `cbf.py` and `formation.py`, you will need to install
Protobuf and the [grSim simulator](https://github.com/RoboCup-SSL/grSim).
Once installed, please follow [this setup](src/ssl_traj/README.md)

## Usage
Python files should be run from the root folder (where `ibuki_lab` and  `src` reside)
and launched in one of the following manners

```bash
# Method 1: Running as module
python3 -m src.discrete
```

```bash
# Method 2: Declaring root folder in `PYTHONPATH`
## a) Temporarily
PYTHONPATH=$PYTHONPATH:$PWD python3 src/discrete.py
```

```bash
## b) During this bash session
export PYTHONPATH=$PYTHONPATH:$PWD
python3 src/discrete.py
```

for the `src/discrete.py` file. This was necessary to be able to use the `src` folder as a module.

# Available scripts
## `continuous.py` | Continuous consensus
Single function achieving consensus algorithm applied in 1D. An array of relative offsets can be specified between agents.

## `discrete.py` | Discrete-time consensus
Two ways to achieve discrete-time consensus
We always consider the dynamics `x(k+1) = x(k) + u(k)` in the following functions.
The main script of the file will just plot a simulation of discrete-time consensus over given time steps.

- `discrete_consensus_cfunc()`
This function returns the control values `u(k)` to apply to the system
to drive it to a consensus value.

- `discrete_consensus_step()`
Taking the same parameters as the previous function, this will return
the vector of the state `x(k+1)` when provided with the current state `x(k)`.
This version uses the Perron matrix used for stability analysis to compute the next state.

- `discrete_consensus_sim_complete()`
Simple wrapper to run discrete-time consensus for given steps. Returns the vector of all states `x(k)` for k in `[0, num_steps]`

## `cbf.py` | CBF (Control Barrier Functions)
Implementation of the Zeroing CBF method as a Quadratic Program (QP) problem, used for collision avoidance.
Before running this script, you need to install the [grSim](https://github.com/RoboCup-SSL/grSim) simulator,
install Protobuf gencode version <= 29, and run the following scripts :
```bash
pip install -r ssl_traj/requirements.txt
./ssl_traj/generate_protobuf.sh 
```

*Note: if this directory is empty, use this command to make it appear*
```bash
git submodule update --init --recursive
```

The function `zeroing_cbf()` takes a nominal speed vector `v`, and returns the solution obtained by the QP solver,
which is the adapted speed value `v_safe` to use for collision avoidance.
The last parameter of this function must be a list of `Obstacle` objects, defined in the same module.

Function `obstacles_except()` is used to generate obstacles from data provided by the grSim simulator,
so we can apply CBF in that simulator.

## `formation.py` | 2D formation control in grSim
Runs the discrete-time consensus algorithm by applying it on the (x, y) positions of robots.
To use it, install the [grSim](https://github.com/RoboCup-SSL/grSim) simulator as well as Protobuf installed, and follow [this setup](./src/ssl_traj/README.md)

The main script will make robot 0 in grSim move to the `target` location while avoiding all other robots using the CBF
technique.

## `data/`
After running the consensus algorithm with drones, using the configuration provided by the Ibuki laboratory at Meiji University,
position data has been collected over time to measure the performance of the consensus algorithm.
This data has been collected using the discrete-time version of consensus algorithm. Parameters
used are listed inside the sub-folders.

Sub-folders contain NumPy array data collected. There are often two files :
- `real_results.npy` : Positions over time
- `achievement.npy` : L2 norm of each drone to its requested offset to achieve formations (current offset minus requested offset).
In case of multiple neighbours, we sum all L2 norms of offsets to each neighbour.

The two scripts plot the achievement rate of the formation over time, and the positions over time of all drones.
These scripts do not have any dependencies, so you can just run them with `python3` without having to specify
the PYTHONPATH environment variable.