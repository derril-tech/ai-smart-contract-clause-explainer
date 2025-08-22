'use client';

import React, { useState } from 'react';
import { 
  ExclamationTriangleIcon, 
  ShieldCheckIcon, 
  InformationCircleIcon,
  ChartBarIcon,
  ChevronDownIcon,
  ChevronRightIcon
} from '@heroicons/react/24/outline';

interface RiskAssessment {
  id: string;
  title: string;
  description: string;
  impact: string;
  mitigation: string;
  risk_level: 'critical' | 'high' | 'medium' | 'low';
  category: 'financial' | 'operational' | 'technical' | 'regulatory';
  probability: number; // 0-1
  impact_score?: number; // 0-1
  calculated_risk_score: number; // 0-1
  source?: string;
}

interface RiskAssessmentProps {
  risks: RiskAssessment[];
  contractId: string;
  showFilters?: boolean;
}

export const RiskAssessment: React.FC<RiskAssessmentProps> = ({
  risks,
  contractId,
  showFilters = true
}) => {
  const [selectedRiskLevel, setSelectedRiskLevel] = useState<string>('all');
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [expandedRisks, setExpandedRisks] = useState<Set<string>>(new Set());

  // Filter risks based on selected filters
  const filteredRisks = risks.filter(risk => {
    if (selectedRiskLevel !== 'all' && risk.risk_level !== selectedRiskLevel) return false;
    if (selectedCategory !== 'all' && risk.category !== selectedCategory) return false;
    return true;
  });

  // Group risks by level
  const groupedRisks = {
    critical: filteredRisks.filter(r => r.risk_level === 'critical'),
    high: filteredRisks.filter(r => r.risk_level === 'high'),
    medium: filteredRisks.filter(r => r.risk_level === 'medium'),
    low: filteredRisks.filter(r => r.risk_level === 'low')
  };

  // Calculate overall risk metrics
  const overallRiskScore = risks.length > 0 
    ? risks.reduce((sum, risk) => sum + risk.calculated_risk_score, 0) / risks.length 
    : 0;

  const highestRisk = risks.reduce((max, risk) => 
    risk.calculated_risk_score > max ? risk.calculated_risk_score : max, 0
  );

  const getRiskIcon = (riskLevel: string) => {
    switch (riskLevel) {
      case 'critical':
        return <ExclamationTriangleIcon className="w-5 h-5 text-red-600" />;
      case 'high':
        return <ExclamationTriangleIcon className="w-5 h-5 text-orange-600" />;
      case 'medium':
        return <ExclamationTriangleIcon className="w-5 h-5 text-yellow-600" />;
      default:
        return <InformationCircleIcon className="w-5 h-5 text-blue-600" />;
    }
  };

  const getRiskColor = (riskLevel: string) => {
    switch (riskLevel) {
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
      case 'financial':
        return 'bg-red-100 text-red-800';
      case 'operational':
        return 'bg-blue-100 text-blue-800';
      case 'technical':
        return 'bg-purple-100 text-purple-800';
      case 'regulatory':
        return 'bg-green-100 text-green-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const toggleExpanded = (riskId: string) => {
    const newExpanded = new Set(expandedRisks);
    if (newExpanded.has(riskId)) {
      newExpanded.delete(riskId);
    } else {
      newExpanded.add(riskId);
    }
    setExpandedRisks(newExpanded);
  };

  const formatPercentage = (value: number) => `${Math.round(value * 100)}%`;

  const getRiskScoreColor = (score: number) => {
    if (score >= 0.8) return 'text-red-600';
    if (score >= 0.6) return 'text-orange-600';
    if (score >= 0.4) return 'text-yellow-600';
    return 'text-green-600';
  };

  const uniqueCategories = [...new Set(risks.map(r => r.category))];

  if (risks.length === 0) {
    return (
      <div className="bg-green-50 border border-green-200 rounded-lg p-6 text-center">
        <div className="flex justify-center mb-3">
          <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center">
            <ShieldCheckIcon className="w-6 h-6 text-green-600" />
          </div>
        </div>
        <h3 className="text-lg font-semibold text-green-900 mb-2">
          Low Risk Profile
        </h3>
        <p className="text-green-700">
          No significant risks were identified in this contract analysis.
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Risk Overview */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-gray-900">Risk Overview</h3>
          <div className="flex items-center space-x-4">
            <div className="text-center">
              <div className={`text-2xl font-bold ${getRiskScoreColor(overallRiskScore)}`}>
                {formatPercentage(overallRiskScore)}
              </div>
              <div className="text-sm text-gray-500">Overall Risk</div>
            </div>
            <div className="text-center">
              <div className={`text-2xl font-bold ${getRiskScoreColor(highestRisk)}`}>
                {formatPercentage(highestRisk)}
              </div>
              <div className="text-sm text-gray-500">Highest Risk</div>
            </div>
          </div>
        </div>

        {/* Risk Distribution */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {Object.entries(groupedRisks).map(([level, items]) => (
            <div
              key={level}
              className={`p-4 rounded-lg border ${getRiskColor(level)}`}
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  {getRiskIcon(level)}
                  <span className="font-semibold capitalize">{level}</span>
                </div>
                <span className="text-2xl font-bold">{items.length}</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Filters */}
      {showFilters && (
        <div className="bg-gray-50 rounded-lg p-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Risk Level
              </label>
              <select
                value={selectedRiskLevel}
                onChange={(e) => setSelectedRiskLevel(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="all">All Risk Levels</option>
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
                    {category.charAt(0).toUpperCase() + category.slice(1)}
                  </option>
                ))}
              </select>
            </div>
          </div>
        </div>
      )}

      {/* Risk List */}
      <div className="space-y-4">
        {filteredRisks.length === 0 ? (
          <div className="text-center py-8 text-gray-500">
            No risks match the selected filters.
          </div>
        ) : (
          filteredRisks
            .sort((a, b) => b.calculated_risk_score - a.calculated_risk_score)
            .map((risk) => {
              const isExpanded = expandedRisks.has(risk.id);
              
              return (
                <div
                  key={risk.id}
                  className={`border rounded-lg ${getRiskColor(risk.risk_level)} transition-all duration-200`}
                >
                  <div
                    className="p-4 cursor-pointer"
                    onClick={() => toggleExpanded(risk.id)}
                  >
                    <div className="flex items-start justify-between">
                      <div className="flex items-start space-x-3 flex-1">
                        {getRiskIcon(risk.risk_level)}
                        <div className="flex-1">
                          <div className="flex items-center space-x-2 mb-2">
                            <h3 className="font-semibold text-gray-900">
                              {risk.title}
                            </h3>
                            <span className={`px-2 py-1 text-xs font-medium rounded-full ${getCategoryBadgeColor(risk.category)}`}>
                              {risk.category}
                            </span>
                          </div>
                          
                          <div className="flex items-center space-x-4 mb-2 text-sm text-gray-600">
                            <div className="flex items-center space-x-1">
                              <ChartBarIcon className="w-4 h-4" />
                              <span>Probability: {formatPercentage(risk.probability)}</span>
                            </div>
                            <div className={`font-semibold ${getRiskScoreColor(risk.calculated_risk_score)}`}>
                              Risk Score: {formatPercentage(risk.calculated_risk_score)}
                            </div>
                          </div>
                          
                          <p className="text-gray-700 text-sm">
                            {risk.description}
                          </p>
                        </div>
                      </div>
                      
                      <div className="flex items-center">
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
                      <div className="grid md:grid-cols-2 gap-6">
                        <div>
                          <h4 className="font-semibold text-gray-900 mb-2">Potential Impact</h4>
                          <p className="text-gray-700">{risk.impact}</p>
                        </div>
                        
                        <div>
                          <h4 className="font-semibold text-gray-900 mb-2">Mitigation Strategy</h4>
                          <p className="text-gray-700">{risk.mitigation}</p>
                        </div>
                      </div>
                      
                      {risk.impact_score && (
                        <div className="mt-4 pt-4 border-t border-gray-200">
                          <div className="flex items-center space-x-6 text-sm">
                            <div>
                              <span className="text-gray-600">Impact Score: </span>
                              <span className={`font-semibold ${getRiskScoreColor(risk.impact_score)}`}>
                                {formatPercentage(risk.impact_score)}
                              </span>
                            </div>
                            <div>
                              <span className="text-gray-600">Probability: </span>
                              <span className="font-semibold">
                                {formatPercentage(risk.probability)}
                              </span>
                            </div>
                            <div>
                              <span className="text-gray-600">Combined Risk: </span>
                              <span className={`font-semibold ${getRiskScoreColor(risk.calculated_risk_score)}`}>
                                {formatPercentage(risk.calculated_risk_score)}
                              </span>
                            </div>
                          </div>
                        </div>
                      )}
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
