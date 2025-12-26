import os
import sys

# Ensure repo root and src/ are on sys.path for direct package imports when running locally
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
ROOT_DIR = os.path.abspath(os.path.join(SRC_DIR, ".."))
for path in (SRC_DIR, ROOT_DIR):
    if path not in sys.path:
        sys.path.insert(0, path)

import numpy as np
from quantum.physical_models import (
    HBAR,
    bloch_vector,
    dephasing_operator,
    evolve_density_matrix,
    evolve_statevector,
    purity,
    rabi_hamiltonian,
)


def test_unitary_and_norm_preserved():
    H = rabi_hamiltonian(omega=1e6)
    psi0 = np.array([1.0, 0.0], dtype=complex)
    psi_t = evolve_statevector(psi0, H, delta_t=1e-9, steps=50)
    assert np.isclose(np.linalg.norm(psi_t), 1.0, atol=1e-9)


def test_density_matrix_trace_and_positivity():
    H = rabi_hamiltonian(omega=1e6)
    rho0 = np.array([[1.0, 0.0], [0.0, 0.0]], dtype=complex)
    rho_t = evolve_density_matrix(rho0, H, delta_t=1e-9, steps=20)
    assert np.isclose(np.trace(rho_t).real, 1.0, atol=1e-8)
    evals = np.linalg.eigvalsh(rho_t)
    assert np.all(evals >= -1e-8)


def test_dephasing_reduces_off_diagonals():
    H = np.zeros((2, 2), dtype=complex)
    rho0 = np.array([[0.5, 0.5], [0.5, 0.5]], dtype=complex)
    L = dephasing_operator()
    rho_t = evolve_density_matrix(rho0, H, delta_t=1e-9, steps=200, lindblad_ops=[L], gamma=2e7)
    assert abs(rho_t[0, 1]) < 1e-3


def test_bloch_vector_purity():
    rho = np.array([[0.7, 0.0], [0.0, 0.3]], dtype=complex)
    r = bloch_vector(rho)
    assert r.shape == (3,)
    p = purity(rho)
    assert 0.5 <= p <= 1.0


def test_energy_scale_units():
    H = rabi_hamiltonian(omega=2.0)
    assert np.allclose(H.imag, 0.0)
    assert np.isclose(H[0, 1], 0.5 * HBAR * 2.0)
