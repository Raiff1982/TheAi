
# === AEGIS Council Core Implementation ===
"""
AEGIS (Advanced Ethical Guardian and Intelligence System) provides ethical oversight
and analysis capabilities through a council of specialized agents.
"""

import json
import hashlib
import threading
import logging
import sqlite3
from datetime import datetime, timedelta
from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Any, Dict, Optional, List, Tuple
import concurrent.futures
import networkx as nx
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import torch
from transformers import pipeline, AutoTokenizer, AutoModel
from copy import deepcopy

# Set up logging
logger = logging.getLogger(__name__)

# Try to import syft, but don't fail if it's not available
try:
    import syft as sy
    SYFT_AVAILABLE = True
except ImportError:
    SYFT_AVAILABLE = False
    logger.warning("PySyft not available. Federated learning features will be disabled.")
    logger.warning("PySyft not available. Federated learning features will be disabled.")

# Core AEGIS Components
class AegisCouncil:
    def __init__(self, config: Dict[str, Any]):
        self.memory = NexusMemory(
            max_entries=config["memory_max_entries"], 
            decay_days=config["memory_decay_days"]
        )
        self.agents = []
        self.reports = {}
        self.graph = nx.DiGraph()
        self.logger = logging.getLogger('AegisCouncil')
        self.config = config
        self.federated_trainer = FederatedTrainer(config["federated_learning"]["num_clients"])

    def register_agent(self, agent: 'AegisAgent') -> None:
        try:
            self.agents.append(agent)
            self.logger.info(f"Registered agent: {agent.name}")
        except Exception as e:
            self.logger.error(f"Error registering agent: {e}")

    def get_reports(self) -> Dict[str, Any]:
        """Get the current analysis reports."""
        return self.reports

    def dispatch(self, input_data: Dict[str, Any], max_retries: int = 3) -> bool:
        try:
            if not isinstance(input_data, dict):
                self.logger.error("Input data must be a dictionary")
                return False

            self.reports.clear()
            self.graph.clear()

            for attempt in range(max_retries):
                try:
                    with concurrent.futures.ThreadPoolExecutor(max_workers=len(self.agents)) as executor:
                        future_to_agent = {
                            executor.submit(agent.analyze, input_data): agent 
                            for agent in self.agents
                        }
                        for future in concurrent.futures.as_completed(future_to_agent):
                            agent = future_to_agent[future]
                            try:
                                future.result()
                                self.reports[agent.name] = agent.report()
                                self.graph.add_node(agent.name, explanation=agent.explanation)
                                for target, weight in agent.influence.items():
                                    self.graph.add_edge(agent.name, target, weight=round(weight, 2))
                            except Exception as e:
                                self.logger.error(f"Error in agent {agent.name}: {e}")
                                self.reports[agent.name] = {
                                    "error": str(e), 
                                    "explanation": "Agent failed to process"
                                }

                    consensus = self._compute_consensus()
                    self.reports["Consensus"] = {
                        "result": consensus,
                        "explanation": "Consensus from weighted agent outputs."
                    }
                    self.memory.blockchain.add_block(self.reports)
                    return True
                except Exception as e:
                    self.logger.warning(f"Retry {attempt + 1} after error: {e}")
            
            self.logger.error(f"Dispatch failed after {max_retries} retries")
            return False
        except Exception as e:
            self.logger.error(f"Error in dispatch: {e}")
            return False

    def _compute_consensus(self) -> Dict[str, Any]:
        try:
            meta_scores = self.reports.get("MetaJudgeAgent", {}).get("result", {}).get("scores", [])
            virtue_profiles = [
                self.reports[agent]["result"].get("virtue_profile", {})
                for agent in self.reports 
                if agent != "Consensus" and "virtue_profile" in self.reports[agent]["result"]
            ]
            
            if not virtue_profiles or not meta_scores:
                return {"error": "Insufficient data for consensus"}

            weights = {agent: score for agent, score in meta_scores}
            default_weight = 0.5 / len(self.agents)
            combined_profile = {}
            
            for virtue in ["compassion", "integrity", "courage", "wisdom"]:
                weighted_sum = 0
                total_weight = 0
                for profile in virtue_profiles:
                    if virtue in profile:
                        agent_name = next(
                            (agent for agent in self.reports if self.reports[agent]["result"].get("virtue_profile") == profile),
                            None
                        )
                        weight = weights.get(agent_name, default_weight)
                        weighted_sum += profile[virtue] * weight
                        total_weight += weight
                combined_profile[virtue] = round(weighted_sum / total_weight, 2) if total_weight > 0 else 0.0
            
            return {"combined_virtue_profile": combined_profile}
        except Exception as e:
            self.logger.error(f"Error computing consensus: {e}")
            return {"error": str(e)}

    def draw_explainability_graph(self, filename: str = "explainability_graph.html") -> None:
        try:
            pos = self._compute_layout()
            edge_trace = self._create_edge_trace(pos)
            node_trace = self._create_node_trace(pos)
            edge_labels = self._create_edge_labels(pos)

            fig = go.Figure(
                data=[edge_trace, node_trace] + edge_labels,
                layout=go.Layout(
                    title="AEGIS Analysis Graph",
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20, l=5, r=5, t=40),
                    xaxis=dict(showgrid=False, zeroline=False),
                    yaxis=dict(showgrid=False, zeroline=False)
                )
            )
            fig.write_html(filename)
            self.logger.info(f"Saved analysis graph to {filename}")
        except Exception as e:
            self.logger.error(f"Error drawing graph: {e}")

    def _compute_layout(self):
        return nx.spring_layout(self.graph)

    def _create_edge_trace(self, pos):
        edge_x, edge_y = [], []
        for edge in self.graph.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
        return go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=1, color='#888'),
            hoverinfo='none',
            mode='lines'
        )

    def _create_node_trace(self, pos):
        node_x, node_y = [], []
        for node in self.graph.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
        return go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            hoverinfo='text',
            marker=dict(size=20, color='lightblue'),
            text=list(self.graph.nodes()),
            textposition="bottom center"
        )

    def _create_edge_labels(self, pos):
        labels = []
        for edge in self.graph.edges(data=True):
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            labels.append(
                go.Scatter(
                    x=[(x0 + x1) / 2],
                    y=[(y0 + y1) / 2],
                    mode='text',
                    text=[f"{edge[2]['weight']:.2f}"],
                    textposition="middle center"
                )
            )
        return labels

