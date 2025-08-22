import { useState } from 'react';
import { AlertCircle, CheckCircle, Clock, FileText, Shield, Zap } from 'lucide-react';

interface AnalysisResult {
  id: string;
  status: 'pending' | 'processing' | 'completed' | 'failed';
  progress: number;
  findings: Finding[];
  explanations: Explanation[];
  risks: Risk[];
}

interface Finding {
  id: string;
  title: string;
  description: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
  category: string;
  line?: number;
  function?: string;
}

interface Explanation {
  id: string;
  type: 'function' | 'modifier' | 'event';
  name: string;
  explanation: string;
  risks: Risk[];
  examples: string[];
  citations: Citation[];
}

interface Risk {
  id: string;
  type: string;
  description: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
  mitigation?: string;
}

interface Citation {
  type: 'code' | 'documentation' | 'standard';
  line?: number;
  content: string;
  url?: string;
}

export function ContractAnalyzer() {
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null);

  // Mock analysis function
  const startAnalysis = async () => {
    setIsAnalyzing(true);
    
    // Simulate analysis progress
    const mockResult: AnalysisResult = {
      id: 'analysis_123',
      status: 'completed',
      progress: 100,
      findings: [
        {
          id: 'finding_1',
          title: 'Integer Overflow and Underflow',
          description: 'The contract uses arithmetic operations without checking for overflow/underflow',
          severity: 'high',
          category: 'SWC-101',
          line: 45,
          function: 'transfer'
        },
        {
          id: 'finding_2',
          title: 'Centralized Ownership',
          description: 'Contract has a single owner with extensive privileges',
          severity: 'medium',
          category: 'Access Control',
          line: 12
        }
      ],
      explanations: [
        {
          id: 'expl_1',
          type: 'function',
          name: 'transfer',
          explanation: 'This function allows the caller to transfer tokens to another address. It includes checks for sufficient balance and valid recipient address.',
          risks: [
            {
              id: 'risk_1',
              type: 'reentrancy',
              description: 'Potential reentrancy attack if recipient is a contract',
              severity: 'medium'
            }
          ],
          examples: ['transfer(0x123..., 100)'],
          citations: [
            {
              type: 'code',
              line: 45,
              content: 'function transfer(address to, uint256 amount) public returns (bool)'
            }
          ]
        }
      ],
      risks: [
        {
          id: 'risk_1',
          type: 'reentrancy',
          description: 'Potential reentrancy attack in transfer function',
          severity: 'medium',
          mitigation: 'Use ReentrancyGuard modifier'
        }
      ]
    };

    // Simulate processing time
    setTimeout(() => {
      setAnalysisResult(mockResult);
      setIsAnalyzing(false);
    }, 3000);
  };

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical': return 'text-red-600 bg-red-100 dark:bg-red-900/20';
      case 'high': return 'text-red-600 bg-red-50 dark:bg-red-900/10';
      case 'medium': return 'text-yellow-600 bg-yellow-50 dark:bg-yellow-900/10';
      case 'low': return 'text-green-600 bg-green-50 dark:bg-green-900/10';
      default: return 'text-gray-600 bg-gray-50 dark:bg-gray-900/10';
    }
  };

  const getSeverityIcon = (severity: string) => {
    switch (severity) {
      case 'critical':
      case 'high':
        return <AlertCircle className="w-4 h-4" />;
      case 'medium':
        return <Clock className="w-4 h-4" />;
      case 'low':
        return <CheckCircle className="w-4 h-4" />;
      default:
        return <FileText className="w-4 h-4" />;
    }
  };

  return (
    <div className="max-w-6xl mx-auto">
      {!analysisResult ? (
        // Analysis Interface
        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-8 border border-gray-200 dark:border-gray-700">
          <div className="text-center mb-8">
            <h3 className="text-2xl font-semibold text-gray-900 dark:text-white mb-2">
              Smart Contract Analysis
            </h3>
            <p className="text-gray-600 dark:text-gray-300">
              Get comprehensive security analysis and plain-English explanations
            </p>
          </div>

          {isAnalyzing ? (
            // Analysis Progress
            <div className="text-center py-12">
              <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-primary-600 mx-auto mb-4"></div>
              <h4 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
                Analyzing Contract...
              </h4>
              <p className="text-gray-600 dark:text-gray-300">
                Running security analysis and generating explanations
              </p>
              
              {/* Progress steps */}
              <div className="mt-8 space-y-3">
                <div className="flex items-center justify-center gap-3 text-sm">
                  <CheckCircle className="w-4 h-4 text-green-500" />
                  <span className="text-gray-600 dark:text-gray-300">Contract verification</span>
                </div>
                <div className="flex items-center justify-center gap-3 text-sm">
                  <Clock className="w-4 h-4 text-yellow-500" />
                  <span className="text-gray-600 dark:text-gray-300">Static analysis</span>
                </div>
                <div className="flex items-center justify-center gap-3 text-sm">
                  <Clock className="w-4 h-4 text-gray-400" />
                  <span className="text-gray-500 dark:text-gray-400">AI explanation generation</span>
                </div>
              </div>
            </div>
          ) : (
            // Start Analysis Button
            <div className="text-center">
              <button
                onClick={startAnalysis}
                className="bg-primary-600 hover:bg-primary-700 text-white font-semibold py-4 px-8 rounded-lg transition-colors duration-200 flex items-center justify-center gap-2 mx-auto"
              >
                <Zap className="w-5 h-5" />
                Start Analysis
              </button>
              <p className="text-sm text-gray-500 dark:text-gray-400 mt-3">
                Analysis typically takes 2-5 minutes
              </p>
            </div>
          )}
        </div>
      ) : (
        // Analysis Results
        <div className="space-y-6">
          {/* Summary Card */}
          <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6 border border-gray-200 dark:border-gray-700">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white">
                Analysis Summary
              </h3>
              <div className="flex items-center gap-2">
                <CheckCircle className="w-5 h-5 text-green-500" />
                <span className="text-sm text-gray-600 dark:text-gray-300">Completed</span>
              </div>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div className="text-center p-4 bg-red-50 dark:bg-red-900/10 rounded-lg">
                <div className="text-2xl font-bold text-red-600">1</div>
                <div className="text-sm text-gray-600 dark:text-gray-300">High Risk</div>
              </div>
              <div className="text-center p-4 bg-yellow-50 dark:bg-yellow-900/10 rounded-lg">
                <div className="text-2xl font-bold text-yellow-600">1</div>
                <div className="text-sm text-gray-600 dark:text-gray-300">Medium Risk</div>
              </div>
              <div className="text-center p-4 bg-green-50 dark:bg-green-900/10 rounded-lg">
                <div className="text-2xl font-bold text-green-600">0</div>
                <div className="text-sm text-gray-600 dark:text-gray-300">Low Risk</div>
              </div>
              <div className="text-center p-4 bg-blue-50 dark:bg-blue-900/10 rounded-lg">
                <div className="text-2xl font-bold text-blue-600">1</div>
                <div className="text-sm text-gray-600 dark:text-gray-300">Functions</div>
              </div>
            </div>
          </div>

          {/* Findings */}
          <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6 border border-gray-200 dark:border-gray-700">
            <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
              <Shield className="w-5 h-5" />
              Security Findings
            </h3>
            
            <div className="space-y-4">
              {analysisResult.findings.map((finding) => (
                <div
                  key={finding.id}
                  className="p-4 border border-gray-200 dark:border-gray-600 rounded-lg"
                >
                  <div className="flex items-start justify-between mb-2">
                    <h4 className="font-medium text-gray-900 dark:text-white">
                      {finding.title}
                    </h4>
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${getSeverityColor(finding.severity)}`}>
                      {finding.severity.toUpperCase()}
                    </span>
                  </div>
                  <p className="text-gray-600 dark:text-gray-300 text-sm mb-2">
                    {finding.description}
                  </p>
                  {finding.line && (
                    <p className="text-xs text-gray-500 dark:text-gray-400">
                      Line {finding.line} • Function: {finding.function}
                    </p>
                  )}
                </div>
              ))}
            </div>
          </div>

          {/* Explanations */}
          <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6 border border-gray-200 dark:border-gray-700">
            <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
              <FileText className="w-5 h-5" />
              Plain English Explanations
            </h3>
            
            <div className="space-y-6">
              {analysisResult.explanations.map((explanation) => (
                <div key={explanation.id} className="border-b border-gray-200 dark:border-gray-600 pb-6 last:border-b-0">
                  <div className="flex items-center gap-2 mb-3">
                    <span className="px-2 py-1 bg-primary-100 dark:bg-primary-900/20 text-primary-700 dark:text-primary-300 text-xs font-medium rounded">
                      {explanation.type}
                    </span>
                    <h4 className="font-medium text-gray-900 dark:text-white">
                      {explanation.name}
                    </h4>
                  </div>
                  
                  <p className="text-gray-700 dark:text-gray-300 mb-4">
                    {explanation.explanation}
                  </p>
                  
                  {explanation.risks.length > 0 && (
                    <div className="mb-4">
                      <h5 className="text-sm font-medium text-gray-900 dark:text-white mb-2">
                        Potential Risks:
                      </h5>
                      <div className="space-y-2">
                        {explanation.risks.map((risk) => (
                          <div key={risk.id} className="flex items-start gap-2">
                            {getSeverityIcon(risk.severity)}
                            <span className="text-sm text-gray-600 dark:text-gray-300">
                              {risk.description}
                            </span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                  
                  {explanation.examples.length > 0 && (
                    <div>
                      <h5 className="text-sm font-medium text-gray-900 dark:text-white mb-2">
                        Example Usage:
                      </h5>
                      <div className="bg-gray-50 dark:bg-gray-700 p-3 rounded text-sm font-mono text-gray-800 dark:text-gray-200">
                        {explanation.examples[0]}
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
