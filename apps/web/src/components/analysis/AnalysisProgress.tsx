'use client';

import React, { useState, useEffect } from 'react';
import { CheckCircleIcon, ExclamationTriangleIcon, ClockIcon } from '@heroicons/react/24/outline';

interface AnalysisProgressProps {
  contractId: string;
  onComplete?: (results: any) => void;
}

interface ProgressData {
  status: 'pending' | 'analyzing' | 'completed' | 'failed';
  progress: number;
  message: string;
  estimated_remaining?: number;
  risk_score?: number;
  summary?: string;
}

export const AnalysisProgress: React.FC<AnalysisProgressProps> = ({
  contractId,
  onComplete
}) => {
  const [progressData, setProgressData] = useState<ProgressData>({
    status: 'pending',
    progress: 0,
    message: 'Initializing analysis...'
  });
  const [websocket, setWebsocket] = useState<WebSocket | null>(null);

  useEffect(() => {
    // Connect to WebSocket for real-time updates
    const ws = new WebSocket(`ws://localhost:8000/ws/analysis/${contractId}`);
    
    ws.onopen = () => {
      console.log('WebSocket connected for analysis updates');
      setWebsocket(ws);
    };
    
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      
      if (data.type === 'analysis_progress') {
        setProgressData(prev => ({
          ...prev,
          ...data.progress
        }));
      } else if (data.type === 'analysis_complete') {
        setProgressData({
          status: 'completed',
          progress: 100,
          message: 'Analysis completed successfully',
          risk_score: data.results.risk_score,
          summary: data.results.summary
        });
        
        if (onComplete) {
          onComplete(data.results);
        }
      }
    };
    
    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
      setProgressData(prev => ({
        ...prev,
        status: 'failed',
        message: 'Connection error occurred'
      }));
    };
    
    ws.onclose = () => {
      console.log('WebSocket connection closed');
      setWebsocket(null);
    };
    
    // Cleanup on unmount
    return () => {
      if (ws.readyState === WebSocket.OPEN) {
        ws.close();
      }
    };
  }, [contractId, onComplete]);

  const getStatusIcon = () => {
    switch (progressData.status) {
      case 'completed':
        return <CheckCircleIcon className="w-6 h-6 text-green-500" />;
      case 'failed':
        return <ExclamationTriangleIcon className="w-6 h-6 text-red-500" />;
      default:
        return <ClockIcon className="w-6 h-6 text-blue-500 animate-spin" />;
    }
  };

  const getStatusColor = () => {
    switch (progressData.status) {
      case 'completed':
        return 'bg-green-500';
      case 'failed':
        return 'bg-red-500';
      case 'analyzing':
        return 'bg-blue-500';
      default:
        return 'bg-gray-300';
    }
  };

  const getRiskScoreColor = (score: number) => {
    if (score >= 0.8) return 'text-red-600 bg-red-50';
    if (score >= 0.6) return 'text-orange-600 bg-orange-50';
    if (score >= 0.4) return 'text-yellow-600 bg-yellow-50';
    return 'text-green-600 bg-green-50';
  };

  const formatTime = (seconds: number) => {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = Math.floor(seconds % 60);
    return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-3">
          {getStatusIcon()}
          <div>
            <h3 className="text-lg font-semibold text-gray-900">
              Smart Contract Analysis
            </h3>
            <p className="text-sm text-gray-600">{progressData.message}</p>
          </div>
        </div>
        
        {progressData.status === 'analyzing' && progressData.estimated_remaining && (
          <div className="text-right">
            <p className="text-sm text-gray-500">Estimated time remaining</p>
            <p className="text-lg font-mono text-gray-900">
              {formatTime(progressData.estimated_remaining)}
            </p>
          </div>
        )}
      </div>

      {/* Progress Bar */}
      <div className="mb-6">
        <div className="flex justify-between items-center mb-2">
          <span className="text-sm font-medium text-gray-700">Progress</span>
          <span className="text-sm text-gray-600">{progressData.progress}%</span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2">
          <div
            className={`h-2 rounded-full transition-all duration-300 ${getStatusColor()}`}
            style={{ width: `${progressData.progress}%` }}
          />
        </div>
      </div>

      {/* Analysis Stages */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        {[
          { name: 'Static Analysis', stage: 25 },
          { name: 'AI Security Review', stage: 50 },
          { name: 'Risk Assessment', stage: 75 },
          { name: 'Report Generation', stage: 100 }
        ].map((item) => (
          <div
            key={item.name}
            className={`p-3 rounded-lg border ${
              progressData.progress >= item.stage
                ? 'border-green-200 bg-green-50'
                : progressData.progress >= item.stage - 25
                ? 'border-blue-200 bg-blue-50'
                : 'border-gray-200 bg-gray-50'
            }`}
          >
            <div className="flex items-center justify-between">
              <span className="text-sm font-medium text-gray-900">
                {item.name}
              </span>
              {progressData.progress >= item.stage && (
                <CheckCircleIcon className="w-4 h-4 text-green-500" />
              )}
            </div>
          </div>
        ))}
      </div>

      {/* Results Summary (shown when completed) */}
      {progressData.status === 'completed' && progressData.risk_score !== undefined && (
        <div className="border-t border-gray-200 pt-6">
          <div className="flex items-center justify-between mb-4">
            <h4 className="text-lg font-semibold text-gray-900">Analysis Complete</h4>
            <div className={`px-3 py-1 rounded-full text-sm font-medium ${getRiskScoreColor(progressData.risk_score)}`}>
              Risk Score: {(progressData.risk_score * 100).toFixed(0)}%
            </div>
          </div>
          
          {progressData.summary && (
            <p className="text-gray-700 mb-4">{progressData.summary}</p>
          )}
          
          <div className="flex space-x-3">
            <button className="btn-primary">
              View Detailed Results
            </button>
            <button className="btn-secondary">
              Download Report
            </button>
          </div>
        </div>
      )}

      {/* Error State */}
      {progressData.status === 'failed' && (
        <div className="border-t border-gray-200 pt-6">
          <div className="flex items-center space-x-3 mb-4">
            <ExclamationTriangleIcon className="w-6 h-6 text-red-500" />
            <h4 className="text-lg font-semibold text-red-900">Analysis Failed</h4>
          </div>
          <p className="text-red-700 mb-4">
            The analysis could not be completed. This might be due to invalid contract code,
            network issues, or service limitations.
          </p>
          <button className="btn-secondary">
            Retry Analysis
          </button>
        </div>
      )}
    </div>
  );
};