# Memory Management
class NexusMemory:
    def __init__(self, max_entries: int = 10000, decay_days: int = 30):
        self.store = defaultdict(dict)
        self.max_entries = max_entries
        self.decay_days = decay_days
        self.lock = threading.Lock()
        self.logger = logging.getLogger('NexusMemory')
        self.blockchain = Blockchain()

    def write(self, key: str, value: Any, emotion_weight: float = 0.5) -> Optional[str]:
        try:
            if not isinstance(key, str) or not (0 <= emotion_weight <= 1):
                self.logger.error(f"Invalid key type or emotion weight")
                return None

            # Convert numpy types to Python native types
            def convert_value(v):
                if isinstance(v, np.bool_):
                    return bool(v)
                if isinstance(v, np.integer):
                    return int(v)
                if isinstance(v, np.floating):
                    return float(v)
                if isinstance(v, np.ndarray):
                    return v.tolist()
                if isinstance(v, dict):
                    return {k: convert_value(val) for k, val in v.items()}
                if isinstance(v, (list, tuple)):
                    return [convert_value(item) for item in v]
                return v

            hashed = hashlib.md5(key.encode()).hexdigest()
            timestamp = datetime.now()

            with self.lock:
                if len(self.store) >= self.max_entries:
                    oldest = min(self.store.items(), key=lambda x: x[1].get('timestamp', timestamp))[0]
                    del self.store[oldest]

                self.store[hashed] = {
                    "value": convert_value(value),
                    "timestamp": timestamp,
                    "emotion_weight": float(emotion_weight)  # Ensure emotion_weight is native float
                }

                self.blockchain.add_block({
                    "key": hashed,
                    "value": value,
                    "timestamp": timestamp.isoformat()
                })

                return hashed
        except Exception as e:
            self.logger.error(f"Error writing to memory: {e}")
            return None

    def read(self, key: str) -> Optional[Any]:
        try:
            hashed = hashlib.md5(key.encode()).hexdigest()
            with self.lock:
                entry = self.store.get(hashed)
                if not entry:
                    return None

                if self._is_decayed(entry["timestamp"], entry.get("emotion_weight", 0.5)):
                    del self.store[hashed]
                    return None

                return entry["value"]
        except Exception as e:
            self.logger.error(f"Error reading from memory: {e}")
            return None

    def _is_decayed(self, timestamp: datetime, emotion_weight: float) -> bool:
        try:
            age = (datetime.now() - timestamp).total_seconds() / (24 * 3600)
            decay_factor = np.exp(-age / (self.decay_days * (1.5 - emotion_weight)))
            return decay_factor < 0.1
        except Exception as e:
            self.logger.error(f"Error checking decay: {e}")
            return True

    def audit(self) -> Dict[str, Any]:
        try:
            with self.lock:
                audit_data = {
                    k: {
                        "timestamp": v["timestamp"],
                        "emotion_weight": v["emotion_weight"],
                        "decayed": self._is_decayed(v["timestamp"], v["emotion_weight"])
                    }
                    for k, v in self.store.items()
                }
                self.blockchain.add_block({"audit": audit_data})
                return audit_data
        except Exception as e:
            self.logger.error(f"Error auditing memory: {e}")
            return {}

