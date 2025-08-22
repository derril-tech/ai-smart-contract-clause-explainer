"""
WebSocket manager for real-time communication.
"""
import json
import asyncio
from typing import Dict, Set, Optional, Any
from fastapi import WebSocket, WebSocketDisconnect
import structlog

logger = structlog.get_logger()


class ConnectionManager:
    """Manages WebSocket connections and broadcasts messages."""
    
    def __init__(self):
        # Store active connections by type and ID
        self.project_connections: Dict[str, Set[WebSocket]] = {}
        self.analysis_connections: Dict[str, Set[WebSocket]] = {}
        self.user_connections: Dict[str, Set[WebSocket]] = {}
        
        # Store connection metadata
        self.connection_metadata: Dict[WebSocket, Dict[str, Any]] = {}
    
    async def connect_project(self, websocket: WebSocket, project_id: str, user_id: str):
        """Connect a WebSocket to a project channel."""
        await websocket.accept()
        
        if project_id not in self.project_connections:
            self.project_connections[project_id] = set()
        
        self.project_connections[project_id].add(websocket)
        self.connection_metadata[websocket] = {
            "type": "project",
            "project_id": project_id,
            "user_id": user_id,
            "connected_at": asyncio.get_event_loop().time()
        }
        
        logger.info("WebSocket connected to project", project_id=project_id, user_id=user_id)
    
    async def connect_analysis(self, websocket: WebSocket, analysis_id: str, user_id: str):
        """Connect a WebSocket to an analysis channel."""
        await websocket.accept()
        
        if analysis_id not in self.analysis_connections:
            self.analysis_connections[analysis_id] = set()
        
        self.analysis_connections[analysis_id].add(websocket)
        self.connection_metadata[websocket] = {
            "type": "analysis",
            "analysis_id": analysis_id,
            "user_id": user_id,
            "connected_at": asyncio.get_event_loop().time()
        }
        
        logger.info("WebSocket connected to analysis", analysis_id=analysis_id, user_id=user_id)
    
    async def connect_user(self, websocket: WebSocket, user_id: str):
        """Connect a WebSocket to a user channel."""
        await websocket.accept()
        
        if user_id not in self.user_connections:
            self.user_connections[user_id] = set()
        
        self.user_connections[user_id].add(websocket)
        self.connection_metadata[websocket] = {
            "type": "user",
            "user_id": user_id,
            "connected_at": asyncio.get_event_loop().time()
        }
        
        logger.info("WebSocket connected to user", user_id=user_id)
    
    def disconnect(self, websocket: WebSocket):
        """Disconnect a WebSocket and clean up."""
        metadata = self.connection_metadata.get(websocket, {})
        connection_type = metadata.get("type")
        
        if connection_type == "project":
            project_id = metadata.get("project_id")
            if project_id and project_id in self.project_connections:
                self.project_connections[project_id].discard(websocket)
                if not self.project_connections[project_id]:
                    del self.project_connections[project_id]
        
        elif connection_type == "analysis":
            analysis_id = metadata.get("analysis_id")
            if analysis_id and analysis_id in self.analysis_connections:
                self.analysis_connections[analysis_id].discard(websocket)
                if not self.analysis_connections[analysis_id]:
                    del self.analysis_connections[analysis_id]
        
        elif connection_type == "user":
            user_id = metadata.get("user_id")
            if user_id and user_id in self.user_connections:
                self.user_connections[user_id].discard(websocket)
                if not self.user_connections[user_id]:
                    del self.user_connections[user_id]
        
        # Clean up metadata
        if websocket in self.connection_metadata:
            del self.connection_metadata[websocket]
        
        logger.info("WebSocket disconnected", connection_type=connection_type, **metadata)
    
    async def send_personal_message(self, message: Dict[str, Any], websocket: WebSocket):
        """Send a message to a specific WebSocket connection."""
        try:
            await websocket.send_text(json.dumps(message))
        except Exception as e:
            logger.error("Failed to send personal message", error=str(e))
            self.disconnect(websocket)
    
    async def broadcast_to_project(self, project_id: str, message: Dict[str, Any]):
        """Broadcast a message to all connections in a project."""
        if project_id not in self.project_connections:
            return
        
        disconnected = set()
        for websocket in self.project_connections[project_id]:
            try:
                await websocket.send_text(json.dumps(message))
            except Exception as e:
                logger.error("Failed to broadcast to project", error=str(e), project_id=project_id)
                disconnected.add(websocket)
        
        # Clean up disconnected websockets
        for websocket in disconnected:
            self.disconnect(websocket)
        
        logger.info("Broadcasted to project", project_id=project_id, recipients=len(self.project_connections[project_id]))
    
    async def broadcast_to_analysis(self, analysis_id: str, message: Dict[str, Any]):
        """Broadcast a message to all connections in an analysis."""
        if analysis_id not in self.analysis_connections:
            return
        
        disconnected = set()
        for websocket in self.analysis_connections[analysis_id]:
            try:
                await websocket.send_text(json.dumps(message))
            except Exception as e:
                logger.error("Failed to broadcast to analysis", error=str(e), analysis_id=analysis_id)
                disconnected.add(websocket)
        
        # Clean up disconnected websockets
        for websocket in disconnected:
            self.disconnect(websocket)
        
        logger.info("Broadcasted to analysis", analysis_id=analysis_id, recipients=len(self.analysis_connections[analysis_id]))
    
    async def broadcast_to_user(self, user_id: str, message: Dict[str, Any]):
        """Broadcast a message to all connections of a user."""
        if user_id not in self.user_connections:
            return
        
        disconnected = set()
        for websocket in self.user_connections[user_id]:
            try:
                await websocket.send_text(json.dumps(message))
            except Exception as e:
                logger.error("Failed to broadcast to user", error=str(e), user_id=user_id)
                disconnected.add(websocket)
        
        # Clean up disconnected websockets
        for websocket in disconnected:
            self.disconnect(websocket)
        
        logger.info("Broadcasted to user", user_id=user_id, recipients=len(self.user_connections[user_id]))
    
    async def broadcast_to_all(self, message: Dict[str, Any]):
        """Broadcast a message to all connected WebSockets."""
        all_websockets = set()
        
        # Collect all websockets
        for connections in self.project_connections.values():
            all_websockets.update(connections)
        for connections in self.analysis_connections.values():
            all_websockets.update(connections)
        for connections in self.user_connections.values():
            all_websockets.update(connections)
        
        disconnected = set()
        for websocket in all_websockets:
            try:
                await websocket.send_text(json.dumps(message))
            except Exception as e:
                logger.error("Failed to broadcast to all", error=str(e))
                disconnected.add(websocket)
        
        # Clean up disconnected websockets
        for websocket in disconnected:
            self.disconnect(websocket)
        
        logger.info("Broadcasted to all", recipients=len(all_websockets))
    
    def get_connection_stats(self) -> Dict[str, Any]:
        """Get connection statistics."""
        return {
            "project_connections": len(self.project_connections),
            "analysis_connections": len(self.analysis_connections),
            "user_connections": len(self.user_connections),
            "total_connections": len(self.connection_metadata),
            "projects": list(self.project_connections.keys()),
            "analyses": list(self.analysis_connections.keys()),
            "users": list(self.user_connections.keys())
        }


