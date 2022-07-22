# Practical Floquet Theory
Tools, tips, and tricks for numerically simulating periodically-driven quantum systems using Floquet theory. For more details, please refer to the [notes](https://drive.google.com/drive/folders/1dp3FaByU1iY38Za1x4lQacvOHZxoJOJe?usp=sharing) accompanying this tutorial. 

Driven nonlinear systems are ubiquitous throughout physics, and can result in a rich set of dynamical phenomena that are absent in the static case. Within superconducting qubits and circuit QED, we are often interested in understanding the effects that arise when we drive given nonlinear circuit element --- for example, the ac Stark shift or the renormalization of system nonlinearities. More generally, drives can be thought of as a powerful control knob in the cQED toolbox that allow for in-situ modification of the system Hamiltonian. Some exciting examples of recent use cases in the field include dynamical sweet spot engineering, microwave-activated 2Q gates, and realizing Kerr cat qubits, among many others.

When the drive acting on a system is time-periodic, we can use *Floquet theory* to rigorously capture the associated dynamical effects. There are several largely equivalent ways to formulate Floquet problems. In this tutorial, we make use of the extended Hilbert space formalism in order in order to introduce the drive as another degree of freedom. We can then use numerical diagonalization to get the Floquet quasi-energy spectrum of the driven system. Here, we apply these techniques to simulate the ac-Stark shift in a driven transmon qubit. 

This repo is divided across three files: 
1. `demo-notebook.ipynb`: This notebook is structured as a problem set, with short coding exercises left to the reader. The goal is to walk you through setting up a Floquet numerical simulation from scratch. Several parts of the code have been left blank and marked `TODO` – e.g. setting up a qubit Hamiltonian in `qutip`. Feel free to fill in the blanks with your solution!

2. `demo-notebook-soln.ipynb`: This notebook provides the 'solution code' for the problem set. Running through all cells of the notebook will generate a working Floquet simulation of a driven transmon qubit, and produce a plot of the transmon's ac-Stark shift. 

3. `qubits.py`: Base infrastructure needed to set up the simulation. We have written a set of helper classes (e.g. `Qubit` and `DrivenSystem`) that you will then build upon in the simulation notebooks.


Note: the simulation notebooks here can also be found on [Deepnote](https://deepnote.com/workspace/shoumikdc-4d79e9b2-9de0-4601-ae84-2de19b25e79a/project/Practical-Floquet-Theory-62d8ce2a-0ca7-49d9-b8bc-c9bc74bd57d7/%2Fqubits.py) and run via the browser. If you don't want to install anything, this option provides an easy way to run through the tutorial!  


## Setup
The only dependencies needed to run the code in this repo are `qutip`, `numpy`, and `matplotlib`. As such, if you have these installed, you should be good to go. Simply clone the repository via:
```bash
$ git clone git@github.com:shoumikdc/practical-floquet.git
$ cd practical-floquet
```
If you are a `conda` user, you can install the requirements above directly to your environment by running `conda install qutip` and so on. Alternatively, use the provided requirements file:
```bash
$ conda install pip
$ pip install -r requirements.txt
```

## Ackowledgements
This tutorial was created in collaboration with [Agustin Di Paolo](https://github.com/agudipaolo) to accompany a lecture on "Practical Floquet Theory" delivered to the Engineering Quantum Systems (EQuS) group at MIT in May 2022. I would like to thank Agustin, as well as [Shantanu Jha](https://github.com/Phionx) and [Max Hays](https://scholar.google.com/citations?user=06z0MjwAAAAJ&hl=en) for many helpful discussions in getting this set up.