# Auditability
class Blockchain:
    def __init__(self):
        self.chain = [{
            "index": 0,
            "timestamp": datetime.now().isoformat(),
            "data": "Genesis Block",
            "prev_hash": "0"
        }]
        self.logger = logging.getLogger('Blockchain')

    def add_block(self, data: Dict[str, Any]) -> None:
        try:
            prev_block = self.chain[-1]
            # Convert datetime objects and numpy types to JSON serializable format
            def json_handler(obj):
                if isinstance(obj, datetime):
                    return obj.isoformat()
                if isinstance(obj, np.bool_):
                    return bool(obj)
                if isinstance(obj, np.integer):
                    return int(obj)
                if isinstance(obj, np.floating):
                    return float(obj)
                if isinstance(obj, np.ndarray):
                    return obj.tolist()
                raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
                
            block = {
                "index": len(self.chain),
                "timestamp": datetime.now().isoformat(),
                "data": json.dumps(data, default=json_handler),
                "prev_hash": self._hash_block(prev_block)
            }
            block["hash"] = self._hash_block(block)
            self.chain.append(block)
        except Exception as e:
            self.logger.error(f"Error adding block: {e}")

    def _hash_block(self, block: Dict[str, Any]) -> str:
        try:
            block_str = json.dumps(block, sort_keys=True)
            return hashlib.sha256(block_str.encode()).hexdigest()
        except Exception as e:
            self.logger.error(f"Error hashing block: {e}")
            return ""

    def verify(self) -> bool:
        try:
            for i in range(1, len(self.chain)):
                current = self.chain[i]
                prev = self.chain[i-1]
                if current["prev_hash"] != self._hash_block(prev):
                    return False
            return True
        except Exception as e:
            self.logger.error(f"Error verifying blockchain: {e}")
            return False

