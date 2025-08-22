'use client';

import React, { useState } from 'react';
import { 
  ExclamationTriangleIcon, 
  ShieldExclamationIcon, 
  InformationCircleIcon,
  ChevronDownIcon,
  ChevronRightIcon
} from '@heroicons/react/24/outline';

interface SecurityFinding {
  id: string;
  title: string;
  description: string;
  recommendation: string;
  severity: 'critical' | 'high' | 'medium' | 'low';
  category: 'access-control' | 'arithmetic' | 'reentrancy' | 'gas' | 'other';
  line_number?: number;
  function_name?: string;
  file_name?: string;
  tool: string;
  confidence?: number;
  source?: string;
}

interface SecurityFindingsProps {
  findings: SecurityFinding[];
  contractId: string;
  showFilters?: boolean;
}

export const SecurityFindings: React.FC<SecurityFindingsProps> = ({
  findings,
  contractId,
  showFilters = true
}) => {
  const [selectedSeverity, setSelectedSeverity] = useState<string>('all');
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [selectedTool, setSelectedTool] = useState<string>('all');
  const [expandedFindings, setExpandedFindings] = useState<Set<string>>(new Set());

  // Filter findings based on selected filters
  const filteredFindings = findings.filter(finding => {
    if (selectedSeverity !== 'all' && finding.severity !== selectedSeverity) return false;
    if (selectedCategory !== 'all' && finding.category !== selectedCategory) return false;
    if (selectedTool !== 'all' && finding.tool !== selectedTool) return false;
    return true;
  });

  // Group findings by severity
  const groupedFindings = {
    critical: filteredFindings.filter(f => f.severity === 'critical'),
    high: filteredFindings.filter(f => f.severity === 'high'),
    medium: filteredFindings.filter(f => f.severity === 'medium'),
    low: filteredFindings.filter(f => f.severity === 'low')
  };

  const getSeverityIcon = (severity: string) => {
    switch (severity) {
      case 'critical':
        return <ExclamationTriangleIcon className="w-5 h-5 text-red-600" />;
      case 'high':
        return <ShieldExclamationIcon className="w-5 h-5 text-orange-600" />;
      case 'medium':
        return <ExclamationTriangleIcon className="w-5 h-5 text-yellow-600" />;
      default:
        return <InformationCircleIcon className="w-5 h-5 text-blue-600" />;
    }
  };

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical':
        return 'bg-red-50 border-red-200 text-red-800';
      case 'high':
        return 'bg-orange-50 border-orange-200 text-orange-800';
      case 'medium':
        return 'bg-yellow-50 border-yellow-200 text-yellow-800';
      default:
        return 'bg-blue-50 border-blue-200 text-blue-800';
    }
  };

  const getCategoryBadgeColor = (category: string) => {
    switch (category) {
      case 'access-control':
        return 'bg-purple-100 text-purple-800';
      case 'reentrancy':
        return 'bg-red-100 text-red-800';
      case 'arithmetic':
        return 'bg-orange-100 text-orange-800';
      case 'gas':
        return 'bg-green-100 text-green-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getToolBadgeColor = (tool: string) => {
    switch (tool) {
      case 'slither':
        return 'bg-indigo-100 text-indigo-800';
      case 'mythril':
        return 'bg-cyan-100 text-cyan-800';
      case 'semgrep':
        return 'bg-teal-100 text-teal-800';
      case 'openai':
      case 'gpt-4':
        return 'bg-emerald-100 text-emerald-800';
      case 'anthropic':
      case 'claude':
        return 'bg-violet-100 text-violet-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const toggleExpanded = (findingId: string) => {
    const newExpanded = new Set(expandedFindings);
    if (newExpanded.has(findingId)) {
      newExpanded.delete(findingId);
    } else {
      newExpanded.add(findingId);
    }
    setExpandedFindings(newExpanded);
  };

  const uniqueTools = [...new Set(findings.map(f => f.tool))];
  const uniqueCategories = [...new Set(findings.map(f => f.category))];

  if (findings.length === 0) {
    return (
      <div className="bg-green-50 border border-green-200 rounded-lg p-6 text-center">
        <div className="flex justify-center mb-3">
          <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center">
            <ShieldExclamationIcon className="w-6 h-6 text-green-600" />
          </div>
        </div>
        <h3 className="text-lg font-semibold text-green-900 mb-2">
          No Security Issues Found
        </h3>
        <p className="text-green-700">
          The analysis did not identify any security vulnerabilities in this contract.
          However, this doesn't guarantee the contract is completely secure.
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Summary Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {Object.entries(groupedFindings).map(([severity, items]) => (
          <div
            key={severity}
            className={`p-4 rounded-lg border ${getSeverityColor(severity)}`}
          >
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2">
                {getSeverityIcon(severity)}
                <span className="font-semibold capitalize">{severity}</span>
              </div>
              <span className="text-2xl font-bold">{items.length}</span>
            </div>
          </div>
        ))}
      </div>

      {/* Filters */}
      {showFilters && (
        <div className="bg-gray-50 rounded-lg p-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Severity
              </label>
              <select
                value={selectedSeverity}
                onChange={(e) => setSelectedSeverity(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="all">All Severities</option>
                <option value="critical">Critical</option>
                <option value="high">High</option>
                <option value="medium">Medium</option>
                <option value="low">Low</option>
              </select>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Category
              </label>
              <select
                value={selectedCategory}
                onChange={(e) => setSelectedCategory(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="all">All Categories</option>
                {uniqueCategories.map(category => (
                  <option key={category} value={category}>
                    {category.charAt(0).toUpperCase() + category.slice(1).replace('-', ' ')}
                  </option>
                ))}
              </select>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Analysis Tool
              </label>
              <select
                value={selectedTool}
                onChange={(e) => setSelectedTool(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="all">All Tools</option>
                {uniqueTools.map(tool => (
                  <option key={tool} value={tool}>
                    {tool.charAt(0).toUpperCase() + tool.slice(1)}
                  </option>
                ))}
              </select>
            </div>
          </div>
        </div>
      )}

      {/* Findings List */}
      <div className="space-y-4">
        {filteredFindings.length === 0 ? (
          <div className="text-center py-8 text-gray-500">
            No findings match the selected filters.
          </div>
        ) : (
          filteredFindings.map((finding) => {
            const isExpanded = expandedFindings.has(finding.id);
            
            return (
              <div
                key={finding.id}
                className={`border rounded-lg ${getSeverityColor(finding.severity)} transition-all duration-200`}
              >
                <div
                  className="p-4 cursor-pointer"
                  onClick={() => toggleExpanded(finding.id)}
                >
                  <div className="flex items-start justify-between">
                    <div className="flex items-start space-x-3 flex-1">
                      {getSeverityIcon(finding.severity)}
                      <div className="flex-1">
                        <div className="flex items-center space-x-2 mb-2">
                          <h3 className="font-semibold text-gray-900">
                            {finding.title}
                          </h3>
                          <span className={`px-2 py-1 text-xs font-medium rounded-full ${getCategoryBadgeColor(finding.category)}`}>
                            {finding.category.replace('-', ' ')}
                          </span>
                          <span className={`px-2 py-1 text-xs font-medium rounded-full ${getToolBadgeColor(finding.tool)}`}>
                            {finding.tool}
                          </span>
                        </div>
                        
                        {(finding.line_number || finding.function_name) && (
                          <div className="text-sm text-gray-600 mb-2">
                            {finding.function_name && (
                              <span>Function: <code className="bg-gray-200 px-1 rounded">{finding.function_name}</code></span>
                            )}
                            {finding.line_number && (
                              <span className="ml-3">Line: {finding.line_number}</span>
                            )}
                          </div>
                        )}
                        
                        <p className="text-gray-700 text-sm">
                          {finding.description}
                        </p>
                      </div>
                    </div>
                    
                    <div className="flex items-center space-x-2">
                      {finding.confidence && (
                        <span className="text-xs text-gray-500">
                          {Math.round(finding.confidence * 100)}% confidence
                        </span>
                      )}
                      {isExpanded ? (
                        <ChevronDownIcon className="w-5 h-5 text-gray-400" />
                      ) : (
                        <ChevronRightIcon className="w-5 h-5 text-gray-400" />
                      )}
                    </div>
                  </div>
                </div>
                
                {isExpanded && (
                  <div className="border-t border-gray-200 p-4 bg-white bg-opacity-50">
                    <div className="space-y-4">
                      <div>
                        <h4 className="font-semibold text-gray-900 mb-2">Recommendation</h4>
                        <p className="text-gray-700">{finding.recommendation}</p>
                      </div>
                      
                      {finding.file_name && (
                        <div>
                          <h4 className="font-semibold text-gray-900 mb-2">File Location</h4>
                          <code className="bg-gray-100 px-2 py-1 rounded text-sm">
                            {finding.file_name}
                          </code>
                        </div>
                      )}
                    </div>
                  </div>
                )}
              </div>
            );
          })
        )}
      </div>
    </div>
  );
};
