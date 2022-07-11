from typing import Dict, Any, List, Optional
from abc import abstractmethod, ABCMeta
from numbers import Number
import qutip as qt
import numpy as np


# Units and Useful Constants
GHz = 1
MHz = 1e-3
kHz = 1e-6


class Qubit(metaclass=ABCMeta):
    """
    Base class for defining superconducting qubits
    """

    @property
    @abstractmethod
    def expected_params(self) -> List[str]:
        """
        List of expected param strings. Note all frequencies have units GHz.
        E.g. ["Ej", "Ec", "N_max"]
        """

    def __init__(self, params: Dict[str, Any]):
        self.params = params.copy()

        # Set base parameters
        for param in self.expected_params:
            if param not in params:
                raise Exception(f"Please include the required parameter {param}")

        # Define operators
        self.ops: Dict[str, qt.Qobj] = {}
        self.build_ops()
        self._eig_system: Dict[str, List[np.ndarray]] = {}

    # Base Operators - To be overridden
    # ==========================================
    def build_ops(self):
        N = self.params["N_max"]
        self.ops["a_dag"] = qt.create(N)
        self.ops["a"] = qt.destroy(N)

    # System Hamiltonian and Eigenstates
    # ==========================================
    @abstractmethod
    def get_H(self) -> qt.Qobj:
        """
        Method for calculating the static qubit system Hamiltonian. Note: this version takes no args.

        Returns:
            H (qt.Qobj): Qubit Hamiltonian
        """

    @property
    def eig_system(self):
        """
        Method for diagonalizing the system Hamiltonian and storing sorted eigenvalues and eigenvectors.
        """
        N = self.params["N_max"]
        if "vals" not in self._eig_system or "vecs" not in self._eig_system:
            eig_system = np.linalg.eigh(self.get_H())

            # dim(eigvals_sorted) = N
            eigvals_sorted = np.sort(eig_system[0])
            idxs_sorted_by_eigval = np.argsort(eig_system[0])

            # dim(evs_sorted) = [N, N]
            eigvecs_sorted = eig_system[1][:, idxs_sorted_by_eigval]

            # Truncates eigensystem: keeps only the lowest N eigenvalues and vectors
            self._eig_system["vals"] = np.array(eigvals_sorted)[:N]
            self._eig_system["vecs"] = np.array(eigvecs_sorted)[:, :N]

        return self._eig_system

    @property
    def Ud(self):
        """
        Unitary change of basis matrix consisting of eigenvectors of H₀ as columns.
        """
        return qt.Qobj(self.eig_system["vecs"])

    def op_matrix_in_H_eigenbasis(self, op: qt.Qobj) -> qt.Qobj:
        """
        Method for calculating the matrix of an operator O in the eigenbasis of H₀
        """
        return (self.Ud.dag() * op * self.Ud).tidyup()

    # Analysis
    # ==========================================
    def qubit_report(self):
        """
        Method to print qubit frequency and anharmonicity.
        """
        eigvals = self.eig_system["vals"]

        ω_01 = eigvals[1] - eigvals[0]
        anharm = eigvals[2] + eigvals[0] - 2 * eigvals[1]

        print(f"Qubit frequency ω01 = {ω_01 * GHz} GHz")
        print(f"Qubit anharmonicity α = {anharm / MHz} MHz")
        return ω_01, anharm


class DrivenSystem(metaclass=ABCMeta):
    """
    Base class for a general driven quantum system
    """

    @property
    def expected_params(self) -> List[str]:
        """
        List of expected param strings.
            M_max: Drive "charge" basis truncation, defined -M_max to +M_max
        """
        return ["M_max"]

    def __init__(self, params: Dict[str, Any], qubit: Qubit, drive_coupling: qt.Qobj):
        self.qubit = qubit

        for param in self.expected_params:
            if param not in params:
                raise Exception(f"Please include the required parameter {param}")
        self.params = params.copy()

        # Initialize stored analysis dictionaries
        self.reset_analysis()
        self.ops["drive_coupling"] = drive_coupling

    def reset_analysis(self):
        """
        Initialize stored analysis dictionaries
        """
        self.ops: Dict[str, np.ndarray] = {}
        self.states: Dict[str, np.ndarray] = {}
        self.build_ops_and_states()
        
    
    # Analysis
    # ==========================================
    def get_bare_basis_idxs_overlaps(self, omega: float):
        """
        Method to calculate the indices of the eigenvectors that most closely match |α⟩⊗|m=0⟩,
        at zero drive amplitude Ω = 0. This is done via computing the state overlaps with a 
        fixed basis. 
        """
        H_eff_0 = fq.H_eff(omega, 0)

        eigvals, eigvecs = H_eff_0.eigenstates()

        bare_basis_idxs = []
        for bare_basis_vec in self.states["bare_basis"]:

            overlaps = []
            for vec in eigvecs:
                overlaps.append(np.abs(bare_basis_vec.overlap(vec)))

            max_overlap_idx = np.argmax(overlaps)
            bare_basis_idxs.append(max_overlap_idx)
    
        return np.array(bare_basis_idxs)