# Federated Learning
class FederatedTrainer:
    def __init__(self, num_clients: int):
        self.num_clients = num_clients
        self.logger = logging.getLogger('FederatedTrainer')
        
        if SYFT_AVAILABLE:
            self.hook = sy.TorchHook(torch)
            self.clients = [
                sy.VirtualWorker(self.hook, id=f"client_{i}") 
                for i in range(num_clients)
            ]
        else:
            self.hook = None
            self.clients = []
            self.logger.warning("Running without federated learning - PySyft not available")

    def train(self, weights: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
        try:
            if not SYFT_AVAILABLE:
                self.logger.debug("Skipping federated training - PySyft not available")
                return weights

            client_updates = []
            for client in self.clients:
                client_weights = deepcopy(weights)
                for virtue in client_weights:
                    client_weights[virtue] += np.random.normal(0, 0.01, size=client_weights[virtue].shape)
                client_updates.append(client_weights)
            
            aggregated = {}
            for virtue in weights:
                aggregated[virtue] = np.mean([update[virtue] for update in client_updates], axis=0)
            
            return aggregated
        except Exception as e:
            self.logger.error(f"Error in federated training: {e}")
            return weights

# Agent Base Class
class AegisAgent(ABC):
    def __init__(self, name: str, memory: NexusMemory):
        self.name = name
        self.memory = memory
        self.result: Dict[str, Any] = {}
        self.explanation: str = ""
        self.influence: Dict[str, float] = {}
        self.logger = logging.getLogger(f'AegisAgent.{name}')

    @abstractmethod
    def analyze(self, input_data: Dict[str, Any]) -> None:
        pass

    def report(self) -> Dict[str, Any]:
        return {
            "result": self.result,
            "explanation": self.explanation
        }

# Specialized Agents
class MetaJudgeAgent(AegisAgent):
    def __init__(self, name: str, memory: NexusMemory, weights: Dict[str, float]):
        super().__init__(name, memory)
        self.weights = weights

    def analyze(self, input_data: Dict[str, Any]) -> None:
        try:
            overrides = input_data.get("overrides", {})
            if not overrides:
                self.result = {"error": "No overrides provided"}
                self.explanation = "No overrides provided for analysis."
                return

            scores = []
            for agent, data in overrides.items():
                try:
                    influence = float(data.get("influence", 0.5))
                    reliability = float(data.get("reliability", 0.5))
                    severity = float(data.get("severity", 0.5))
                    
                    if not all(0 <= x <= 1 for x in [influence, reliability, severity]):
                        continue

                    score = (
                        self.weights["influence"] * influence +
                        self.weights["reliability"] * reliability +
                        self.weights["severity"] * severity
                    )
                    scores.append((agent, score))
                    self.influence[agent] = score
                except Exception as e:
                    self.logger.error(f"Error processing agent {agent}: {e}")

            if not scores:
                self.result = {"error": "No valid agents to score"}
                self.explanation = "No valid agents for meta-analysis."
                return

            scores.sort(key=lambda x: x[1], reverse=True)
            self.result = {
                "override_decision": scores[0][0],
                "scores": scores
            }
            self.explanation = f"Selected '{scores[0][0]}' with score {scores[0][1]:.2f}"
        except Exception as e:
            self.result = {"error": str(e)}
            self.explanation = f"Analysis failed: {e}"

class TemporalAgent(AegisAgent):
    def __init__(self, name: str, memory: NexusMemory, decay_thresholds: Dict[str, float]):
        super().__init__(name, memory)
        self.decay_thresholds = decay_thresholds

    def analyze(self, input_data: Dict[str, Any]) -> None:
        try:
            audit = self.memory.audit()
            recent_keys = sorted(
                audit.items(), 
                key=lambda x: x[1]["timestamp"],
                reverse=True
            )[:5]
            
            decay_rates = [1 if v["decayed"] else 0 for _, v in recent_keys]
            avg_decay = np.mean(decay_rates) if decay_rates else 0.0
            
            forecast = (
                "stable" if avg_decay < self.decay_thresholds["stable"]
                else "volatile" if avg_decay > self.decay_thresholds["volatile"]
                else "neutral"
            )
            
            self.result = {
                "temporal_forecast": forecast,
                "recent_keys": [k for k, _ in recent_keys],
                "decay_rate": avg_decay
            }
            self.explanation = f"Forecast: {forecast} (decay rate: {avg_decay:.2f})"
            
            for k, _ in recent_keys:
                self.influence[k] = 0.2
        except Exception as e:
            self.result = {"error": str(e)}
            self.explanation = f"Temporal analysis failed: {e}"

class VirtueAgent(AegisAgent):
    def __init__(self, name: str, memory: NexusMemory, virtue_weights: Dict[str, List[float]]):
        super().__init__(name, memory)
        self.tokenizer = AutoTokenizer.from_pretrained(
            "distilbert-base-uncased-finetuned-sst-2-english"
        )
        self.model = AutoModel.from_pretrained(
            "distilbert-base-uncased-finetuned-sst-2-english"
        )
        self.sentiment = pipeline(
            "sentiment-analysis",
            model="distilbert-base-uncased-finetuned-sst-2-english"
        )
        self.virtue_weights = {k: np.array(v) for k, v in virtue_weights.items()}
        self.federated_trainer = None

    def set_federated_trainer(self, trainer: FederatedTrainer):
        self.federated_trainer = trainer

    def analyze(self, input_data: Dict[str, Any]) -> None:
        try:
            text = input_data.get("text", "")
            if not text or not isinstance(text, str):
                self.result = {"error": "Invalid input text"}
                self.explanation = "No valid text provided for analysis."
                return

            # Check cache
            mem_key = f"virtue_cache_{hashlib.md5(text.encode()).hexdigest()}"
            cached = self.memory.read(mem_key)
            if cached:
                self.result = {"virtue_profile": cached}
                self.explanation = f"Retrieved cached analysis"
                self.influence.update({k: v for k, v in cached.items()})
                return

            # Perform analysis
            sentiment_result = self.sentiment(text)[0]
            sentiment = 1.0 if sentiment_result["label"] == "POSITIVE" else -1.0
            sentiment_score = sentiment_result["score"]

            inputs = self.tokenizer(
                text,
                return_tensors="pt",
                truncation=True,
                max_length=512
            )
            with torch.no_grad():
                outputs = self.model(**inputs)
            
            embeddings = outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
            subjectivity = min(max(np.std(embeddings), 0.0), 1.0)
            neutrality = 1.0 - abs(sentiment)

            if self.federated_trainer:
                self.virtue_weights = self.federated_trainer.train(self.virtue_weights)

            features = np.array([
                sentiment * sentiment_score,
                subjectivity,
                neutrality
            ])

            virtues = {}
            for virtue, weights in self.virtue_weights.items():
                # Convert numpy types to Python native types
                score = float(max(np.dot(weights, features), 0.0))
                virtues[virtue] = float(min(round(score, 2), 1.0))  # Ensure native float

            # Convert all numpy types in the result
            self.result = {
                "virtue_profile": {
                    k: float(v) if isinstance(v, (np.number, float)) else v
                    for k, v in virtues.items()
                }
            }
            self.explanation = (
                f"Virtues analyzed: {', '.join(f'{k}: {v:.2f}' for k, v in virtues.items())}"
            )
            
            for virtue, score in virtues.items():
                self.influence[virtue] = float(score)  # Ensure native float
            
            self.memory.write(mem_key, virtues, emotion_weight=0.8)
        except Exception as e:
            self.result = {"error": str(e)}

# === AEGIS Council Core Implementation ===
"""
AEGIS (Advanced Ethical Guardian and Intelligence System) provides ethical oversight
and analysis capabilities through a council of specialized agents.
"""

import json
import hashlib
import threading
import logging
import sqlite3
from datetime import datetime, timedelta
from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Any, Dict, Optional, List, Tuple
import concurrent.futures
import networkx as nx
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import torch
from transformers import pipeline, AutoTokenizer, AutoModel
from copy import deepcopy

# Set up logging
logger = logging.getLogger(__name__)

# Try to import syft, but don't fail if it's not available
try:
    import syft as sy
    SYFT_AVAILABLE = True
except ImportError:
    SYFT_AVAILABLE = False
    logger.warning("PySyft not available. Federated learning features will be disabled.")
    logger.warning("PySyft not available. Federated learning features will be disabled.")

# Core AEGIS Components
class AegisCouncil:
    def __init__(self, config: Dict[str, Any]):
        self.memory = NexusMemory(
            max_entries=config["memory_max_entries"], 
            decay_days=config["memory_decay_days"]
        )
        self.agents = []
        self.reports = {}
        self.graph = nx.DiGraph()
        self.logger = logging.getLogger('AegisCouncil')
        self.config = config
        self.federated_trainer = FederatedTrainer(config["federated_learning"]["num_clients"])

    def register_agent(self, agent: 'AegisAgent') -> None:
        try:
            self.agents.append(agent)
            self.logger.info(f"Registered agent: {agent.name}")
        except Exception as e:
            self.logger.error(f"Error registering agent: {e}")

    def get_reports(self) -> Dict[str, Any]:
        """Get the current analysis reports."""
        return self.reports

    def dispatch(self, input_data: Dict[str, Any], max_retries: int = 3) -> bool:
        try:
            if not isinstance(input_data, dict):
                self.logger.error("Input data must be a dictionary")
                return False

            self.reports.clear()
            self.graph.clear()

            for attempt in range(max_retries):
                try:
                    with concurrent.futures.ThreadPoolExecutor(max_workers=len(self.agents)) as executor:
                        future_to_agent = {
                            executor.submit(agent.analyze, input_data): agent 
                            for agent in self.agents
                        }
                        for future in concurrent.futures.as_completed(future_to_agent):
                            agent = future_to_agent[future]
                            try:
                                future.result()
                                self.reports[agent.name] = agent.report()
                                self.graph.add_node(agent.name, explanation=agent.explanation)
                                for target, weight in agent.influence.items():
                                    self.graph.add_edge(agent.name, target, weight=round(weight, 2))
                            except Exception as e:
                                self.logger.error(f"Error in agent {agent.name}: {e}")
                                self.reports[agent.name] = {
                                    "error": str(e), 
                                    "explanation": "Agent failed to process"
                                }

                    consensus = self._compute_consensus()
                    self.reports["Consensus"] = {
                        "result": consensus,
                        "explanation": "Consensus from weighted agent outputs."
                    }
                    self.memory.blockchain.add_block(self.reports)
                    return True
                except Exception as e:
                    self.logger.warning(f"Retry {attempt + 1} after error: {e}")
            
            self.logger.error(f"Dispatch failed after {max_retries} retries")
            return False
        except Exception as e:
            self.logger.error(f"Error in dispatch: {e}")
            return False

    def _compute_consensus(self) -> Dict[str, Any]:
        try:
            meta_scores = self.reports.get("MetaJudgeAgent", {}).get("result", {}).get("scores", [])
            virtue_profiles = [
                self.reports[agent]["result"].get("virtue_profile", {})
                for agent in self.reports 
                if agent != "Consensus" and "virtue_profile" in self.reports[agent]["result"]
            ]
            
            if not virtue_profiles or not meta_scores:
                return {"error": "Insufficient data for consensus"}

            weights = {agent: score for agent, score in meta_scores}
            default_weight = 0.5 / len(self.agents)
            combined_profile = {}
            
            for virtue in ["compassion", "integrity", "courage", "wisdom"]:
                weighted_sum = 0
                total_weight = 0
                for profile in virtue_profiles:
                    if virtue in profile:
                        agent_name = next(
                            (agent for agent in self.reports if self.reports[agent]["result"].get("virtue_profile") == profile),
                            None
                        )
                        weight = weights.get(agent_name, default_weight)
                        weighted_sum += profile[virtue] * weight
                        total_weight += weight
                combined_profile[virtue] = round(weighted_sum / total_weight, 2) if total_weight > 0 else 0.0
            
            return {"combined_virtue_profile": combined_profile}
        except Exception as e:
            self.logger.error(f"Error computing consensus: {e}")
            return {"error": str(e)}

    def draw_explainability_graph(self, filename: str = "explainability_graph.html") -> None:
        try:
            pos = self._compute_layout()
            edge_trace = self._create_edge_trace(pos)
            node_trace = self._create_node_trace(pos)
            edge_labels = self._create_edge_labels(pos)

            fig = go.Figure(
                data=[edge_trace, node_trace] + edge_labels,
                layout=go.Layout(
                    title="AEGIS Analysis Graph",
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20, l=5, r=5, t=40),
                    xaxis=dict(showgrid=False, zeroline=False),
                    yaxis=dict(showgrid=False, zeroline=False)
                )
            )
            fig.write_html(filename)
            self.logger.info(f"Saved analysis graph to {filename}")
        except Exception as e:
            self.logger.error(f"Error drawing graph: {e}")

    def _compute_layout(self):
        return nx.spring_layout(self.graph)

    def _create_edge_trace(self, pos):
        edge_x, edge_y = [], []
        for edge in self.graph.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
        return go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=1, color='#888'),
            hoverinfo='none',
            mode='lines'
        )

    def _create_node_trace(self, pos):
        node_x, node_y = [], []
        for node in self.graph.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
        return go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            hoverinfo='text',
            marker=dict(size=20, color='lightblue'),
            text=list(self.graph.nodes()),
            textposition="bottom center"
        )

    def _create_edge_labels(self, pos):
        labels = []
        for edge in self.graph.edges(data=True):
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            labels.append(
                go.Scatter(
                    x=[(x0 + x1) / 2],
                    y=[(y0 + y1) / 2],
                    mode='text',
                    text=[f"{edge[2]['weight']:.2f}"],
                    textposition="middle center"
                )
            )
        return labels

