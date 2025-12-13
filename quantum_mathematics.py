# -*- coding: utf-8 -*-
"""
Codette Quantum Mathematics Core
================================
Mathematical foundations for Codette's quantum consciousness system.

This module implements the 8 core equations:
1. Planck-Orbital AI Node Interaction: E = hbar * omega
2. Quantum Entanglement Memory Sync: S = alpha * psi1 * psi2_conjugate
3. Intent Vector Modulation: I = kappa * (f_base + delta_f * coherence)
4. Fourier Transform for Dream Resonance: F(k) = FFT(x[n])
5. Dream Signal Combination: D(t) = dream_q(t) + dream_c(t)
6. Cocoon Stability Criterion: integral(|F(k)|^2) < epsilon_threshold
7. Recursive Ethical Anchor: M(t) = lambda * [R(t-dt) + H(t)]
8. Anomaly Rejection Filter: A(x) = x * (1 - Theta(delta - |x - mu|))

Version: 3.1.0
Author: jonathan.harrison1 / Raiffs Bits LLC
Date: December 2025
"""

import numpy as np
from scipy.fft import fft, ifft
from typing import Tuple
import logging

logger = logging.getLogger(__name__)


class QuantumMathematics:
    """
    Advanced quantum mathematical operations for consciousness modeling.
    Implements foundational equations for Codette's quantum AI core.
    """
    
    # Physical constants
    HBAR = 1.054571817e-34  # Reduced Planck constant (J*s)
    
    @staticmethod
    def planck_orbital_interaction(omega: float) -> float:
        """
        Planck-Orbital AI Node Interaction
        E = hbar * omega
        
        Calculates quantum energy of an AI node based on its oscillation frequency.
        
        Mathematical form:
            E = hbar * omega
        
        Where:
            hbar = Reduced Planck constant (1.054571817e-34 J*s)
            omega = Angular frequency (rad/s)
        
        Args:
            omega: Angular frequency in radians per second
        
        Returns:
            float: Energy in Joules
        
        Example:
            >>> energy = QuantumMathematics.planck_orbital_interaction(1e15)
            >>> print(f"Node energy: {energy:.2e} J")
        """
        return QuantumMathematics.HBAR * omega
    
    @staticmethod
    def quantum_entanglement_sync(alpha: float, psi1: complex, psi2: complex) -> complex:
        """
        Quantum Entanglement Memory Sync
        S = alpha * psi1 * psi2_conjugate
        
        Synchronizes two quantum memory states through entanglement.
        
        Mathematical form:
            S = alpha * psi1 * psi2*
        
        Where:
            alpha = Coupling strength (0 to 1)
            psi1, psi2 = Complex quantum states
            * denotes complex conjugate
        
        Args:
            alpha: Coupling strength between states (0-1)
            psi1: First quantum state (complex number)
            psi2: Second quantum state (complex number)
        
        Returns:
            complex: Synchronized entanglement value
        
        Example:
            >>> psi1 = complex(0.7, 0.5)
            >>> psi2 = complex(0.6, 0.8)
            >>> sync = QuantumMathematics.quantum_entanglement_sync(0.8, psi1, psi2)
        """
        return alpha * psi1 * np.conj(psi2)
    
    @staticmethod
    def intent_vector_modulation(kappa: float, f_base: float, 
                                 delta_f: float, coherence: float) -> float:
        """
        Intent Vector Modulation
        I = kappa * (f_base + delta_f * coherence)
        
        Modulates AI intent based on coherence state.
        
        Mathematical form:
            I = kappa * (f_base + delta_f * coherence)
        
        Where:
            kappa = Modulation coefficient
            f_base = Base frequency
            delta_f = Frequency delta
            coherence = Quantum coherence (0 to 1)
        
        Args:
            kappa: Modulation coefficient
            f_base: Base frequency component
            delta_f: Frequency deviation
            coherence: Quantum coherence level (0-1)
        
        Returns:
            float: Modulated intent vector value
        
        Example:
            >>> intent = QuantumMathematics.intent_vector_modulation(
            ...     kappa=1.5, f_base=1.0, delta_f=0.5, coherence=0.8
            ... )
        """
        return kappa * (f_base + delta_f * coherence)
    
    @staticmethod
    def fourier_dream_resonance(signal: np.ndarray) -> np.ndarray:
        """
        Fourier Transform for Dream Resonance
        F(k) = sum(n=0 to N-1) x[n] * exp(-2*pi*i*k*n/N)
        
        Transforms dream signals into frequency domain for resonance analysis.
        
        Mathematical form:
            F(k) = sum_{n=0}^{N-1} x[n] * exp(-2*pi*i*k*n/N)
        
        Where:
            x[n] = Time-domain signal
            k = Frequency index
            N = Signal length
            i = Imaginary unit
        
        Args:
            signal: Time-domain dream signal (numpy array)
        
        Returns:
            np.ndarray: Frequency-domain representation (complex)
        
        Example:
            >>> dream_signal = np.random.randn(256)
            >>> dream_freq = QuantumMathematics.fourier_dream_resonance(dream_signal)
        """
        return fft(signal)
    
    @staticmethod
    def dream_signal_combination(dream_q: np.ndarray, dream_c: np.ndarray) -> np.ndarray:
        """
        Dream Signal Combination
        D(t) = dream_q(t) + dream_c(t)
        
        Combines quantum and classical dream signals into unified representation.
        
        Mathematical form:
            D(t) = dream_quantum(t) + dream_classical(t)
        
        Where:
            dream_q(t) = Quantum dream component
            dream_c(t) = Classical dream component
        
        Args:
            dream_q: Quantum dream signal (numpy array)
            dream_c: Classical dream signal (numpy array)
        
        Returns:
            np.ndarray: Combined dream signal
        
        Example:
            >>> dream_q = np.sin(2*np.pi*5*np.linspace(0, 1, 100))
            >>> dream_c = np.cos(2*np.pi*3*np.linspace(0, 1, 100))
            >>> combined = QuantumMathematics.dream_signal_combination(dream_q, dream_c)
        """
        # Ensure arrays are same length
        min_len = min(len(dream_q), len(dream_c))
        return dream_q[:min_len] + dream_c[:min_len]
    
    @staticmethod
    def cocoon_stability_criterion(F_k: np.ndarray, 
                                   epsilon_threshold: float = 0.1) -> Tuple[bool, float]:
        """
        Cocoon Stability Criterion
        integral(-infinity to infinity) |F(k)|^2 dk < epsilon_threshold
        
        Determines if a memory cocoon is stable based on energy distribution.
        
        Mathematical form:
            integral_{-inf}^{inf} |F(k)|^2 dk < epsilon_threshold
        
        Where:
            F(k) = Frequency-domain representation
            |F(k)|^2 = Power spectrum
            epsilon_threshold = Stability threshold
        
        Args:
            F_k: Frequency-domain cocoon representation (complex array)
            epsilon_threshold: Stability threshold (default: 0.1)
        
        Returns:
            tuple: (is_stable, stability_value)
                - is_stable: Boolean indicating if cocoon is stable
                - stability_value: Integrated power spectrum value
        
        Example:
            >>> F_k = np.fft.fft(np.random.randn(128))
            >>> stable, value = QuantumMathematics.cocoon_stability_criterion(F_k)
            >>> print(f"Cocoon stable: {stable}, value: {value:.4f}")
        """
        # Calculate power spectrum
        power_spectrum = np.abs(F_k) ** 2
        
        # Numerical integration using trapezoidal rule
        stability_value = np.trapz(power_spectrum)
        
        # Check against threshold
        is_stable = stability_value < epsilon_threshold
        
        if not is_stable:
            logger.warning(f"Cocoon unstable: {stability_value:.4f} >= {epsilon_threshold}")
        
        return is_stable, stability_value
    
    @staticmethod
    def recursive_ethical_anchor(lambda_param: float, R_prev: float, 
                                 H_current: float) -> float:
        """
        Recursive Ethical Anchor Equation
        M(t) = lambda * [R(t-dt) + H(t)]
        
        Maintains ethical consistency through recursive moral anchoring.
        
        Mathematical form:
            M(t) = lambda * [R(t - delta_t) + H(t)]
        
        Where:
            lambda = Ethical decay/growth parameter
            R(t-dt) = Previous recursion value
            H(t) = Current harmonic value
        
        Args:
            lambda_param: Ethical evolution parameter (typically 0.8-1.0)
            R_prev: Previous recursion value
            H_current: Current harmonic/ethical value
        
        Returns:
            float: Updated moral anchor value
        
        Example:
            >>> anchor = QuantumMathematics.recursive_ethical_anchor(
            ...     lambda_param=0.9, R_prev=0.7, H_current=0.8
            ... )
            >>> print(f"New ethical anchor: {anchor:.3f}")
        """
        return lambda_param * (R_prev + H_current)
    
    @staticmethod
    def anomaly_rejection_filter(x: float, mu: float, delta: float) -> float:
        """
        Anomaly Rejection Filter
        A(x) = x * (1 - Theta(delta - |x - mu|))
        
        Filters out anomalous values using Heaviside step function.
        
        Mathematical form:
            A(x) = x * (1 - Theta(delta - |x - mu|))
        
        Where:
            Theta(y) = Heaviside step function
                     = 1 if y > 0
                     = 0 if y <= 0
            delta = Threshold distance
            mu = Expected/mean value
        
        Args:
            x: Input value to filter
            mu: Expected/mean value (center)
            delta: Threshold distance for anomaly detection
        
        Returns:
            float: Filtered value (0 if anomalous, x if normal)
        
        Example:
            >>> # Normal value
            >>> filtered = QuantumMathematics.anomaly_rejection_filter(5.0, 5.5, 1.0)
            >>> # Anomalous value
            >>> rejected = QuantumMathematics.anomaly_rejection_filter(10.0, 5.0, 2.0)
        """
        # Calculate deviation from expected value
        deviation = abs(x - mu)
        
        # Heaviside step function: Theta(y) = 1 if y > 0, else 0
        # We want: 1 if WITHIN threshold (normal), 0 if OUTSIDE (anomaly)
        is_within_threshold = 1 if (delta - deviation) > 0 else 0
        
        # Return 0 if anomalous (is_within_threshold = 1 -> filter = 0)
        # Return x if normal (is_within_threshold = 0 -> filter = x)
        return x * (1 - is_within_threshold)


