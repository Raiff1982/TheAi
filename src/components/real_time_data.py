"""
This module provides real-time data integration and processing capabilities.
"""

import asyncio
import aiohttp
import json
from typing import Dict, Any, List, Optional
from datetime import datetime

class RealTimeDataIntegrator:
    def __init__(self):
        self.data_sources = {}
        self.active_streams = {}
        self.data_buffer = {}
        self.session = None

    async def initialize(self):
        """
        Initialize the data integrator with a new aiohttp session.
        """
        if not self.session:
            self.session = aiohttp.ClientSession()

    async def add_data_source(self, source_id: str, config: Dict[str, Any]) -> bool:
        """
        Add a new data source for real-time integration.
        
        Args:
            source_id: Unique identifier for the data source
            config: Configuration for the data source
            
        Returns:
            Success status
        """
        try:
            self.data_sources[source_id] = {
                "config": config,
                "status": "configured",
                "last_update": None,
                "error_count": 0
            }
            return True
        except Exception as e:
            print(f"Error adding data source: {e}")
            return False

    async def start_stream(self, source_id: str) -> bool:
        """
        Start streaming data from a specific source.
        
        Args:
            source_id: ID of the data source to stream from
            
        Returns:
            Success status
        """
        if source_id not in self.data_sources:
            return False
            
        try:
            # Initialize buffer for this stream
            self.data_buffer[source_id] = []
            
            # Start async streaming task
            self.active_streams[source_id] = asyncio.create_task(
                self._stream_data(source_id)
            )
            
            return True
        except Exception as e:
            print(f"Error starting stream: {e}")
            return False

    async def stop_stream(self, source_id: str) -> bool:
        """
        Stop streaming from a specific source.
        
        Args:
            source_id: ID of the data source to stop
            
        Returns:
            Success status
        """
        if source_id in self.active_streams:
            try:
                self.active_streams[source_id].cancel()
                del self.active_streams[source_id]
                return True
            except Exception as e:
                print(f"Error stopping stream: {e}")
                
        return False

    async def get_latest_data(self, source_id: str) -> Optional[Dict[str, Any]]:
        """
        Get the latest data from a specific source.
        
        Args:
            source_id: ID of the data source to query
            
        Returns:
            Latest data point if available
        """
        if source_id in self.data_buffer and self.data_buffer[source_id]:
            return self.data_buffer[source_id][-1]
        return None

    async def _stream_data(self, source_id: str):
        """
        Internal method to handle continuous data streaming.
        """
        config = self.data_sources[source_id]["config"]
        url = config.get("url")
        interval = config.get("interval", 1.0)  # Default to 1 second
        
        while True:
            try:
                if not self.session:
                    await self.initialize()
                
                async with self.session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        self._process_data(source_id, data)
                    else:
                        self.data_sources[source_id]["error_count"] += 1
                        
            except Exception as e:
                print(f"Stream error for {source_id}: {e}")
                self.data_sources[source_id]["error_count"] += 1
                
            await asyncio.sleep(interval)

    def _process_data(self, source_id: str, data: Dict[str, Any]):
        """
        Process incoming data from a stream.
        """
        # Add timestamp
        processed_data = {
            "timestamp": datetime.now().isoformat(),
            "data": data
        }
        
        # Update buffer
        self.data_buffer[source_id].append(processed_data)
        
        # Limit buffer size
        max_buffer = self.data_sources[source_id]["config"].get("buffer_size", 1000)
        if len(self.data_buffer[source_id]) > max_buffer:
            self.data_buffer[source_id] = self.data_buffer[source_id][-max_buffer:]
            
        # Update source status
        self.data_sources[source_id]["last_update"] = processed_data["timestamp"]
        self.data_sources[source_id]["status"] = "active"

    def get_source_status(self, source_id: str) -> Dict[str, Any]:
        """
        Get status information for a data source.
        
        Args:
            source_id: ID of the data source to query
            
        Returns:
            Status information for the source
        """
        if source_id not in self.data_sources:
            return {"status": "not_found"}
            
        source = self.data_sources[source_id]
        return {
            "status": source["status"],
            "last_update": source["last_update"],
            "error_count": source["error_count"],
            "buffer_size": len(self.data_buffer.get(source_id, []))
        }

    async def clear_data(self, source_id: str) -> bool:
        """
        Clear stored data for a specific source.
        
        Args:
            source_id: ID of the data source to clear
            
        Returns:
            Success status
        """
        if source_id in self.data_buffer:
            self.data_buffer[source_id] = []
            return True
        return False

    async def shutdown(self):
        """
        Cleanup and shutdown all data streams.
        """
        # Cancel all active streams
        for source_id in list(self.active_streams.keys()):
            await self.stop_stream(source_id)
            
        # Close aiohttp session
        if self.session:
            await self.session.close()
            self.session = None
            
        # Clear buffers
        self.data_buffer = {}