# Memory Management
class NexusMemory:
    def __init__(self, max_entries: int = 10000, decay_days: int = 30):
        self.store = defaultdict(dict)
        self.max_entries = max_entries
        self.decay_days = decay_days
        self.lock = threading.Lock()
        self.logger = logging.getLogger('NexusMemory')
        self.blockchain = Blockchain()

    def write(self, key: str, value: Any, emotion_weight: float = 0.5) -> Optional[str]:
        try:
            if not isinstance(key, str) or not (0 <= emotion_weight <= 1):
                self.logger.error(f"Invalid key type or emotion weight")
                return None

            # Convert numpy types to Python native types
            def convert_value(v):
                if isinstance(v, np.bool_):
                    return bool(v)
                if isinstance(v, np.integer):
                    return int(v)
                if isinstance(v, np.floating):
                    return float(v)
                if isinstance(v, np.ndarray):
                    return v.tolist()
                if isinstance(v, dict):
                    return {k: convert_value(val) for k, val in v.items()}
                if isinstance(v, (list, tuple)):
                    return [convert_value(item) for item in v]
                return v

            hashed = hashlib.md5(key.encode()).hexdigest()
            timestamp = datetime.now()

            with self.lock:
                if len(self.store) >= self.max_entries:
                    oldest = min(self.store.items(), key=lambda x: x[1].get('timestamp', timestamp))[0]
                    del self.store[oldest]

                self.store[hashed] = {
                    "value": convert_value(value),
                    "timestamp": timestamp,
                    "emotion_weight": float(emotion_weight)  # Ensure emotion_weight is native float
                }

                self.blockchain.add_block({
                    "key": hashed,
                    "value": value,
                    "timestamp": timestamp.isoformat()
                })

                return hashed
        except Exception as e:
            self.logger.error(f"Error writing to memory: {e}")
            return None

    def read(self, key: str) -> Optional[Any]:
        try:
            hashed = hashlib.md5(key.encode()).hexdigest()
            with self.lock:
                entry = self.store.get(hashed)
                if not entry:
                    return None

                if self._is_decayed(entry["timestamp"], entry.get("emotion_weight", 0.5)):
                    del self.store[hashed]
                    return None

                return entry["value"]
        except Exception as e:
            self.logger.error(f"Error reading from memory: {e}")
            return None

    def _is_decayed(self, timestamp: datetime, emotion_weight: float) -> bool:
        try:
            age = (datetime.now() - timestamp).total_seconds() / (24 * 3600)
            decay_factor = np.exp(-age / (self.decay_days * (1.5 - emotion_weight)))
            return decay_factor < 0.1
        except Exception as e:
            self.logger.error(f"Error checking decay: {e}")
            return True

    def audit(self) -> Dict[str, Any]:
        try:
            with self.lock:
                audit_data = {
                    k: {
                        "timestamp": v["timestamp"],
                        "emotion_weight": v["emotion_weight"],
                        "decayed": self._is_decayed(v["timestamp"], v["emotion_weight"])
                    }
                    for k, v in self.store.items()
                }
                self.blockchain.add_block({"audit": audit_data})
                return audit_data
        except Exception as e:
            self.logger.error(f"Error auditing memory: {e}")
            return {}

