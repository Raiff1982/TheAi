"""
Advanced Data Processing Component for Codette
Handles sophisticated data processing and analysis tasks
"""

import logging
from typing import Dict, List, Any, Optional, Union, Tuple
from datetime import datetime
import json
import asyncio
from pathlib import Path

try:
    import numpy as np
except Exception:
    np = None

logger = logging.getLogger(__name__)

class AdvancedDataProcessor:
    """Advanced data processing and analysis engine"""
    
    def __init__(self,
                 batch_size: int = 100,
                 processing_threshold: float = 0.8,
                 cache_size: int = 1000):
        """Initialize the advanced data processor"""
        self.batch_size = batch_size
        self.processing_threshold = processing_threshold
        self.cache_size = cache_size
        
        # Initialize state
        self.processing_cache = {}
        self.data_patterns = {}
        self.current_state = {
            "processing_mode": "standard",
            "active_tasks": 0,
            "cache_usage": 0.0,
            "performance_metrics": {}
        }
        
        logger.info("Advanced Data Processor initialized")
        
    async def process_data(self,
                          data: Union[Dict[str, Any], List[Any]],
                          context: Optional[Dict[str, Any]] = None,
                          mode: str = "standard") -> Dict[str, Any]:
        """Process data with advanced analysis"""
        try:
            # Validate and prepare data
            prepared_data = self._prepare_data(data)
            
            # Set processing mode
            self.current_state["processing_mode"] = mode
            
            # Process in batches if needed
            if len(prepared_data) > self.batch_size:
                result = await self._batch_process(prepared_data, context)
            else:
                result = await self._single_process(prepared_data, context)
                
            # Update metrics
            self._update_metrics(result)
            
            return result
            
        except Exception as e:
            logger.error(f"Error processing data: {e}")
            return {
                "status": "error",
                "message": str(e),
                "timestamp": datetime.now().isoformat()
            }
            
    async def analyze_patterns(self,
                             data: Dict[str, Any],
                             analysis_type: str = "comprehensive") -> Dict[str, Any]:
        """Analyze patterns in data"""
        try:
            # Extract features
            features = self._extract_features(data)
            
            # Perform pattern analysis
            patterns = await self._analyze_features(features, analysis_type)
            
            # Generate insights
            insights = self._generate_insights(patterns)
            
            return {
                "status": "success",
                "patterns": patterns,
                "insights": insights,
                "confidence": self._calculate_confidence(patterns),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error analyzing patterns: {e}")
            return {"status": "error", "message": str(e)}
            
    def transform_data(self,
                      data: Any,
                      transformation_type: str,
                      parameters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Transform data according to specified type"""
        try:
            # Validate transformation type
            if not self._validate_transformation(transformation_type, parameters):
                raise ValueError(f"Invalid transformation: {transformation_type}")
                
            # Apply transformation
            transformed = self._apply_transformation(data, transformation_type, parameters)
            
            # Validate result
            if not self._validate_result(transformed):
                raise ValueError("Transformation result validation failed")
                
            return {
                "status": "success",
                "original": data,
                "transformed": transformed,
                "transformation_type": transformation_type,
                "parameters": parameters,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error transforming data: {e}")
            return {"status": "error", "message": str(e)}
            
    def cache_data(self,
                  key: str,
                  data: Any,
                  metadata: Optional[Dict[str, Any]] = None) -> bool:
        """Cache data for faster access"""
        try:
            if len(self.processing_cache) >= self.cache_size:
                self._cleanup_cache()
                
            self.processing_cache[key] = {
                "data": data,
                "metadata": metadata or {},
                "timestamp": datetime.now().isoformat(),
                "access_count": 0
            }
            
            self.current_state["cache_usage"] = len(self.processing_cache) / self.cache_size
            return True
            
        except Exception as e:
            logger.error(f"Error caching data: {e}")
            return False
            
    def _prepare_data(self, data: Union[Dict[str, Any], List[Any]]) -> List[Any]:
        """Prepare data for processing"""
        try:
            if isinstance(data, dict):
                return [self._normalize_dict(data)]
            elif isinstance(data, list):
                return [self._normalize_dict(item) if isinstance(item, dict) else item
                       for item in data]
            else:
                return [data]
                
        except Exception as e:
            logger.error(f"Error preparing data: {e}")
            return []
            
    def _normalize_dict(self, d: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize dictionary data"""
        try:
            normalized = {}
            for key, value in d.items():
                if isinstance(value, dict):
                    normalized[key] = self._normalize_dict(value)
                elif isinstance(value, list):
                    normalized[key] = [
                        self._normalize_dict(item) if isinstance(item, dict) else item
                        for item in value
                    ]
                else:
                    normalized[key] = value
            return normalized
            
        except Exception as e:
            logger.error(f"Error normalizing dictionary: {e}")
            return d
            
    async def _batch_process(self,
                           data: List[Any],
                           context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Process data in batches"""
        try:
            batches = [
                data[i:i + self.batch_size]
                for i in range(0, len(data), self.batch_size)
            ]
            
            # Process batches concurrently
            tasks = [
                self._single_process(batch, context)
                for batch in batches
            ]
            
            results = await asyncio.gather(*tasks)
            
            # Combine results
            combined = self._combine_batch_results(results)
            
            return {
                "status": "success",
                "results": combined,
                "batches_processed": len(batches),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error in batch processing: {e}")
            return {"status": "error", "message": str(e)}
            
    async def _single_process(self,
                            data: List[Any],
                            context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Process a single batch of data"""
        try:
            # Apply processing steps
            validated = self._validate_data(data)
            transformed = self._transform_batch(validated)
            analyzed = await self._analyze_batch(transformed, context)
            
            return {
                "status": "success",
                "processed_data": analyzed,
                "statistics": self._calculate_statistics(analyzed),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error in single process: {e}")
            return {"status": "error", "message": str(e)}
            
    def _validate_data(self, data: List[Any]) -> List[Any]:
        """Validate data entries"""
        valid_data = []
        try:
            for item in data:
                if self._is_valid_entry(item):
                    valid_data.append(item)
                    
            return valid_data
            
        except Exception as e:
            logger.error(f"Error validating data: {e}")
            return valid_data
            
    def _transform_batch(self, data: List[Any]) -> List[Any]:
        """Apply transformations to a batch of data"""
        transformed = []
        try:
            for item in data:
                if isinstance(item, dict):
                    transformed.append(self._transform_dict(item))
                elif isinstance(item, (list, tuple)):
                    transformed.append(self._transform_sequence(item))
                else:
                    transformed.append(self._transform_scalar(item))
                    
            return transformed
            
        except Exception as e:
            logger.error(f"Error transforming batch: {e}")
            return transformed
            
    async def _analyze_batch(self,
                           data: List[Any],
                           context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze a batch of transformed data"""
        try:
            # Extract features
            features = [self._extract_features(item) for item in data]
            
            # Analyze patterns
            patterns = await self._analyze_features(features, "batch")
            
            # Generate insights
            insights = self._generate_insights(patterns)
            
            return {
                "features": features,
                "patterns": patterns,
                "insights": insights,
                "context_influence": self._evaluate_context(context)
            }
            
        except Exception as e:
            logger.error(f"Error analyzing batch: {e}")
            return {}
            
    def _extract_features(self, data: Any) -> Dict[str, Any]:
        """Extract features from data"""
        features = {}
        try:
            if isinstance(data, dict):
                features = self._extract_dict_features(data)
            elif isinstance(data, (list, tuple)):
                features = self._extract_sequence_features(data)
            else:
                features = self._extract_scalar_features(data)
                
            features["timestamp"] = datetime.now().isoformat()
            
        except Exception as e:
            logger.error(f"Error extracting features: {e}")
            
        return features
        
    async def _analyze_features(self,
                              features: Union[Dict[str, Any], List[Dict[str, Any]]],
                              analysis_type: str) -> Dict[str, Any]:
        """Analyze extracted features"""
        try:
            if isinstance(features, list):
                # Batch analysis
                return await self._analyze_feature_batch(features)
            else:
                # Single item analysis
                return self._analyze_single_features(features)
                
        except Exception as e:
            logger.error(f"Error analyzing features: {e}")
            return {}
            
    def _generate_insights(self, patterns: Dict[str, Any]) -> List[str]:
        """Generate insights from analyzed patterns"""
        insights = []
        try:
            # Process pattern categories
            for category, data in patterns.items():
                if isinstance(data, dict):
                    insights.extend(
                        self._generate_category_insights(category, data)
                    )
                    
            return insights[:5]  # Limit to top 5 insights
            
        except Exception as e:
            logger.error(f"Error generating insights: {e}")
            return ["Error generating insights"]
            
    def _calculate_confidence(self, patterns: Dict[str, Any]) -> float:
        """Calculate confidence in pattern analysis"""
        try:
            if not patterns:
                return 0.0
                
            # Calculate based on pattern strength and coverage
            strengths = []
            coverages = []
            
            for pattern_data in patterns.values():
                if isinstance(pattern_data, dict):
                    strengths.append(pattern_data.get("strength", 0))
                    coverages.append(pattern_data.get("coverage", 0))
                    
            if not strengths or not coverages:
                return 0.0
                
            if np is not None:
                return float(min(1.0, (np.mean(strengths) + np.mean(coverages)) / 2))
            else:
                s_mean = sum(strengths)/len(strengths) if strengths else 0.0
                c_mean = sum(coverages)/len(coverages) if coverages else 0.0
                return min(1.0, (s_mean + c_mean) / 2)
            
        except Exception as e:
            logger.error(f"Error calculating confidence: {e}")
            return 0.0
            
    def _update_metrics(self, result: Dict[str, Any]):
        """Update processing metrics"""
        try:
            metrics = self.current_state["performance_metrics"]
            
            # Update processing counts
            metrics["total_processed"] = metrics.get("total_processed", 0) + 1
            metrics["successful"] = metrics.get("successful", 0) + \
                                 (1 if result.get("status") == "success" else 0)
                                 
            # Calculate success rate
            metrics["success_rate"] = metrics["successful"] / metrics["total_processed"]
            
            # Update timestamp
            metrics["last_update"] = datetime.now().isoformat()
            
        except Exception as e:
            logger.error(f"Error updating metrics: {e}")
            
    def _cleanup_cache(self):
        """Clean up least recently used cache entries"""
        try:
            if len(self.processing_cache) <= self.cache_size * 0.9:
                return
                
            # Sort by access count and timestamp
            sorted_cache = sorted(
                self.processing_cache.items(),
                key=lambda x: (x[1]["access_count"], x[1]["timestamp"])
            )
            
            # Remove oldest, least accessed entries
            items_to_remove = int(self.cache_size * 0.2)  # Remove 20%
            for key, _ in sorted_cache[:items_to_remove]:
                del self.processing_cache[key]
                
        except Exception as e:
            logger.error(f"Error cleaning cache: {e}")
            
    def get_state(self) -> Dict[str, Any]:
        """Get current state of the processor"""
        return self.current_state.copy()
        
    def get_cache_info(self) -> Dict[str, Any]:
        """Get information about the cache"""
        return {
            "size": len(self.processing_cache),
            "capacity": self.cache_size,
            "usage": self.current_state["cache_usage"],
            "timestamp": datetime.now().isoformat()
        }
        
    def _is_valid_entry(self, entry: Any) -> bool:
        """Check if a data entry is valid"""
        try:
            if entry is None:
                return False
                
            if isinstance(entry, (dict, list, tuple)):
                return len(entry) > 0
                
            return True
            
        except Exception:
            return False
            
    def _transform_dict(self, d: Dict[str, Any]) -> Dict[str, Any]:
        """Transform dictionary data"""
        transformed = {}
        try:
            for key, value in d.items():
                if isinstance(value, dict):
                    transformed[key] = self._transform_dict(value)
                elif isinstance(value, (list, tuple)):
                    transformed[key] = self._transform_sequence(value)
                else:
                    transformed[key] = self._transform_scalar(value)
                    
        except Exception as e:
            logger.error(f"Error transforming dictionary: {e}")
            
        return transformed
        
    def _transform_sequence(self, seq: Union[List[Any], Tuple[Any, ...]]) -> List[Any]:
        """Transform sequence data"""
        transformed = []
        try:
            for item in seq:
                if isinstance(item, dict):
                    transformed.append(self._transform_dict(item))
                elif isinstance(item, (list, tuple)):
                    transformed.append(self._transform_sequence(item))
                else:
                    transformed.append(self._transform_scalar(item))
                    
        except Exception as e:
            logger.error(f"Error transforming sequence: {e}")
            
        return transformed
        
    def _transform_scalar(self, value: Any) -> Any:
        """Transform scalar value"""
        try:
            if isinstance(value, (int, float)):
                return float(value)
            elif isinstance(value, str):
                return value.strip()
            else:
                return value
                
        except Exception as e:
            logger.error(f"Error transforming scalar: {e}")
            return value
            
    def _extract_dict_features(self, d: Dict[str, Any]) -> Dict[str, Any]:
        """Extract features from dictionary data"""
        features = {
            "type": "dict",
            "size": len(d),
            "keys": list(d.keys()),
            "value_types": {}
        }
        
        try:
            for key, value in d.items():
                features["value_types"][key] = type(value).__name__
                
        except Exception as e:
            logger.error(f"Error extracting dict features: {e}")
            
        return features
        
    def _extract_sequence_features(self, seq: Union[List[Any], Tuple[Any, ...]]) -> Dict[str, Any]:
        """Extract features from sequence data"""
        features = {
            "type": type(seq).__name__,
            "length": len(seq),
            "unique_count": len(set(str(x) for x in seq))
        }
        
        try:
            if all(isinstance(x, (int, float)) for x in seq):
                if np is not None:
                    features.update({
                        "mean": float(np.mean(seq)),
                        "std": float(np.std(seq)),
                        "min": float(np.min(seq)),
                        "max": float(np.max(seq))
                    })
                else:
                    features.update({
                        "mean": float(sum(seq)/len(seq)),
                        "std": float((sum((x - (sum(seq)/len(seq)))**2 for x in seq)/len(seq))**0.5),
                        "min": float(min(seq)),
                        "max": float(max(seq))
                    })
                
        except Exception as e:
            logger.error(f"Error extracting sequence features: {e}")
            
        return features
        
    def _extract_scalar_features(self, value: Any) -> Dict[str, Any]:
        """Extract features from scalar value"""
        features = {
            "type": type(value).__name__,
            "value": str(value)
        }
        
        try:
            if isinstance(value, (int, float)):
                features["numeric"] = True
                features["magnitude"] = abs(float(value))
            elif isinstance(value, str):
                features["length"] = len(value)
                features["word_count"] = len(value.split())
                
        except Exception as e:
            logger.error(f"Error extracting scalar features: {e}")
            
        return features
        
    async def _analyze_feature_batch(self,
                                   features: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze a batch of features"""
        try:
            # Analyze in parallel chunks
            chunk_size = min(100, len(features))
            chunks = [
                features[i:i + chunk_size]
                for i in range(0, len(features), chunk_size)
            ]
            
            tasks = [
                self._analyze_feature_chunk(chunk)
                for chunk in chunks
            ]
            
            chunk_results = await asyncio.gather(*tasks)
            
            # Combine chunk results
            return self._combine_chunk_results(chunk_results)
            
        except Exception as e:
            logger.error(f"Error in batch feature analysis: {e}")
            return {}
            
    async def _analyze_feature_chunk(self,
                                   features: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze a chunk of features"""
        try:
            # Analyze each feature
            analyses = [
                self._analyze_single_features(feature)
                for feature in features
            ]
            
            # Combine analyses
            combined = {}
            for analysis in analyses:
                for key, value in analysis.items():
                    if key not in combined:
                        combined[key] = []
                    combined[key].append(value)
                    
            return combined
            
        except Exception as e:
            logger.error(f"Error analyzing feature chunk: {e}")
            return {}
            
    def _analyze_single_features(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze features of a single item"""
        analysis = {}
        try:
            # Analyze by feature type
            if features.get("type") == "dict":
                analysis.update(self._analyze_dict_features(features))
            elif features.get("type") in ("list", "tuple"):
                analysis.update(self._analyze_sequence_features(features))
            else:
                analysis.update(self._analyze_scalar_features(features))
                
        except Exception as e:
            logger.error(f"Error analyzing single features: {e}")
            
        return analysis
        
    def _combine_chunk_results(self,
                             results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Combine results from multiple chunks"""
        combined = {}
        try:
            # Combine all keys
            all_keys = set()
            for result in results:
                all_keys.update(result.keys())
                
            # Merge values
            for key in all_keys:
                values = []
                for result in results:
                    if key in result:
                        values.extend(result[key])
                combined[key] = values
                
        except Exception as e:
            logger.error(f"Error combining chunk results: {e}")
            
        return combined
        
    def _generate_category_insights(self,
                                  category: str,
                                  data: Dict[str, Any]) -> List[str]:
        """Generate insights for a specific category"""
        insights = []
        try:
            # Generate based on category type
            if category == "structure":
                insights.extend(self._generate_structure_insights(data))
            elif category == "content":
                insights.extend(self._generate_content_insights(data))
            elif category == "patterns":
                insights.extend(self._generate_pattern_insights(data))
                
        except Exception as e:
            logger.error(f"Error generating category insights: {e}")
            
        return insights
        
    def _generate_structure_insights(self, data: Dict[str, Any]) -> List[str]:
        """Generate insights about data structure"""
        insights = []
        try:
            if "depth" in data:
                insights.append(
                    f"Data structure has depth of {data['depth']} levels"
                )
            if "breadth" in data:
                insights.append(
                    f"Contains {data['breadth']} top-level elements"
                )
                
        except Exception as e:
            logger.error(f"Error generating structure insights: {e}")
            
        return insights
        
    def _generate_content_insights(self, data: Dict[str, Any]) -> List[str]:
        """Generate insights about data content"""
        insights = []
        try:
            if "types" in data:
                type_counts = data["types"]
                primary_type = max(type_counts.items(), key=lambda x: x[1])[0]
                insights.append(
                    f"Primary data type is {primary_type}"
                )
                
        except Exception as e:
            logger.error(f"Error generating content insights: {e}")
            
        return insights
        
    def _generate_pattern_insights(self, data: Dict[str, Any]) -> List[str]:
        """Generate insights about data patterns"""
        insights = []
        try:
            if "frequency" in data:
                freq = data["frequency"]
                most_common = max(freq.items(), key=lambda x: x[1])[0]
                insights.append(
                    f"Most frequent pattern: {most_common}"
                )
                
        except Exception as e:
            logger.error(f"Error generating pattern insights: {e}")
            
        return insights
        
    def _evaluate_context(self, context: Optional[Dict[str, Any]]) -> float:
        """Evaluate the influence of context"""
        try:
            if not context:
                return 0.5
                
            # Calculate context relevance
            features = self._extract_features(context)
            analysis = self._analyze_single_features(features)
            
            # Simplified scoring
            score = min(1.0, len(analysis) / 10)
            
            return score
            
        except Exception as e:
            logger.error(f"Error evaluating context: {e}")
            return 0.5