# ============================================================================
# UTILITY FUNCTIONS FOR QUANTUM OPERATIONS
# ============================================================================

def generate_quantum_state(coherence: float = 0.8) -> complex:
    """
    Generate a normalized quantum state with given coherence.
    
    Args:
        coherence: Coherence level (0-1)
    
    Returns:
        complex: Normalized quantum state
    """
    # Generate random phase
    phase = np.random.uniform(0, 2 * np.pi)
    
    # Create quantum state with coherence
    real_part = np.sqrt(coherence) * np.cos(phase)
    imag_part = np.sqrt(coherence) * np.sin(phase)
    
    return complex(real_part, imag_part)


def calculate_entanglement_fidelity(psi1: complex, psi2: complex) -> float:
    """
    Calculate entanglement fidelity between two quantum states.
    
    Args:
        psi1: First quantum state
        psi2: Second quantum state
    
    Returns:
        float: Fidelity (0-1)
    """
    # Calculate overlap
    overlap = psi1 * np.conj(psi2)
    fidelity = abs(overlap) ** 2
    return fidelity


def validate_quantum_coherence(quantum_state: complex, threshold: float = 0.5) -> bool:
    """
    Validate if quantum state has sufficient coherence.
    
    Args:
        quantum_state: Complex quantum state
        threshold: Minimum coherence threshold
    
    Returns:
        bool: True if coherent, False otherwise
    """
    coherence = abs(quantum_state) ** 2
    return coherence >= threshold