# Auditability
class Blockchain:
    def __init__(self):
        self.chain = [{
            "index": 0,
            "timestamp": datetime.now().isoformat(),
            "data": "Genesis Block",
            "prev_hash": "0"
        }]
        self.logger = logging.getLogger('Blockchain')

    def add_block(self, data: Dict[str, Any]) -> None:
        try:
            prev_block = self.chain[-1]
            # Convert datetime objects and numpy types to JSON serializable format
            def json_handler(obj):
                if isinstance(obj, datetime):
                    return obj.isoformat()
                if isinstance(obj, np.bool_):
                    return bool(obj)
                if isinstance(obj, np.integer):
                    return int(obj)
                if isinstance(obj, np.floating):
                    return float(obj)
                if isinstance(obj, np.ndarray):
                    return obj.tolist()
                raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
                
            block = {
                "index": len(self.chain),
                "timestamp": datetime.now().isoformat(),
                "data": json.dumps(data, default=json_handler),
                "prev_hash": self._hash_block(prev_block)
            }
            block["hash"] = self._hash_block(block)
            self.chain.append(block)
        except Exception as e:
            self.logger.error(f"Error adding block: {e}")

    def _hash_block(self, block: Dict[str, Any]) -> str:
        try:
            block_str = json.dumps(block, sort_keys=True)
            return hashlib.sha256(block_str.encode()).hexdigest()
        except Exception as e:
            self.logger.error(f"Error hashing block: {e}")
            return ""

    def verify(self) -> bool:
        try:
            for i in range(1, len(self.chain)):
                current = self.chain[i]
                prev = self.chain[i-1]
                if current["prev_hash"] != self._hash_block(prev):
                    return False
            return True
        except Exception as e:
            self.logger.error(f"Error verifying blockchain: {e}")
            return False

