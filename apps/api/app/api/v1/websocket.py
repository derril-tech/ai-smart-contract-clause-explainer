"""
WebSocket endpoints for ClauseLens AI API.
Handles real-time updates for analysis progress and streaming.
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException
from typing import Dict, List
import json
import structlog

from app.core.security import get_current_user_ws
from app.services.websocket import WebSocketManager

router = APIRouter()
logger = structlog.get_logger()

# WebSocket connection manager
ws_manager = WebSocketManager()


@router.websocket("/projects/{project_id}")
async def project_websocket(
    websocket: WebSocket,
    project_id: str
):
    """
    WebSocket endpoint for project-specific real-time updates.
    
    Args:
        websocket: WebSocket connection
        project_id: Project identifier for updates
    """
    await websocket.accept()
    
    try:
        # Add connection to manager
        await ws_manager.connect(websocket, project_id)
        logger.info("WebSocket connected", project_id=project_id)
        
        # Send initial connection confirmation
        await websocket.send_text(json.dumps({
            "type": "connection_established",
            "project_id": project_id,
            "message": "Connected to project updates"
        }))
        
        # Keep connection alive and handle messages
        while True:
            try:
                # Wait for messages from client
                data = await websocket.receive_text()
                message = json.loads(data)
                
                # Handle client messages
                await handle_client_message(websocket, project_id, message)
                
            except WebSocketDisconnect:
                break
            except json.JSONDecodeError:
                await websocket.send_text(json.dumps({
                    "type": "error",
                    "message": "Invalid JSON format"
                }))
            except Exception as e:
                logger.error("WebSocket error", error=str(e), project_id=project_id)
                await websocket.send_text(json.dumps({
                    "type": "error",
                    "message": "Internal server error"
                }))
                
    except WebSocketDisconnect:
        logger.info("WebSocket disconnected", project_id=project_id)
    except Exception as e:
        logger.error("WebSocket connection error", error=str(e), project_id=project_id)
    finally:
        # Remove connection from manager
        await ws_manager.disconnect(websocket, project_id)


@router.websocket("/analysis/{analysis_id}")
async def analysis_websocket(
    websocket: WebSocket,
    analysis_id: str
):
    """
    WebSocket endpoint for analysis-specific real-time updates.
    
    Args:
        websocket: WebSocket connection
        analysis_id: Analysis identifier for updates
    """
    await websocket.accept()
    
    try:
        # Add connection to manager
        await ws_manager.connect(websocket, f"analysis_{analysis_id}")
        logger.info("Analysis WebSocket connected", analysis_id=analysis_id)
        
        # Send initial connection confirmation
        await websocket.send_text(json.dumps({
            "type": "connection_established",
            "analysis_id": analysis_id,
            "message": "Connected to analysis updates"
        }))
        
        # Keep connection alive and handle messages
        while True:
            try:
                # Wait for messages from client
                data = await websocket.receive_text()
                message = json.loads(data)
                
                # Handle client messages
                await handle_analysis_message(websocket, analysis_id, message)
                
            except WebSocketDisconnect:
                break
            except json.JSONDecodeError:
                await websocket.send_text(json.dumps({
                    "type": "error",
                    "message": "Invalid JSON format"
                }))
            except Exception as e:
                logger.error("Analysis WebSocket error", error=str(e), analysis_id=analysis_id)
                await websocket.send_text(json.dumps({
                    "type": "error",
                    "message": "Internal server error"
                }))
                
    except WebSocketDisconnect:
        logger.info("Analysis WebSocket disconnected", analysis_id=analysis_id)
    except Exception as e:
        logger.error("Analysis WebSocket connection error", error=str(e), analysis_id=analysis_id)
    finally:
        # Remove connection from manager
        await ws_manager.disconnect(websocket, f"analysis_{analysis_id}")


async def handle_client_message(websocket: WebSocket, project_id: str, message: Dict):
    """
    Handle messages from project WebSocket clients.
    
    Args:
        websocket: WebSocket connection
        project_id: Project identifier
        message: Client message
    """
    message_type = message.get("type")
    
    if message_type == "ping":
        # Respond to ping with pong
        await websocket.send_text(json.dumps({
            "type": "pong",
            "timestamp": message.get("timestamp")
        }))
    elif message_type == "subscribe":
        # Subscribe to specific update types
        update_types = message.get("update_types", [])
        await ws_manager.subscribe_to_updates(websocket, project_id, update_types)
        await websocket.send_text(json.dumps({
            "type": "subscribed",
            "update_types": update_types
        }))
    elif message_type == "unsubscribe":
        # Unsubscribe from specific update types
        update_types = message.get("update_types", [])
        await ws_manager.unsubscribe_from_updates(websocket, project_id, update_types)
        await websocket.send_text(json.dumps({
            "type": "unsubscribed",
            "update_types": update_types
        }))
    else:
        # Unknown message type
        await websocket.send_text(json.dumps({
            "type": "error",
            "message": f"Unknown message type: {message_type}"
        }))


async def handle_analysis_message(websocket: WebSocket, analysis_id: str, message: Dict):
    """
    Handle messages from analysis WebSocket clients.
    
    Args:
        websocket: WebSocket connection
        analysis_id: Analysis identifier
        message: Client message
    """
    message_type = message.get("type")
    
    if message_type == "ping":
        # Respond to ping with pong
        await websocket.send_text(json.dumps({
            "type": "pong",
            "timestamp": message.get("timestamp")
        }))
    elif message_type == "get_status":
        # Get current analysis status
        status = await ws_manager.get_analysis_status(analysis_id)
        await websocket.send_text(json.dumps({
            "type": "analysis_status",
            "analysis_id": analysis_id,
            "status": status
        }))
    else:
        # Unknown message type
        await websocket.send_text(json.dumps({
            "type": "error",
            "message": f"Unknown message type: {message_type}"
        }))


# Broadcast functions for sending updates to connected clients
async def broadcast_project_update(project_id: str, update_type: str, data: Dict):
    """
    Broadcast project update to all connected clients.
    
    Args:
        project_id: Project identifier
        update_type: Type of update
        data: Update data
    """
    message = {
        "type": update_type,
        "project_id": project_id,
        "data": data,
        "timestamp": structlog.get_logger()._context.get("timestamp")
    }
    
    await ws_manager.broadcast_to_project(project_id, json.dumps(message))


async def broadcast_analysis_update(analysis_id: str, update_type: str, data: Dict):
    """
    Broadcast analysis update to all connected clients.
    
    Args:
        analysis_id: Analysis identifier
        update_type: Type of update
        data: Update data
    """
    message = {
        "type": update_type,
        "analysis_id": analysis_id,
        "data": data,
        "timestamp": structlog.get_logger()._context.get("timestamp")
    }
    
    await ws_manager.broadcast_to_analysis(analysis_id, json.dumps(message))


async def broadcast_explanation_stream(analysis_id: str, symbol_id: str, explanation: str, completed: bool = False):
    """
    Broadcast explanation streaming updates.
    
    Args:
        analysis_id: Analysis identifier
        symbol_id: Symbol identifier
        explanation: Explanation text
        completed: Whether explanation is complete
    """
    message = {
        "type": "explanation_stream",
        "analysis_id": analysis_id,
        "symbol_id": symbol_id,
        "explanation": explanation,
        "completed": completed,
        "timestamp": structlog.get_logger()._context.get("timestamp")
    }
    
    await ws_manager.broadcast_to_analysis(analysis_id, json.dumps(message))
