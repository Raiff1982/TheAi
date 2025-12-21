"""
Quantum spiderweb implementation for advanced cognition.
Framework-compliant multi-dimensional cognitive graph.
"""

try:
    import networkx as nx
    NETWORKX_AVAILABLE = True
except Exception:
    nx = None
    NETWORKX_AVAILABLE = False

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except Exception:
    np = None
    NUMPY_AVAILABLE = False

try:
    from quantum_mathematics import QuantumMathematics
    QM_AVAILABLE = True
except Exception:
    QuantumMathematics = None
    QM_AVAILABLE = False

from typing import Dict, Any, List, Optional, Tuple, Callable
import random
import logging

logger = logging.getLogger(__name__)

class QuantumSpiderweb:
    """
    Simulates a cognitive spiderweb architecture with dimensions:
    Ψ (thought), τ (time), χ (speed), Φ (emotion), λ (space)
    
    Features:
    - Multi-dimensional quantum state vectors
    - Thought propagation with activation decay
    - Tension detection for instability
    - Quantum collapse to definite states
    - Node entanglement
    """
    
    def __init__(self, node_count: int = 128, seed: Optional[int] = None,
                 telemetry_hook: Optional[Callable[[str, Dict[str, Any]], None]] = None):
        if NETWORKX_AVAILABLE:
            self.graph = nx.Graph()
            self.use_networkx = True
        else:
            self.graph = {'nodes': {}, 'edges': {}}
            self.use_networkx = False
            logger.warning("NetworkX not available - using dict-based fallback")
        
        self.seed = seed
        self.telemetry_hook = telemetry_hook
        if seed is not None:
            random.seed(seed)
            if NUMPY_AVAILABLE:
                np.random.seed(seed)
        
        self.dimensions = ['Ψ', 'τ', 'χ', 'Φ', 'λ']
        self._init_nodes(node_count)
        self.entangled_states = {}
        self.activation_threshold = 0.3
        self.telemetry = {
            "propagations": 0,
            "tension_checks": 0,
            "collapses": 0,
            "entanglements": 0,
            "last_metrics": {}
        }
        
    def _init_nodes(self, count: int):
        """Initialize quantum nodes with multi-dimensional states"""
        for i in range(count):
            node_id = f"QNode_{i}"
            state = self._generate_state()
            
            if self.use_networkx:
                self.graph.add_node(node_id, state=state)
            else:
                self.graph['nodes'][node_id] = {'state': state, 'neighbors': {}}
            
            if i > 0:
                # Create connections with probability decay
                connection_count = min(3, i)  # Maximum 3 connections per node
                potential_connections = [f"QNode_{j}" for j in range(i)]
                selected_connections = random.sample(potential_connections, connection_count)
                
                for connection in selected_connections:
                    weight = random.uniform(0.1, 1.0)
                    if self.use_networkx:
                        self.graph.add_edge(node_id, connection, weight=weight)
                    else:
                        if connection not in self.graph['nodes']:
                            continue
                        self.graph['nodes'][node_id]['neighbors'][connection] = weight
                        # Bidirectional edge
                        self.graph['nodes'][connection]['neighbors'][node_id] = weight
                    
    def _generate_state(self) -> Dict[str, float]:
        """Generate quantum state vector for all dimensions"""
        if NUMPY_AVAILABLE:
            return {dim: float(np.random.uniform(-1.0, 1.0)) for dim in self.dimensions}
        return {dim: random.uniform(-1.0, 1.0) for dim in self.dimensions}
        
    def propagate_thought(self, origin: str, depth: int = 3) -> List[Tuple[str, Dict[str, float]]]:
        """
        Traverse the graph from a starting node, simulating pre-cognitive waveform
        
        Args:
            origin: Starting node ID
            depth: Propagation depth (default: 3)
            
        Returns:
            List of (node_id, state) tuples
        """
        if not self._node_exists(origin):
            logger.warning(f"Origin node {origin} does not exist")
            return []
            
        visited = set()
        stack = [(origin, 0)]
        traversal_output = []
        
        while stack:
            node, level = stack.pop()
            if node in visited or level > depth:
                continue
            visited.add(node)
            
            state = self._get_node_state(node)
            traversal_output.append((node, state))
            
            for neighbor in self._get_neighbors(node):
                stack.append((neighbor, level + 1))
                
        self._record_telemetry("propagation", {
            "origin": origin,
            "depth": depth,
            "visited": len(traversal_output)
        })
        return traversal_output
        
    def detect_tension(self, node: str) -> float:
        """
        Measures tension (instability) in the node's quantum state
        
        Args:
            node: Node ID to check
            
        Returns:
            Tension value (0-1, higher = more unstable)
        """
        if not self._node_exists(node):
            return 0.0
            
        state = self._get_node_state(node)
        
        if NUMPY_AVAILABLE:
            tension = float(np.std(list(state.values())))
        else:
            values = list(state.values())
            mean = sum(values) / len(values)
            variance = sum((v - mean) ** 2 for v in values) / len(values)
            tension = variance ** 0.5  # Standard deviation
        
        intent = None
        if QM_AVAILABLE and QuantumMathematics is not None:
            coherence = max(0.0, 1.0 - min(1.0, tension))
            # Slight modulation uses activation threshold as base frequency
            intent = QuantumMathematics.intent_vector_modulation(
                kappa=1.0,
                f_base=self.activation_threshold,
                delta_f=0.1,
                coherence=coherence
            )
        
        self._record_telemetry("tension", {
            "node": node,
            "tension": tension,
            "intent": intent
        })
        return tension
        
    def collapse_node(self, node: str) -> Dict[str, Any]:
        """
        Collapse superposed thought into deterministic response
        
        Args:
            node: Node ID to collapse
            
        Returns:
            Collapsed state dict
        """
        if not self._node_exists(node):
            return {}
            
        state = self._get_node_state(node)
        collapsed = {k: round(v, 2) for k, v in state.items()}
        
        # Update node state
        self._set_node_state(node, collapsed)
        
        # Store in entangled states
        self.entangled_states[node] = collapsed
        
        self._record_telemetry("collapse", {
            "node": node,
            "state": collapsed
        })
        return collapsed
        
    def entangle_nodes(self, node1: str, node2: str) -> bool:
        """
        Create quantum entanglement between nodes
        
        Args:
            node1: First node ID
            node2: Second node ID
            
        Returns:
            Success status
        """
        if not (self._node_exists(node1) and self._node_exists(node2)):
            return False
            
        state1 = self._get_node_state(node1)
        state2 = self._get_node_state(node2)
        entangled_id = f"E_{node1}_{node2}"
        entangled_state = self._generate_state()

        coherence = None
        energy = None
        if QM_AVAILABLE and NUMPY_AVAILABLE and QuantumMathematics is not None:
            try:
                psi1 = complex(state1.get('Ψ', 0.0), state1.get('Φ', 0.0))
                psi2 = complex(state2.get('Ψ', 0.0), state2.get('Φ', 0.0))
                coherence = QuantumMathematics.quantum_entanglement_sync(0.8, psi1, psi2)
                energy = QuantumMathematics.planck_orbital_interaction(abs(coherence))
            except Exception as exc:
                logger.debug(f"Entanglement math fallback: {exc}")

        self.entangled_states[entangled_id] = {
            "nodes": [node1, node2],
            "state": entangled_state,
            "coherence": float(abs(coherence)) if coherence is not None else None,
            "energy": float(energy) if energy is not None else None
        }
        
        # Add high-weight connection
        if self.use_networkx:
            self.graph.add_edge(node1, node2, weight=1.0, entangled=True)
        else:
            self.graph['nodes'][node1]['neighbors'][node2] = 1.0
            self.graph['nodes'][node2]['neighbors'][node1] = 1.0
            
        self._record_telemetry("entangle", {
            "pair": (node1, node2),
            "coherence": float(abs(coherence)) if coherence is not None else None,
            "energy": float(energy) if energy is not None else None
        })
        return True
    
    # =========================================================================
    # HELPER METHODS
    # =========================================================================
    
    def _node_exists(self, node_id: str) -> bool:
        """Check if node exists"""
        if self.use_networkx:
            return node_id in self.graph
        return node_id in self.graph['nodes']
    
    def _get_node_state(self, node_id: str) -> Dict[str, float]:
        """Get node's quantum state"""
        if self.use_networkx:
            return self.graph.nodes[node_id]["state"]
        return self.graph['nodes'][node_id]['state']
    
    def _set_node_state(self, node_id: str, state: Dict[str, float]):
        """Set node's quantum state"""
        if self.use_networkx:
            self.graph.nodes[node_id]["state"] = state
        else:
            self.graph['nodes'][node_id]['state'] = state
    
    def _get_neighbors(self, node_id: str) -> List[str]:
        """Get node's neighbors"""
        if self.use_networkx:
            return list(self.graph.neighbors(node_id))
        return list(self.graph['nodes'][node_id]['neighbors'].keys())
    
    def get_node_state(self, node_id: str) -> Optional[Dict[str, float]]:
        """Public method to get node state"""
        if self._node_exists(node_id):
            return self._get_node_state(node_id)
        return None
        
    def update_node_state(self, node_id: str, new_state: Dict[str, float]) -> bool:
        """Public method to update node state"""
        if self._node_exists(node_id):
            # Validate state dimensions
            if all(dim in new_state for dim in self.dimensions):
                self._set_node_state(node_id, new_state)
                return True
        return False
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get graph statistics"""
        if self.use_networkx:
            return {
                "node_count": self.graph.number_of_nodes(),
                "edge_count": self.graph.number_of_edges(),
                "entangled_pairs": len(self.entangled_states),
                "dimensions": len(self.dimensions)
            }
        else:
            node_count = len(self.graph['nodes'])
            edge_count = sum(len(n['neighbors']) for n in self.graph['nodes'].values()) // 2
            return {
                "node_count": node_count,
                "edge_count": edge_count,
                "entangled_pairs": len(self.entangled_states),
                "dimensions": len(self.dimensions)
            }

    def get_telemetry(self) -> Dict[str, Any]:
        """Expose lightweight telemetry metrics"""
        return dict(self.telemetry)

    # ---------------------------------------------------------------------
    # Internal telemetry helper
    # ---------------------------------------------------------------------
    def _record_telemetry(self, event: str, payload: Dict[str, Any]):
        if not hasattr(self, "telemetry"):
            return
        if event == "propagation":
            self.telemetry["propagations"] += 1
        elif event == "tension":
            self.telemetry["tension_checks"] += 1
        elif event == "collapse":
            self.telemetry["collapses"] += 1
        elif event == "entangle":
            self.telemetry["entanglements"] += 1
        self.telemetry["last_metrics"] = payload
        logger.debug(f"Telemetry event={event} payload={payload}")
        if self.telemetry_hook is not None:
            try:
                self.telemetry_hook(event, payload)
            except Exception as exc:
                logger.debug(f"Telemetry hook failed: {exc}")


if __name__ == "__main__":
    # Test QuantumSpiderweb
    print("="*70)
    print("QUANTUM SPIDERWEB TEST")
    print("="*70)
    
    web = QuantumSpiderweb(node_count=32)
    root = "QNode_0"
    
    print(f"\nStatistics: {web.get_statistics()}")
    
    print(f"\nInitial Propagation from: {root}")
    path = web.propagate_thought(root)
    for n, s in path[:5]:  # Show first 5
        print(f"{n}: Ψ={s['Ψ']:.2f}, τ={s['τ']:.2f}, χ={s['χ']:.2f}, Φ={s['Φ']:.2f}, λ={s['λ']:.2f}")
    
    print(f"\nDetect Tension: {web.detect_tension(root):.4f}")
    
    print("\nCollapse Sample Node:")
    collapsed = web.collapse_node(root)
    print(collapsed)
    
    print("\n✅ Test complete")