# Federated Learning
class FederatedTrainer:
    def __init__(self, num_clients: int):
        self.num_clients = num_clients
        self.logger = logging.getLogger('FederatedTrainer')
        
        if SYFT_AVAILABLE:
            self.hook = sy.TorchHook(torch)
            self.clients = [
                sy.VirtualWorker(self.hook, id=f"client_{i}") 
                for i in range(num_clients)
            ]
        else:
            self.hook = None
            self.clients = []
            self.logger.warning("Running without federated learning - PySyft not available")

    def train(self, weights: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
        try:
            if not SYFT_AVAILABLE:
                self.logger.debug("Skipping federated training - PySyft not available")
                return weights

            client_updates = []
            for client in self.clients:
                client_weights = deepcopy(weights)
                for virtue in client_weights:
                    client_weights[virtue] += np.random.normal(0, 0.01, size=client_weights[virtue].shape)
                client_updates.append(client_weights)
            
            aggregated = {}
            for virtue in weights:
                aggregated[virtue] = np.mean([update[virtue] for update in client_updates], axis=0)
            
            return aggregated
        except Exception as e:
            self.logger.error(f"Error in federated training: {e}")
            return weights

# Agent Base Class
class AegisAgent(ABC):
    def __init__(self, name: str, memory: NexusMemory):
        self.name = name
        self.memory = memory
        self.result: Dict[str, Any] = {}
        self.explanation: str = ""
        self.influence: Dict[str, float] = {}
        self.logger = logging.getLogger(f'AegisAgent.{name}')

    @abstractmethod
    def analyze(self, input_data: Dict[str, Any]) -> None:
        pass

    def report(self) -> Dict[str, Any]:
        return {
            "result": self.result,
            "explanation": self.explanation
        }

# Specialized Agents
class MetaJudgeAgent(AegisAgent):
    def __init__(self, name: str, memory: NexusMemory, weights: Dict[str, float]):
        super().__init__(name, memory)
        self.weights = weights

    def analyze(self, input_data: Dict[str, Any]) -> None:
        try:
            overrides = input_data.get("overrides", {})
            if not overrides:
                self.result = {"error": "No overrides provided"}
                self.explanation = "No overrides provided for analysis."
                return

            scores = []
            for agent, data in overrides.items():
                try:
                    influence = float(data.get("influence", 0.5))
                    reliability = float(data.get("reliability", 0.5))
                    severity = float(data.get("severity", 0.5))
                    
                    if not all(0 <= x <= 1 for x in [influence, reliability, severity]):
                        continue

                    score = (
                        self.weights["influence"] * influence +
                        self.weights["reliability"] * reliability +
                        self.weights["severity"] * severity
                    )
                    scores.append((agent, score))
                    self.influence[agent] = score
                except Exception as e:
                    self.logger.error(f"Error processing agent {agent}: {e}")

            if not scores:
                self.result = {"error": "No valid agents to score"}
                self.explanation = "No valid agents for meta-analysis."
                return

            scores.sort(key=lambda x: x[1], reverse=True)
            self.result = {
                "override_decision": scores[0][0],
                "scores": scores
            }
            self.explanation = f"Selected '{scores[0][0]}' with score {scores[0][1]:.2f}"
        except Exception as e:
            self.result = {"error": str(e)}
            self.explanation = f"Analysis failed: {e}"

class TemporalAgent(AegisAgent):
    def __init__(self, name: str, memory: NexusMemory, decay_thresholds: Dict[str, float]):
        super().__init__(name, memory)
        self.decay_thresholds = decay_thresholds

    def analyze(self, input_data: Dict[str, Any]) -> None:
        try:
            audit = self.memory.audit()
            recent_keys = sorted(
                audit.items(), 
                key=lambda x: x[1]["timestamp"],
                reverse=True
            )[:5]
            
            decay_rates = [1 if v["decayed"] else 0 for _, v in recent_keys]
            avg_decay = np.mean(decay_rates) if decay_rates else 0.0
            
            forecast = (
                "stable" if avg_decay < self.decay_thresholds["stable"]
                else "volatile" if avg_decay > self.decay_thresholds["volatile"]
                else "neutral"
            )
            
            self.result = {
                "temporal_forecast": forecast,
                "recent_keys": [k for k, _ in recent_keys],
                "decay_rate": avg_decay
            }
            self.explanation = f"Forecast: {forecast} (decay rate: {avg_decay:.2f})"
            
            for k, _ in recent_keys:
                self.influence[k] = 0.2
        except Exception as e:
            self.result = {"error": str(e)}
            self.explanation = f"Temporal analysis failed: {e}"

class VirtueAgent(AegisAgent):
    def __init__(self, name: str, memory: NexusMemory, virtue_weights: Dict[str, List[float]]):
        super().__init__(name, memory)
        self.tokenizer = AutoTokenizer.from_pretrained(
            "distilbert-base-uncased-finetuned-sst-2-english"
        )
        self.model = AutoModel.from_pretrained(
            "distilbert-base-uncased-finetuned-sst-2-english"
        )
        self.sentiment = pipeline(
            "sentiment-analysis",
            model="distilbert-base-uncased-finetuned-sst-2-english"
        )
        self.virtue_weights = {k: np.array(v) for k, v in virtue_weights.items()}
        self.federated_trainer = None

    def set_federated_trainer(self, trainer: FederatedTrainer):
        self.federated_trainer = trainer

    def analyze(self, input_data: Dict[str, Any]) -> None:
        try:
            text = input_data.get("text", "")
            if not text or not isinstance(text, str):
                self.result = {"error": "Invalid input text"}
                self.explanation = "No valid text provided for analysis."
                return

            # Check cache
            mem_key = f"virtue_cache_{hashlib.md5(text.encode()).hexdigest()}"
            cached = self.memory.read(mem_key)
            if cached:
                self.result = {"virtue_profile": cached}
                self.explanation = f"Retrieved cached analysis"
                self.influence.update({k: v for k, v in cached.items()})
                return

            # Perform analysis
            sentiment_result = self.sentiment(text)[0]
            sentiment = 1.0 if sentiment_result["label"] == "POSITIVE" else -1.0
            sentiment_score = sentiment_result["score"]

            inputs = self.tokenizer(
                text,
                return_tensors="pt",
                truncation=True,
                max_length=512
            )
            with torch.no_grad():
                outputs = self.model(**inputs)
            
            embeddings = outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
            subjectivity = min(max(np.std(embeddings), 0.0), 1.0)
            neutrality = 1.0 - abs(sentiment)

            if self.federated_trainer:
                self.virtue_weights = self.federated_trainer.train(self.virtue_weights)

            features = np.array([
                sentiment * sentiment_score,
                subjectivity,
                neutrality
            ])

            virtues = {}
            for virtue, weights in self.virtue_weights.items():
                # Convert numpy types to Python native types
                score = float(max(np.dot(weights, features), 0.0))
                virtues[virtue] = float(min(round(score, 2), 1.0))  # Ensure native float

            # Convert all numpy types in the result
            self.result = {
                "virtue_profile": {
                    k: float(v) if isinstance(v, (np.number, float)) else v
                    for k, v in virtues.items()
                }
            }
            self.explanation = (
                f"Virtues analyzed: {', '.join(f'{k}: {v:.2f}' for k, v in virtues.items())}"
            )
            
            for virtue, score in virtues.items():
                self.influence[virtue] = float(score)  # Ensure native float
            
            self.memory.write(mem_key, virtues, emotion_weight=0.8)
        except Exception as e:
            self.result = {"error": str(e)}

            self.explanation = f"Virtue analysis failed: {e}"