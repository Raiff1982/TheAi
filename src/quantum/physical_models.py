"""
Physical quantum models (small-scale, classical simulation).
Implements 2-level Schrödinger and Lindblad evolution with explicit units.
No external quantum hardware required; uses NumPy eigen-decomposition for expm.
"""

import math
import numpy as np

# Reduced Planck constant in SI (J·s)
HBAR = 1.054_571_817e-34


class QuantumDimensionError(ValueError):
    pass


def _is_hermitian(matrix: np.ndarray, atol: float = 1e-10) -> bool:
    return np.allclose(matrix, matrix.conj().T, atol=atol)


def _validate_statevector(psi: np.ndarray) -> np.ndarray:
    if psi.ndim != 1:
        raise QuantumDimensionError("Statevector must be 1-D")
    norm = np.linalg.norm(psi)
    if norm == 0:
        raise ValueError("Statevector norm is zero")
    return psi / norm


def _validate_density_matrix(rho: np.ndarray, atol: float = 1e-10) -> np.ndarray:
    if rho.ndim != 2 or rho.shape[0] != rho.shape[1]:
        raise QuantumDimensionError("Density matrix must be square")
    if not _is_hermitian(rho, atol=atol):
        raise ValueError("Density matrix must be Hermitian")
    trace = np.trace(rho).real
    if not math.isclose(trace, 1.0, rel_tol=0, abs_tol=1e-8):
        rho = rho / trace
    # Positivity check via eigenvalues
    evals = np.linalg.eigvalsh(rho)
    if np.any(evals < -1e-8):
        raise ValueError("Density matrix not positive semidefinite")
    return rho


def _unitary_from_hamiltonian(H: np.ndarray, delta_t: float) -> np.ndarray:
    if not _is_hermitian(H):
        raise ValueError("Hamiltonian must be Hermitian")
    evals, evecs = np.linalg.eigh(H)
    phases = np.exp(-1j * evals * delta_t / HBAR)
    return (evecs @ np.diag(phases) @ evecs.conj().T)


def evolve_statevector(psi: np.ndarray, H: np.ndarray, delta_t: float, steps: int = 1) -> np.ndarray:
    """Evolve a pure state under Schrödinger dynamics (closed system)."""
    psi = _validate_statevector(np.asarray(psi, dtype=complex))
    H = np.asarray(H, dtype=complex)
    U = _unitary_from_hamiltonian(H, delta_t)
    for _ in range(max(steps, 1)):
        psi = U @ psi
        psi = psi / np.linalg.norm(psi)
    return psi


def evolve_density_matrix(
    rho: np.ndarray,
    H: np.ndarray,
    delta_t: float,
    steps: int = 1,
    lindblad_ops=None,
    gamma: float = 0.0,
) -> np.ndarray:
    """Evolve an open system via Lindblad master equation (Euler step)."""
    rho = _validate_density_matrix(np.asarray(rho, dtype=complex))
    H = np.asarray(H, dtype=complex)
    lindblad_ops = lindblad_ops or []
    if not _is_hermitian(H):
        raise ValueError("Hamiltonian must be Hermitian")
    for _ in range(max(steps, 1)):
        commutator = H @ rho - rho @ H
        drho_dt = -1j / HBAR * commutator
        for L in lindblad_ops:
            L = np.asarray(L, dtype=complex)
            LdL = L.conj().T @ L
            drho_dt += gamma * (L @ rho @ L.conj().T - 0.5 * (LdL @ rho + rho @ LdL))
        rho = rho + delta_t * drho_dt
        # Stabilize: enforce Hermiticity and project small negative eigenvalues to zero
        rho = 0.5 * (rho + rho.conj().T)
        evals, evecs = np.linalg.eigh(rho)
        evals = np.clip(evals, 0.0, None)
        rho = (evecs @ np.diag(evals) @ evecs.conj().T)
        # Renormalize trace to 1
        tr = np.trace(rho).real
        if tr > 0:
            rho = rho / tr
        rho = _validate_density_matrix(rho)
    return rho


def bloch_vector(rho: np.ndarray) -> np.ndarray:
    """Return Bloch vector for a single qubit density matrix."""
    rho = _validate_density_matrix(np.asarray(rho, dtype=complex))
    if rho.shape != (2, 2):
        raise QuantumDimensionError("Bloch vector only defined for 2x2 density matrices")
    sx = np.array([[0, 1], [1, 0]], dtype=complex)
    sy = np.array([[0, -1j], [1j, 0]], dtype=complex)
    sz = np.array([[1, 0], [0, -1]], dtype=complex)
    return np.array([
        np.trace(rho @ sx).real,
        np.trace(rho @ sy).real,
        np.trace(rho @ sz).real,
    ])


def purity(rho: np.ndarray) -> float:
    rho = _validate_density_matrix(np.asarray(rho, dtype=complex))
    return float(np.real(np.trace(rho @ rho)))


def rabi_hamiltonian(omega: float, delta: float = 0.0) -> np.ndarray:
    """Two-level Rabi Hamiltonian: H = (ħ/2)(delta*σz + omega*σx)."""
    sx = np.array([[0, 1], [1, 0]], dtype=complex)
    sz = np.array([[1, 0], [0, -1]], dtype=complex)
    return 0.5 * HBAR * (delta * sz + omega * sx)


def dephasing_operator() -> np.ndarray:
    """Lindblad operator for pure dephasing (Z-channel)."""
    return np.array([[1, 0], [0, -1]], dtype=complex)


def example_rabi_oscillation(prob_initial_excited: float = 0.0, omega: float = 1e6, steps: int = 100) -> float:
    """Simulate Rabi oscillation and return final excited-state probability."""
    # Start in ground |0> = [1,0]
    psi0 = np.array([1.0, 0.0], dtype=complex)
    H = rabi_hamiltonian(omega)
    delta_t = 1e-9  # 1 ns step
    psi_t = evolve_statevector(psi0, H, delta_t, steps=steps)
    # Probability of excited state |1>
    return float(np.abs(psi_t[1]) ** 2)