class WebSocketManager:
    """High-level WebSocket manager with message handling."""
    
    def __init__(self):
        self.connection_manager = ConnectionManager()
    
    async def handle_project_connection(self, websocket: WebSocket, project_id: str, user_id: str):
        """Handle project WebSocket connection."""
        await self.connection_manager.connect_project(websocket, project_id, user_id)
        
        try:
            while True:
                # Wait for messages from the client
                data = await websocket.receive_text()
                message = json.loads(data)
                
                # Handle different message types
                await self.handle_project_message(websocket, project_id, user_id, message)
                
        except WebSocketDisconnect:
            logger.info("Project WebSocket disconnected", project_id=project_id, user_id=user_id)
        except Exception as e:
            logger.error("Project WebSocket error", error=str(e), project_id=project_id, user_id=user_id)
        finally:
            self.connection_manager.disconnect(websocket)
    
    async def handle_analysis_connection(self, websocket: WebSocket, analysis_id: str, user_id: str):
        """Handle analysis WebSocket connection."""
        await self.connection_manager.connect_analysis(websocket, analysis_id, user_id)
        
        try:
            while True:
                # Wait for messages from the client
                data = await websocket.receive_text()
                message = json.loads(data)
                
                # Handle different message types
                await self.handle_analysis_message(websocket, analysis_id, user_id, message)
                
        except WebSocketDisconnect:
            logger.info("Analysis WebSocket disconnected", analysis_id=analysis_id, user_id=user_id)
        except Exception as e:
            logger.error("Analysis WebSocket error", error=str(e), analysis_id=analysis_id, user_id=user_id)
        finally:
            self.connection_manager.disconnect(websocket)
    
    async def handle_project_message(self, websocket: WebSocket, project_id: str, user_id: str, message: Dict[str, Any]):
        """Handle incoming project messages."""
        message_type = message.get("type")
        
        if message_type == "ping":
            # Respond to ping
            await self.connection_manager.send_personal_message({
                "type": "pong",
                "timestamp": asyncio.get_event_loop().time()
            }, websocket)
        
        elif message_type == "subscribe":
            # Subscribe to specific events
            events = message.get("events", [])
            await self.connection_manager.send_personal_message({
                "type": "subscribed",
                "events": events,
                "project_id": project_id
            }, websocket)
        
        elif message_type == "unsubscribe":
            # Unsubscribe from events
            events = message.get("events", [])
            await self.connection_manager.send_personal_message({
                "type": "unsubscribed",
                "events": events,
                "project_id": project_id
            }, websocket)
        
        else:
            # Unknown message type
            await self.connection_manager.send_personal_message({
                "type": "error",
                "message": f"Unknown message type: {message_type}"
            }, websocket)
    
    async def handle_analysis_message(self, websocket: WebSocket, analysis_id: str, user_id: str, message: Dict[str, Any]):
        """Handle incoming analysis messages."""
        message_type = message.get("type")
        
        if message_type == "ping":
            # Respond to ping
            await self.connection_manager.send_personal_message({
                "type": "pong",
                "timestamp": asyncio.get_event_loop().time()
            }, websocket)
        
        elif message_type == "subscribe":
            # Subscribe to specific events
            events = message.get("events", [])
            await self.connection_manager.send_personal_message({
                "type": "subscribed",
                "events": events,
                "analysis_id": analysis_id
            }, websocket)
        
        elif message_type == "unsubscribe":
            # Unsubscribe from events
            events = message.get("events", [])
            await self.connection_manager.send_personal_message({
                "type": "unsubscribed",
                "events": events,
                "analysis_id": analysis_id
            }, websocket)
        
        else:
            # Unknown message type
            await self.connection_manager.send_personal_message({
                "type": "error",
                "message": f"Unknown message type: {message_type}"
            }, websocket)
    
    async def send_analysis_progress(self, analysis_id: str, progress: Dict[str, Any]):
        """Send analysis progress update."""
        message = {
            "type": "analysis_progress",
            "analysis_id": analysis_id,
            "progress": progress,
            "timestamp": asyncio.get_event_loop().time()
        }
        await self.connection_manager.broadcast_to_analysis(analysis_id, message)
    
    async def send_analysis_complete(self, analysis_id: str, results: Dict[str, Any]):
        """Send analysis completion notification."""
        message = {
            "type": "analysis_complete",
            "analysis_id": analysis_id,
            "results": results,
            "timestamp": asyncio.get_event_loop().time()
        }
        await self.connection_manager.broadcast_to_analysis(analysis_id, message)
    
    async def send_project_update(self, project_id: str, update: Dict[str, Any]):
        """Send project update notification."""
        message = {
            "type": "project_update",
            "project_id": project_id,
            "update": update,
            "timestamp": asyncio.get_event_loop().time()
        }
        await self.connection_manager.broadcast_to_project(project_id, message)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get WebSocket manager statistics."""
        return self.connection_manager.get_connection_stats()


# Global WebSocket manager instance
websocket_manager = WebSocketManager()
