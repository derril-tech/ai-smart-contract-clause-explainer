'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { 
  MagnifyingGlassIcon, 
  DocumentArrowUpIcon, 
  SparklesIcon,
  CpuChipIcon,
  ShieldCheckIcon,
  ChartBarIcon
} from '@heroicons/react/24/outline';

interface AnalysisOptions {
  analysisTypes: string[];
  useAI: boolean;
  useStaticAnalysis: boolean;
}

export const EnhancedContractAnalyzer: React.FC = () => {
  const router = useRouter();
  const [contractAddress, setContractAddress] = useState('');
  const [chainId, setChainId] = useState(1);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [showUpload, setShowUpload] = useState(false);
  const [analysisOptions, setAnalysisOptions] = useState<AnalysisOptions>({
    analysisTypes: ['security', 'risk', 'gas', 'compliance'],
    useAI: true,
    useStaticAnalysis: true
  });

  const handleAnalyze = async () => {
    if (!contractAddress) return;

    setIsAnalyzing(true);
    
    try {
      const response = await fetch('/api/v1/contracts/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}` // Add auth token
        },
        body: JSON.stringify({
          contract_address: contractAddress,
          chain_id: chainId,
          analysis_type: analysisOptions.analysisTypes
        })
      });

      if (response.ok) {
        const result = await response.json();
        // Redirect to analysis dashboard
        router.push(`/analysis/${result.contract_id}`);
      } else {
        const error = await response.json();
        console.error('Analysis failed:', error);
        setIsAnalyzing(false);
      }
    } catch (error) {
      console.error('Error starting analysis:', error);
      setIsAnalyzing(false);
    }
  };

  const handleUpload = async (files: FileList) => {
    if (!files.length) return;

    setIsAnalyzing(true);
    
    try {
      const sourceFiles: Record<string, string> = {};
      
      // Read all files
      for (let i = 0; i < files.length; i++) {
        const file = files[i];
        const content = await file.text();
        sourceFiles[file.name] = content;
      }

      const response = await fetch('/api/v1/contracts/upload', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}` // Add auth token
        },
        body: JSON.stringify({
          project_id: 'default', // Use default project for now
          contract_name: `Uploaded Contract ${Date.now()}`,
          source_files: sourceFiles
        })
      });

      if (response.ok) {
        const result = await response.json();
        // Redirect to analysis dashboard
        router.push(`/analysis/${result.contract_id}`);
      } else {
        const error = await response.json();
        console.error('Upload failed:', error);
        setIsAnalyzing(false);
      }
    } catch (error) {
      console.error('Error uploading contract:', error);
      setIsAnalyzing(false);
    }
  };

  const chains = [
    { id: 1, name: 'Ethereum Mainnet', icon: '⟠' },
    { id: 5, name: 'Goerli Testnet', icon: '⟠' },
    { id: 137, name: 'Polygon', icon: '⬢' },
    { id: 56, name: 'BSC', icon: '🟡' },
    { id: 43114, name: 'Avalanche', icon: '🔺' },
    { id: 42161, name: 'Arbitrum', icon: '🔷' },
    { id: 10, name: 'Optimism', icon: '🔴' }
  ];

  const analysisTypeOptions = [
    { 
      id: 'security', 
      name: 'Security Analysis', 
      description: 'Comprehensive vulnerability detection and security review',
      icon: ShieldCheckIcon,
      color: 'text-red-600 bg-red-50'
    },
    { 
      id: 'risk', 
      name: 'Risk Assessment', 
      description: 'Financial, operational, and technical risk evaluation',
      icon: ChartBarIcon,
      color: 'text-orange-600 bg-orange-50'
    },
    { 
      id: 'gas', 
      name: 'Gas Optimization', 
      description: 'Gas usage analysis and optimization opportunities',
      icon: CpuChipIcon,
      color: 'text-green-600 bg-green-50'
    },
    { 
      id: 'compliance', 
      name: 'Compliance Check', 
      description: 'Standards and best practices compliance verification',
      icon: DocumentArrowUpIcon,
      color: 'text-blue-600 bg-blue-50'
    }
  ];

  const aiTools = [
    { name: 'GPT-4', description: 'OpenAI\'s most advanced language model', color: 'bg-green-500' },
    { name: 'Claude-3', description: 'Anthropic\'s constitutional AI model', color: 'bg-purple-500' }
  ];

  const staticTools = [
    { name: 'Slither', description: 'Static analysis framework for Solidity', color: 'bg-indigo-500' },
    { name: 'Mythril', description: 'Security analysis tool for EVM bytecode', color: 'bg-cyan-500' },
    { name: 'Semgrep', description: 'Static analysis tool for finding bugs', color: 'bg-teal-500' }
  ];

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-8">
      <div className="text-center mb-8">
        <div className="flex justify-center mb-4">
          <div className="w-20 h-20 bg-gradient-to-r from-blue-500 via-purple-600 to-green-500 rounded-full flex items-center justify-center">
            <SparklesIcon className="w-10 h-10 text-white" />
          </div>
        </div>
        <h2 className="text-4xl font-bold text-gray-900 mb-4">
          ClauseLens AI
        </h2>
        <p className="text-xl text-gray-600 max-w-3xl mx-auto">
          Revolutionary smart contract analysis powered by cutting-edge AI models and 
          industry-standard security tools. Get comprehensive insights in minutes, not hours.
        </p>
        
        {/* Key Features */}
        <div className="flex justify-center space-x-8 mt-6">
          <div className="flex items-center space-x-2 text-sm text-gray-600">
            <SparklesIcon className="w-4 h-4 text-green-500" />
            <span>AI-Powered</span>
          </div>
          <div className="flex items-center space-x-2 text-sm text-gray-600">
            <ShieldCheckIcon className="w-4 h-4 text-blue-500" />
            <span>Security First</span>
          </div>
          <div className="flex items-center space-x-2 text-sm text-gray-600">
            <CpuChipIcon className="w-4 h-4 text-purple-500" />
            <span>Real-time Analysis</span>
          </div>
        </div>
      </div>

      <div className="max-w-5xl mx-auto">
        {/* Analysis Method Tabs */}
        <div className="flex justify-center mb-8">
          <div className="bg-gray-100 rounded-lg p-1 flex">
            <button
              onClick={() => setShowUpload(false)}
              className={`px-8 py-3 rounded-md font-medium transition-all duration-200 ${
                !showUpload 
                  ? 'bg-white text-blue-600 shadow-sm transform scale-105' 
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              <div className="flex items-center space-x-2">
                <MagnifyingGlassIcon className="w-5 h-5" />
                <span>Analyze by Address</span>
              </div>
            </button>
            <button
              onClick={() => setShowUpload(true)}
              className={`px-8 py-3 rounded-md font-medium transition-all duration-200 ${
                showUpload 
                  ? 'bg-white text-blue-600 shadow-sm transform scale-105' 
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              <div className="flex items-center space-x-2">
                <DocumentArrowUpIcon className="w-5 h-5" />
                <span>Upload Source Code</span>
              </div>
            </button>
          </div>
        </div>

        {!showUpload ? (
          /* Contract Address Analysis */
          <div className="space-y-6">
            <div className="grid md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-3">
                  Smart Contract Address
                </label>
                <div className="relative">
                  <input
                    type="text"
                    value={contractAddress}
                    onChange={(e) => setContractAddress(e.target.value)}
                    placeholder="0x742d35Cc6634C0532925a3b8D1C9CEE0FC1e1234"
                    className="w-full px-4 py-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent font-mono text-sm"
                  />
                  <div className="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
                    <MagnifyingGlassIcon className="w-5 h-5 text-gray-400" />
                  </div>
                </div>
              </div>
              
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-3">
                  Blockchain Network
                </label>
                <select
                  value={chainId}
                  onChange={(e) => setChainId(Number(e.target.value))}
                  className="w-full px-4 py-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  {chains.map(chain => (
                    <option key={chain.id} value={chain.id}>
                      {chain.icon} {chain.name}
                    </option>
                  ))}
                </select>
              </div>
            </div>
          </div>
        ) : (
          /* File Upload */
          <div className="space-y-6">
            <div className="border-2 border-dashed border-gray-300 rounded-xl p-12 text-center hover:border-blue-400 transition-colors bg-gray-50 hover:bg-blue-50">
              <DocumentArrowUpIcon className="w-16 h-16 text-gray-400 mx-auto mb-4" />
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                Upload Smart Contract Files
              </h3>
              <p className="text-gray-600 mb-6">
                Drop your Solidity (.sol) or Vyper (.vy) files here, or click to browse
              </p>
              <input
                type="file"
                multiple
                accept=".sol,.vy"
                onChange={(e) => e.target.files && handleUpload(e.target.files)}
                className="hidden"
                id="file-upload"
              />
              <label
                htmlFor="file-upload"
                className="btn-primary cursor-pointer inline-flex items-center space-x-2 px-8 py-3"
              >
                <DocumentArrowUpIcon className="w-5 h-5" />
                <span>Choose Files</span>
              </label>
              <p className="text-xs text-gray-500 mt-4">
                Supports multiple files • Maximum 10MB per file • Secure processing
              </p>
            </div>
          </div>
        )}

        {/* Analysis Configuration */}
        <div className="bg-gradient-to-br from-gray-50 to-blue-50 rounded-xl p-8 mt-8">
          <h3 className="text-xl font-semibold text-gray-900 mb-6 text-center">
            Analysis Configuration
          </h3>
          
          <div className="grid lg:grid-cols-2 gap-8">
            {/* Analysis Types */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-4">
                Analysis Types
              </label>
              <div className="space-y-3">
                {analysisTypeOptions.map(option => {
                  const Icon = option.icon;
                  return (
                    <label key={option.id} className="flex items-start space-x-3 cursor-pointer group">
                      <input
                        type="checkbox"
                        checked={analysisOptions.analysisTypes.includes(option.id)}
                        onChange={(e) => {
                          if (e.target.checked) {
                            setAnalysisOptions(prev => ({
                              ...prev,
                              analysisTypes: [...prev.analysisTypes, option.id]
                            }));
                          } else {
                            setAnalysisOptions(prev => ({
                              ...prev,
                              analysisTypes: prev.analysisTypes.filter(t => t !== option.id)
                            }));
                          }
                        }}
                        className="mt-1 h-5 w-5 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                      />
                      <div className="flex-1 p-3 rounded-lg group-hover:bg-white transition-colors">
                        <div className="flex items-center space-x-2 mb-1">
                          <div className={`p-1 rounded ${option.color}`}>
                            <Icon className="w-4 h-4" />
                          </div>
                          <span className="font-semibold text-gray-900">{option.name}</span>
                        </div>
                        <p className="text-sm text-gray-600">{option.description}</p>
                      </div>
                    </label>
                  );
                })}
              </div>
            </div>

            {/* Analysis Tools */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-4">
                Analysis Tools
              </label>
              <div className="space-y-4">
                {/* AI Analysis */}
                <label className="flex items-start space-x-3 cursor-pointer group">
                  <input
                    type="checkbox"
                    checked={analysisOptions.useAI}
                    onChange={(e) => setAnalysisOptions(prev => ({ ...prev, useAI: e.target.checked }))}
                    className="mt-1 h-5 w-5 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                  />
                  <div className="flex-1 p-4 rounded-lg group-hover:bg-white transition-colors border border-gray-200">
                    <div className="flex items-center space-x-2 mb-2">
                      <SparklesIcon className="w-5 h-5 text-purple-600" />
                      <span className="font-semibold text-gray-900">AI-Powered Analysis</span>
                      <div className="flex space-x-1">
                        {aiTools.map(tool => (
                          <span key={tool.name} className={`px-2 py-1 ${tool.color} text-white text-xs rounded-full`}>
                            {tool.name}
                          </span>
                        ))}
                      </div>
                    </div>
                    <p className="text-sm text-gray-600 mb-2">
                      Advanced AI models provide deep contextual analysis and natural language explanations
                    </p>
                    <div className="text-xs text-gray-500">
                      • Contextual vulnerability analysis • Natural language explanations • Advanced pattern recognition
                    </div>
                  </div>
                </label>

                {/* Static Analysis */}
                <label className="flex items-start space-x-3 cursor-pointer group">
                  <input
                    type="checkbox"
                    checked={analysisOptions.useStaticAnalysis}
                    onChange={(e) => setAnalysisOptions(prev => ({ ...prev, useStaticAnalysis: e.target.checked }))}
                    className="mt-1 h-5 w-5 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                  />
                  <div className="flex-1 p-4 rounded-lg group-hover:bg-white transition-colors border border-gray-200">
                    <div className="flex items-center space-x-2 mb-2">
                      <CpuChipIcon className="w-5 h-5 text-indigo-600" />
                      <span className="font-semibold text-gray-900">Static Analysis</span>
                      <div className="flex space-x-1">
                        {staticTools.map(tool => (
                          <span key={tool.name} className={`px-2 py-1 ${tool.color} text-white text-xs rounded-full`}>
                            {tool.name}
                          </span>
                        ))}
                      </div>
                    </div>
                    <p className="text-sm text-gray-600 mb-2">
                      Industry-standard static analysis tools for comprehensive vulnerability detection
                    </p>
                    <div className="text-xs text-gray-500">
                      • Pattern-based detection • Formal verification • Industry standards compliance
                    </div>
                  </div>
                </label>
              </div>
            </div>
          </div>
        </div>

        {/* Action Button */}
        <div className="text-center mt-10">
          <button
            onClick={handleAnalyze}
            disabled={(!contractAddress && !showUpload) || isAnalyzing || analysisOptions.analysisTypes.length === 0}
            className={`px-12 py-5 text-lg font-semibold rounded-xl transition-all duration-300 ${
              isAnalyzing
                ? 'bg-gray-400 text-gray-700 cursor-not-allowed'
                : 'bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white shadow-lg hover:shadow-xl transform hover:scale-105'
            }`}
          >
            <div className="flex items-center space-x-3">
              <SparklesIcon className="w-6 h-6" />
              <span>
                {isAnalyzing 
                  ? 'Initializing Analysis...' 
                  : `Start AI-Powered Analysis`
                }
              </span>
            </div>
          </button>
          
          {isAnalyzing && (
            <div className="mt-6">
              <div className="inline-flex items-center px-6 py-3 bg-blue-50 rounded-lg">
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-blue-600 mr-3"></div>
                <span className="text-blue-700 font-medium">
                  Preparing comprehensive analysis with AI and static analysis tools...
                </span>
              </div>
            </div>
          )}
          
          {analysisOptions.analysisTypes.length === 0 && (
            <p className="text-red-600 text-sm mt-3">
              Please select at least one analysis type to continue.
            </p>
          )}
        </div>

        {/* Features Highlight */}
        <div className="mt-16 grid md:grid-cols-3 gap-8">
          <div className="text-center p-6 bg-white rounded-xl shadow-sm border border-gray-100">
            <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-purple-600 rounded-2xl flex items-center justify-center mx-auto mb-4">
              <SparklesIcon className="w-8 h-8 text-white" />
            </div>
            <h4 className="font-bold text-gray-900 mb-2 text-lg">AI-Native Security</h4>
            <p className="text-gray-600">
              Revolutionary AI models understand context, intent, and complex attack vectors
            </p>
          </div>
          
          <div className="text-center p-6 bg-white rounded-xl shadow-sm border border-gray-100">
            <div className="w-16 h-16 bg-gradient-to-br from-green-500 to-teal-600 rounded-2xl flex items-center justify-center mx-auto mb-4">
              <ShieldCheckIcon className="w-8 h-8 text-white" />
            </div>
            <h4 className="font-bold text-gray-900 mb-2 text-lg">Comprehensive Coverage</h4>
            <p className="text-gray-600">
              Security, risk, gas optimization, and compliance analysis in one platform
            </p>
          </div>
          
          <div className="text-center p-6 bg-white rounded-xl shadow-sm border border-gray-100">
            <div className="w-16 h-16 bg-gradient-to-br from-orange-500 to-red-600 rounded-2xl flex items-center justify-center mx-auto mb-4">
              <CpuChipIcon className="w-8 h-8 text-white" />
            </div>
            <h4 className="font-bold text-gray-900 mb-2 text-lg">Real-time Insights</h4>
            <p className="text-gray-600">
              Live progress updates and instant results delivered via real-time WebSocket
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};