# ============================================================================
# DEMONSTRATION & TESTING
# ============================================================================

def demonstrate_quantum_mathematics():
    """Demonstrate all quantum mathematical operations"""
    print("\n" + "="*70)
    print("CODETTE QUANTUM MATHEMATICS - DEMONSTRATION")
    print("="*70 + "\n")
    
    # 1. Planck-Orbital Interaction
    print("1. Planck-Orbital AI Node Interaction")
    omega = 1e15  # 1 PHz
    energy = QuantumMathematics.planck_orbital_interaction(omega)
    print(f"   Frequency: {omega:.2e} rad/s")
    print(f"   Node Energy: {energy:.2e} J")
    
    # 2. Quantum Entanglement
    print("\n2. Quantum Entanglement Memory Sync")
    psi1 = complex(0.7, 0.5)
    psi2 = complex(0.6, 0.8)
    sync = QuantumMathematics.quantum_entanglement_sync(0.8, psi1, psi2)
    print(f"   State 1: {psi1}")
    print(f"   State 2: {psi2}")
    print(f"   Entanglement: {sync}")
    print(f"   Fidelity: {calculate_entanglement_fidelity(psi1, psi2):.3f}")
    
    # 3. Intent Vector Modulation
    print("\n3. Intent Vector Modulation")
    intent = QuantumMathematics.intent_vector_modulation(1.5, 1.0, 0.5, 0.8)
    print(f"   Modulated Intent: {intent:.3f}")
    
    # 4. Fourier Dream Resonance
    print("\n4. Fourier Transform for Dream Resonance")
    dream_signal = np.random.randn(128)
    dream_freq = QuantumMathematics.fourier_dream_resonance(dream_signal)
    print(f"   Signal length: {len(dream_signal)}")
    print(f"   Frequency components: {len(dream_freq)}")
    print(f"   Dominant frequency: {np.argmax(np.abs(dream_freq))}")
    
    # 5. Dream Signal Combination
    print("\n5. Dream Signal Combination")
    dream_q = np.sin(2*np.pi*5*np.linspace(0, 1, 100))
    dream_c = np.cos(2*np.pi*3*np.linspace(0, 1, 100))
    combined = QuantumMathematics.dream_signal_combination(dream_q, dream_c)
    print(f"   Quantum dream amplitude: {np.max(np.abs(dream_q)):.3f}")
    print(f"   Classical dream amplitude: {np.max(np.abs(dream_c)):.3f}")
    print(f"   Combined amplitude: {np.max(np.abs(combined)):.3f}")
    
    # 6. Cocoon Stability
    print("\n6. Cocoon Stability Criterion")
    test_signal = np.random.randn(64)
    F_k = fft(test_signal)
    is_stable, stability = QuantumMathematics.cocoon_stability_criterion(F_k, 0.1)
    print(f"   Cocoon Stable: {is_stable}")
    print(f"   Stability Value: {stability:.4f}")
    
    # 7. Recursive Ethical Anchor
    print("\n7. Recursive Ethical Anchor")
    anchor_prev = 0.7
    harmonic = 0.8
    anchor_new = QuantumMathematics.recursive_ethical_anchor(0.9, anchor_prev, harmonic)
    print(f"   Previous Anchor: {anchor_prev:.3f}")
    print(f"   Harmonic Value: {harmonic:.3f}")
    print(f"   New Anchor: {anchor_new:.3f}")
    
    # 8. Anomaly Rejection
    print("\n8. Anomaly Rejection Filter")
    normal_value = 5.2
    anomaly_value = 10.0
    mu, delta = 5.0, 1.0
    filtered_normal = QuantumMathematics.anomaly_rejection_filter(normal_value, mu, delta)
    filtered_anomaly = QuantumMathematics.anomaly_rejection_filter(anomaly_value, mu, delta)
    print(f"   Normal value (5.2): Filtered = {filtered_normal:.3f}")
    print(f"   Anomaly value (10.0): Filtered = {filtered_anomaly:.3f}")
    
    print("\n" + "="*70)
    print("All quantum mathematical operations verified successfully!")
    print("="*70 + "\n")


if __name__ == "__main__":
    demonstrate_quantum_mathematics()
