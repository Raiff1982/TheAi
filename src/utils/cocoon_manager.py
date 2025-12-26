from datetime import datetime
import os
import json
import logging
from typing import List, Dict, Any, Optional
import gzip
import shutil
import numpy as np

logger = logging.getLogger(__name__)

class NumpyEncoder(json.JSONEncoder):
    """Custom JSON encoder that handles numpy types"""
    def default(self, obj):
        if isinstance(obj, (np.bool_, np.integer)):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NumpyEncoder, self).default(obj)

class CocoonManager:
    """Manages Codette's cocoon data storage and retrieval"""
    
    def __init__(self, base_dir: str = "./cocoons"):
        self.base_dir = base_dir
        self.cocoon_data = []  # Backward-compatible; populated on-demand
        self.cocoon_index: List[Dict[str, Any]] = []  # Metadata-only index
        self.quantum_state = {"coherence": 0.5}
        self.hot_retention = int(os.getenv("CODETTE_COCOON_HOT_RETENTION", "20"))
        self.archive_dir = os.path.join(self.base_dir, "archive")
        self.compress_level = 6
        self._ensure_cocoon_dir()
        
    def _ensure_cocoon_dir(self):
        """Ensure cocoon directory exists"""
        os.makedirs(self.base_dir, exist_ok=True)
        os.makedirs(self.archive_dir, exist_ok=True)
        
    def load_cocoons(self) -> None:
        """Load cocoon metadata only (lazy full-load on demand)."""
        try:
            # Ensure directory exists
            os.makedirs(self.base_dir, exist_ok=True)
            
            cocoon_files = [
                f for f in os.listdir(self.base_dir) 
                if f.endswith('.cocoon')
            ]
            logger.info(f"Found {len(cocoon_files)} cocoon files in {self.base_dir}")
            
            self.cocoon_index = []
            self.cocoon_data = []
            latest_quantum_state = None
            for fname in cocoon_files:
                try:
                    full_path = os.path.join(self.base_dir, fname)
                    with open(full_path, 'r') as f:
                        cocoon = json.load(f)
                        if not self._validate_cocoon(cocoon):
                            continue

                        # Build metadata entry
                        data_block = cocoon.get('data', {}) if isinstance(cocoon, dict) else {}
                        quantum_state = data_block.get('quantum_state')
                        metadata_entry = {
                            "timestamp": cocoon.get('timestamp'),
                            "type": data_block.get('type', 'codette'),
                            "path": full_path,
                            "size_bytes": os.path.getsize(full_path),
                            "quantum_state": self._normalize_quantum_state(quantum_state) if quantum_state else None,
                            "has_quantum_state": bool(quantum_state)
                        }
                        self.cocoon_index.append(metadata_entry)

                        # Track latest quantum state without holding full data
                        if metadata_entry["quantum_state"]:
                            if latest_quantum_state is None:
                                latest_quantum_state = metadata_entry["quantum_state"].copy()
                            elif metadata_entry.get("timestamp", "") > (self.quantum_state.get("timestamp", "") if isinstance(self.quantum_state, dict) else ""):
                                latest_quantum_state = metadata_entry["quantum_state"].copy()
                except Exception as e:
                    logger.error(f"Error loading cocoon {fname}: {e}")
                    continue
            # Sort metadata by timestamp
            self.cocoon_index = sorted(
                [c for c in self.cocoon_index if c.get('timestamp')],
                key=lambda x: x.get('timestamp', '0'),
                reverse=True
            )

            if latest_quantum_state:
                self.quantum_state = latest_quantum_state

            logger.info(
                f"Indexed {len(self.cocoon_index)} cocoons (metadata-only); full content loads on demand"
            )
            self._rotate_and_compress_archives()
            
        except Exception as e:
            logger.error(f"Error loading cocoons: {e}")
            self.cocoon_data = []
            self.cocoon_index = []
            # Ensure we have a valid quantum state
            if not isinstance(self.quantum_state, dict) or 'coherence' not in self.quantum_state:
                self.quantum_state = {"coherence": 0.5}
            
    def _validate_cocoon(self, cocoon: Dict[str, Any]) -> bool:
        """Validate cocoon data structure"""
        required_fields = ['timestamp', 'data']
        return all(field in cocoon for field in required_fields)

    def _normalize_quantum_state(self, quantum_state: Any) -> Dict[str, Any]:
        """Normalize quantum state to dict with coherence key."""
        if isinstance(quantum_state, dict):
            return quantum_state
        if isinstance(quantum_state, list) and quantum_state:
            return {"coherence": sum(quantum_state) / len(quantum_state)}
        return {"coherence": 0.5}
        
    def save_cocoon(
        self, 
        data: Dict[str, Any],
        cocoon_type: str = "codette"
    ) -> bool:
        """Save new cocoon data to file"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{cocoon_type}_cocoon_{timestamp}.cocoon"
            filepath = os.path.join(self.base_dir, filename)
            
            # If data has its own quantum state, update our state
            if "quantum_state" in data:
                self.quantum_state = data["quantum_state"]
            
            cocoon = {
                "timestamp": timestamp,
                "data": {
                    **data,
                    "quantum_state": self.quantum_state.copy()
                }
            }
            
            with open(filepath, 'w') as f:
                json.dump(cocoon, f, indent=2, cls=NumpyEncoder)
                
            # Update metadata index lazily
            metadata_entry = {
                "timestamp": timestamp,
                "type": data.get("type", cocoon_type),
                "path": filepath,
                "size_bytes": os.path.getsize(filepath),
                "quantum_state": self.quantum_state.copy(),
                "has_quantum_state": True
            }
            self.cocoon_index.insert(0, metadata_entry)
            # Preserve backward-compatible attribute (empty unless explicitly loaded)
            if self.cocoon_data is not None:
                self.cocoon_data.insert(0, cocoon)
            logger.info(f"Saved cocoon: {filename}")
            self._rotate_and_compress_archives()
            return True
            
        except Exception as e:
            logger.error(f"Error saving cocoon: {e}")
            return False
            
    def get_latest_quantum_state(self) -> Dict[str, float]:
        """Get the most recent quantum state"""
        # Ensure quantum_state is always a proper dict
        if not isinstance(self.quantum_state, dict):
            self.quantum_state = {"coherence": 0.5}
        return self.quantum_state.copy()
        
    def get_latest_cocoons(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Get the most recent cocoons (loads content on demand)."""
        latest_meta = self.cocoon_index[:limit]
        cocoons: List[Dict[str, Any]] = []
        for meta in latest_meta:
            loaded = self._load_cocoon_file(meta.get("path"))
            if loaded:
                cocoons.append(loaded)
        return cocoons

    def get_latest_rc_xi(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Return latest RC+xi cocoon records (loads full content)."""
        rc_meta = [m for m in self.cocoon_index if m.get("type") == "rc_xi"]
        rc_meta = rc_meta[:limit]
        records: List[Dict[str, Any]] = []
        for meta in rc_meta:
            loaded = self._load_cocoon_file(meta.get("path"))
            if loaded:
                records.append(loaded)
        return records

    def _rotate_and_compress_archives(self):
        """Keep hottest N cocoons in base_dir; compress older ones into archive."""
        try:
            # Refresh index ordering
            self.cocoon_index = sorted(
                self.cocoon_index,
                key=lambda x: x.get('timestamp', '0'),
                reverse=True
            )

            hot = self.cocoon_index[: self.hot_retention]
            cold = self.cocoon_index[self.hot_retention :]

            for meta in cold:
                path = meta.get("path")
                if not path or not os.path.exists(path):
                    continue
                
                # Skip if already archived (already ends with .gz)
                if str(path).endswith(".gz"):
                    meta["archived"] = True
                    continue
                
                archived_path = os.path.join(
                    self.archive_dir,
                    os.path.basename(path) + ".gz"
                )
                
                # Skip if archive file already exists (shouldn't happen, but be safe)
                if os.path.exists(archived_path):
                    logger.debug(f"Archive already exists: {archived_path}")
                    continue
                
                try:
                    with open(path, 'rb') as src, gzip.open(archived_path, 'wb', compresslevel=self.compress_level) as dst:
                        shutil.copyfileobj(src, dst)
                    # Remove original cold file after successful compression
                    os.remove(path)
                    meta["path"] = archived_path
                    meta["archived"] = True
                    logger.debug(f"Archived cocoon: {os.path.basename(path)}")
                except Exception as e:
                    logger.error(f"Failed to archive cocoon {path}: {e}")

            # Update index to reflect hot/cold segmentation
            self.cocoon_index = hot + cold
        except Exception as e:
            logger.error(f"Error rotating/compressing cocoons: {e}")

    def _load_cocoon_file(self, path: Optional[str]) -> Optional[Dict[str, Any]]:
        if not path or not os.path.exists(path):
            return None
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load cocoon file {path}: {e}")
            return None
        
    def update_quantum_state(self, new_state: Dict[str, float]) -> None:
        """Update the current quantum state and save it"""
        self.quantum_state.update(new_state)
        logger.info(f"Updated quantum state: {self.quantum_state}")
        
        # Save the new state in a cocoon
        self.save_cocoon({
            "type": "quantum_update",
            "quantum_state": self.quantum_state.copy()
        })

    def get_archival_stats(self) -> Dict[str, Any]:
        """Return lightweight archival metrics without loading cocoon contents."""
        try:
            indexed_total = len(self.cocoon_index)
            hot_count = min(indexed_total, self.hot_retention)
            cold_count = max(indexed_total - self.hot_retention, 0)
            archived_entries = [
                meta for meta in self.cocoon_index
                if meta.get("archived") or str(meta.get("path", "")).endswith(".gz")
            ]

            archive_files = []
            archive_size = 0
            if os.path.isdir(self.archive_dir):
                for fname in os.listdir(self.archive_dir):
                    if not fname.endswith(".gz"):
                        continue
                    archive_files.append(fname)
                    try:
                        archive_size += os.path.getsize(os.path.join(self.archive_dir, fname))
                    except Exception:
                        continue

            archived_count = max(len(archived_entries), len(archive_files))

            return {
                "hot_retention": self.hot_retention,
                "indexed_total": indexed_total,
                "hot_count": hot_count,
                "cold_count": cold_count,
                "archived_count": archived_count,
                "archive_dir_size_bytes": archive_size,
                "archive_dir": self.archive_dir,
            }
        except Exception as e:
            logger.debug(f"Failed to collect archival stats: {e}")
            return {
                "hot_retention": self.hot_retention,
                "indexed_total": len(self.cocoon_index),
                "hot_count": 0,
                "cold_count": 0,
                "archived_count": 0,
                "archive_dir_size_bytes": 0,
                "archive_dir": self.archive_dir,
                "error": str(e),
            }

    @property
    def cocoon_count(self) -> int:
        """Number of indexed cocoons (metadata-based)."""
        return len(self.cocoon_index)