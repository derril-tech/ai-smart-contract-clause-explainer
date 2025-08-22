'use client';

import React, { useState, useEffect } from 'react';
import { Tab } from '@headlessui/react';
import { 
  DocumentTextIcon, 
  ShieldExclamationIcon, 
  ChartBarIcon, 
  CogIcon,
  DocumentArrowDownIcon,
  ShareIcon
} from '@heroicons/react/24/outline';
import { AnalysisProgress } from './AnalysisProgress';
import { SecurityFindings } from './SecurityFindings';
import { RiskAssessment } from './RiskAssessment';

interface AnalysisResult {
  contract: {
    id: string;
    address: string;
    name: string;
    chain_id: number;
    analysis_status: string;
    risk_score: number;
    analysis_summary: string;
  };
  findings: any[];
  risks: any[];
  summary: {
    total_findings: number;
    total_risks: number;
    risk_score: number;
    analysis_duration: number;
    status: string;
  };
}

interface AnalysisDashboardProps {
  contractId: string;
  initialData?: AnalysisResult;
}

function classNames(...classes: string[]) {
  return classes.filter(Boolean).join(' ');
}

export const AnalysisDashboard: React.FC<AnalysisDashboardProps> = ({
  contractId,
  initialData
}) => {
  const [analysisData, setAnalysisData] = useState<AnalysisResult | null>(initialData || null);
  const [isLoading, setIsLoading] = useState(!initialData);
  const [selectedTab, setSelectedTab] = useState(0);

  useEffect(() => {
    if (!initialData) {
      fetchAnalysisData();
    }
  }, [contractId, initialData]);

  const fetchAnalysisData = async () => {
    try {
      setIsLoading(true);
      const response = await fetch(`/api/v1/contracts/${contractId}/results`);
      if (response.ok) {
        const data = await response.json();
        setAnalysisData(data);
      }
    } catch (error) {
      console.error('Failed to fetch analysis data:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleAnalysisComplete = (results: any) => {
    // Refresh the analysis data when analysis completes
    fetchAnalysisData();
  };

  const downloadReport = async () => {
    try {
      const response = await fetch(`/api/v1/reports/generate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          contract_id: contractId,
          report_type: 'security',
          format: 'pdf'
        })
      });
      
      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `security-report-${contractId}.pdf`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
      }
    } catch (error) {
      console.error('Failed to download report:', error);
    }
  };

  const shareResults = async () => {
    try {
      await navigator.share({
        title: `Smart Contract Analysis - ${analysisData?.contract.name || 'Contract'}`,
        text: `Security analysis results for contract ${analysisData?.contract.address}`,
        url: window.location.href
      });
    } catch (error) {
      // Fallback to copying URL to clipboard
      navigator.clipboard.writeText(window.location.href);
      // Show toast notification here
    }
  };

  const getRiskScoreColor = (score: number) => {
    if (score >= 0.8) return 'text-red-600 bg-red-50 border-red-200';
    if (score >= 0.6) return 'text-orange-600 bg-orange-50 border-orange-200';
    if (score >= 0.4) return 'text-yellow-600 bg-yellow-50 border-yellow-200';
    return 'text-green-600 bg-green-50 border-green-200';
  };

  const tabs = [
    { name: 'Overview', icon: DocumentTextIcon },
    { name: 'Security Findings', icon: ShieldExclamationIcon },
    { name: 'Risk Assessment', icon: ChartBarIcon },
    { name: 'Gas Optimization', icon: CogIcon },
  ];

  // Show progress component if analysis is not completed
  if (!analysisData || analysisData.contract.analysis_status !== 'completed') {
    return (
      <div className="max-w-7xl mx-auto px-4 py-8">
        <AnalysisProgress 
          contractId={contractId} 
          onComplete={handleAnalysisComplete}
        />
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      {/* Header */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 mb-8">
        <div className="px-6 py-4 border-b border-gray-200">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">
                {analysisData.contract.name}
              </h1>
              <p className="text-sm text-gray-600 font-mono">
                {analysisData.contract.address}
              </p>
              <p className="text-sm text-gray-500">
                Chain ID: {analysisData.contract.chain_id}
              </p>
            </div>
            
            <div className="flex items-center space-x-4">
              <div className={`px-4 py-2 rounded-lg border ${getRiskScoreColor(analysisData.contract.risk_score)}`}>
                <div className="text-center">
                  <div className="text-2xl font-bold">
                    {Math.round(analysisData.contract.risk_score * 100)}%
                  </div>
                  <div className="text-sm">Risk Score</div>
                </div>
              </div>
              
              <div className="flex space-x-2">
                <button
                  onClick={downloadReport}
                  className="btn-secondary flex items-center space-x-2"
                >
                  <DocumentArrowDownIcon className="w-4 h-4" />
                  <span>Download Report</span>
                </button>
                
                <button
                  onClick={shareResults}
                  className="btn-secondary flex items-center space-x-2"
                >
                  <ShareIcon className="w-4 h-4" />
                  <span>Share</span>
                </button>
              </div>
            </div>
          </div>
        </div>
        
        {/* Summary Stats */}
        <div className="px-6 py-4">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
            <div className="text-center">
              <div className="text-2xl font-bold text-gray-900">
                {analysisData.summary.total_findings}
              </div>
              <div className="text-sm text-gray-600">Security Findings</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-gray-900">
                {analysisData.summary.total_risks}
              </div>
              <div className="text-sm text-gray-600">Risk Assessments</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-gray-900">
                {Math.round(analysisData.summary.analysis_duration / 60)}m
              </div>
              <div className="text-sm text-gray-600">Analysis Duration</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-green-600">
                ✓
              </div>
              <div className="text-sm text-gray-600">Analysis Complete</div>
            </div>
          </div>
        </div>
      </div>

      {/* Analysis Summary */}
      {analysisData.contract.analysis_summary && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-6 mb-8">
          <h3 className="text-lg font-semibold text-blue-900 mb-2">
            Analysis Summary
          </h3>
          <p className="text-blue-800">
            {analysisData.contract.analysis_summary}
          </p>
        </div>
      )}

      {/* Tabs */}
      <Tab.Group selectedIndex={selectedTab} onChange={setSelectedTab}>
        <Tab.List className="flex space-x-1 rounded-xl bg-blue-900/20 p-1 mb-8">
          {tabs.map((tab) => (
            <Tab
              key={tab.name}
              className={({ selected }) =>
                classNames(
                  'w-full rounded-lg py-2.5 text-sm font-medium leading-5',
                  'ring-white ring-opacity-60 ring-offset-2 ring-offset-blue-400 focus:outline-none focus:ring-2',
                  selected
                    ? 'bg-white shadow text-blue-700'
                    : 'text-blue-100 hover:bg-white/[0.12] hover:text-white'
                )
              }
            >
              <div className="flex items-center justify-center space-x-2">
                <tab.icon className="w-4 h-4" />
                <span>{tab.name}</span>
              </div>
            </Tab>
          ))}
        </Tab.List>
        
        <Tab.Panels>
          {/* Overview Tab */}
          <Tab.Panel>
            <div className="grid md:grid-cols-2 gap-8">
              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">
                  Security Overview
                </h3>
                <SecurityFindings 
                  findings={analysisData.findings} 
                  contractId={contractId}
                  showFilters={false}
                />
              </div>
              
              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">
                  Risk Overview
                </h3>
                <RiskAssessment 
                  risks={analysisData.risks} 
                  contractId={contractId}
                  showFilters={false}
                />
              </div>
            </div>
          </Tab.Panel>
          
          {/* Security Findings Tab */}
          <Tab.Panel>
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <SecurityFindings 
                findings={analysisData.findings} 
                contractId={contractId}
                showFilters={true}
              />
            </div>
          </Tab.Panel>
          
          {/* Risk Assessment Tab */}
          <Tab.Panel>
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <RiskAssessment 
                risks={analysisData.risks} 
                contractId={contractId}
                showFilters={true}
              />
            </div>
          </Tab.Panel>
          
          {/* Gas Optimization Tab */}
          <Tab.Panel>
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <div className="text-center py-12">
                <CogIcon className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-900 mb-2">
                  Gas Optimization Analysis
                </h3>
                <p className="text-gray-600">
                  Gas optimization recommendations will be displayed here.
                </p>
              </div>
            </div>
          </Tab.Panel>
        </Tab.Panels>
      </Tab.Group>
    </div>
  );
};
