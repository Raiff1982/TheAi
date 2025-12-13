
# Default configuration for AEGIS integration
AEGIS_CONFIG = {
    "meta_judge_weights": {
        "influence": 0.5,
        "reliability": 0.3,
        "severity": 0.2
    },
    "temporal_decay_thresholds": {
        "stable": 0.3,
        "volatile": 0.7
    },
    "virtue_weights": {
        "compassion": [0.7, 0.3, -0.1],
        "integrity": [0.4, -0.6, 0.2],
        "courage": [0.1, 0.5, 0.4],
        "wisdom": [0.3, -0.7, 0.2]
    },
    "memory_decay_days": 30,
    "memory_max_entries": 10000,
    "log_level": "INFO",
    "federated_learning": {
        "num_clients": 2,
        "aggregation_rounds": 1
    }

}