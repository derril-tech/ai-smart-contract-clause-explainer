import { useState } from 'react';
import { Search, Shield, Zap, BarChart3 } from 'lucide-react';

export function HeroSection() {
  const [contractAddress, setContractAddress] = useState('');
  const [selectedChain, setSelectedChain] = useState('1'); // Ethereum mainnet

  const chains = [
    { id: '1', name: 'Ethereum', icon: '🔵' },
    { id: '10', name: 'Optimism', icon: '🔴' },
    { id: '42161', name: 'Arbitrum', icon: '🔵' },
    { id: '137', name: 'Polygon', icon: '🟣' },
    { id: '56', name: 'BSC', icon: '🟡' },
  ];

  const handleAnalyze = () => {
    // TODO: Implement contract analysis
    console.log('Analyzing contract:', contractAddress, 'on chain:', selectedChain);
  };

  return (
    <section className="relative bg-gradient-to-br from-primary-50 to-secondary-50 dark:from-gray-900 dark:to-gray-800 py-20 overflow-hidden">
      {/* Background decoration */}
      <div className="absolute inset-0 bg-grid-pattern opacity-5"></div>
      
      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h1 className="text-5xl md:text-6xl font-bold text-gray-900 dark:text-white mb-6">
            Turn Smart Contracts into
            <span className="text-primary-600 dark:text-primary-400 block">
              Plain English
            </span>
          </h1>
          
          <p className="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto mb-8">
            ClauseLens AI instantly explains smart contract obligations, risks, and rights. 
            Get comprehensive analysis with AI-powered insights and actionable recommendations.
          </p>

          {/* Feature highlights */}
          <div className="flex flex-wrap justify-center gap-8 mb-12">
            <div className="flex items-center gap-2 text-gray-600 dark:text-gray-300">
              <Shield className="w-5 h-5 text-success-500" />
              <span>Security Analysis</span>
            </div>
            <div className="flex items-center gap-2 text-gray-600 dark:text-gray-300">
              <Zap className="w-5 h-5 text-warning-500" />
              <span>Instant Results</span>
            </div>
            <div className="flex items-center gap-2 text-gray-600 dark:text-gray-300">
              <BarChart3 className="w-5 h-5 text-primary-500" />
              <span>Risk Assessment</span>
            </div>
          </div>
        </div>

        {/* Contract Analysis Interface */}
        <div className="max-w-4xl mx-auto">
          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8 border border-gray-200 dark:border-gray-700">
            <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-6 text-center">
              Analyze Your Smart Contract
            </h2>
            
            <div className="space-y-6">
              {/* Chain Selector */}
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
                  Select Blockchain Network
                </label>
                <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
                  {chains.map((chain) => (
                    <button
                      key={chain.id}
                      onClick={() => setSelectedChain(chain.id)}
                      className={`p-3 rounded-lg border-2 transition-all ${
                        selectedChain === chain.id
                          ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20'
                          : 'border-gray-200 dark:border-gray-600 hover:border-gray-300 dark:hover:border-gray-500'
                      }`}
                    >
                      <div className="text-2xl mb-1">{chain.icon}</div>
                      <div className="text-xs font-medium text-gray-700 dark:text-gray-300">
                        {chain.name}
                      </div>
                    </button>
                  ))}
                </div>
              </div>

              {/* Contract Address Input */}
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
                  Contract Address
                </label>
                <div className="relative">
                  <input
                    type="text"
                    value={contractAddress}
                    onChange={(e) => setContractAddress(e.target.value)}
                    placeholder="0x1234567890123456789012345678901234567890"
                    className="w-full px-4 py-3 pl-12 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400"
                  />
                  <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                </div>
                <p className="mt-2 text-sm text-gray-500 dark:text-gray-400">
                  Enter a verified smart contract address to begin analysis
                </p>
              </div>

              {/* Analysis Button */}
              <button
                onClick={handleAnalyze}
                disabled={!contractAddress.trim()}
                className="w-full bg-primary-600 hover:bg-primary-700 disabled:bg-gray-300 disabled:cursor-not-allowed text-white font-semibold py-4 px-6 rounded-lg transition-colors duration-200 flex items-center justify-center gap-2"
              >
                <Zap className="w-5 h-5" />
                Analyze Contract
              </button>

              {/* Alternative Input Methods */}
              <div className="text-center">
                <p className="text-sm text-gray-500 dark:text-gray-400 mb-3">
                  Or analyze by:
                </p>
                <div className="flex flex-wrap justify-center gap-3">
                  <button className="text-primary-600 hover:text-primary-700 dark:text-primary-400 dark:hover:text-primary-300 text-sm font-medium">
                    Upload Source Code
                  </button>
                  <span className="text-gray-300 dark:text-gray-600">•</span>
                  <button className="text-primary-600 hover:text-primary-700 dark:text-primary-400 dark:hover:text-primary-300 text-sm font-medium">
                    Link Repository
                  </button>
                  <span className="text-gray-300 dark:text-gray-600">•</span>
                  <button className="text-primary-600 hover:text-primary-700 dark:text-primary-400 dark:hover:text-primary-300 text-sm font-medium">
                    Browse Examples
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Trust indicators */}
        <div className="mt-16 text-center">
          <p className="text-sm text-gray-500 dark:text-gray-400 mb-4">
            Trusted by leading protocols and auditors
          </p>
          <div className="flex flex-wrap justify-center items-center gap-8 opacity-60">
            {/* TODO: Add actual logos */}
            <div className="h-8 w-24 bg-gray-200 dark:bg-gray-700 rounded"></div>
            <div className="h-8 w-24 bg-gray-200 dark:bg-gray-700 rounded"></div>
            <div className="h-8 w-24 bg-gray-200 dark:bg-gray-700 rounded"></div>
            <div className="h-8 w-24 bg-gray-200 dark:bg-gray-700 rounded"></div>
          </div>
        </div>
      </div>
    </section>
  );
}
