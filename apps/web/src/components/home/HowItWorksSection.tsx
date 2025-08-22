import { Search, Shield, Brain, FileText, ArrowRight } from 'lucide-react';

const steps = [
  {
    icon: Search,
    title: 'Input Contract',
    description: 'Paste a contract address, upload source code, or link to a repository. We support all major blockchains.',
    color: 'text-blue-600 bg-blue-100 dark:bg-blue-900/20'
  },
  {
    icon: Shield,
    title: 'Security Analysis',
    description: 'Our advanced tools analyze the contract for vulnerabilities, access control issues, and security risks.',
    color: 'text-green-600 bg-green-100 dark:bg-green-900/20'
  },
  {
    icon: Brain,
    title: 'AI Explanation',
    description: 'AI generates plain-English explanations of functions, modifiers, and events with risk assessments.',
    color: 'text-purple-600 bg-purple-100 dark:bg-purple-900/20'
  },
  {
    icon: FileText,
    title: 'Detailed Report',
    description: 'Get comprehensive reports with citations, diagrams, and actionable recommendations.',
    color: 'text-orange-600 bg-orange-100 dark:bg-orange-900/20'
  }
];

export function HowItWorksSection() {
  return (
    <section className="py-20 bg-white dark:bg-gray-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
            How ClauseLens AI Works
          </h2>
          <p className="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
            Our four-step process delivers comprehensive smart contract analysis in minutes, not hours.
          </p>
        </div>

        <div className="relative">
          {/* Connection line */}
          <div className="hidden lg:block absolute top-1/2 left-0 right-0 h-0.5 bg-gradient-to-r from-blue-200 via-green-200 via-purple-200 to-orange-200 transform -translate-y-1/2"></div>
          
          <div className="grid grid-cols-1 lg:grid-cols-4 gap-8 lg:gap-4">
            {steps.map((step, index) => (
              <div key={index} className="relative">
                <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-lg border border-gray-200 dark:border-gray-700 text-center relative z-10">
                  <div className={`w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4 ${step.color}`}>
                    <step.icon className="w-8 h-8" />
                  </div>
                  
                  <div className="mb-4">
                    <span className="inline-flex items-center justify-center w-8 h-8 bg-primary-600 text-white text-sm font-bold rounded-full">
                      {index + 1}
                    </span>
                  </div>
                  
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">
                    {step.title}
                  </h3>
                  
                  <p className="text-gray-600 dark:text-gray-300 text-sm leading-relaxed">
                    {step.description}
                  </p>
                </div>
                
                {/* Arrow for mobile */}
                {index < steps.length - 1 && (
                  <div className="lg:hidden flex justify-center mt-4">
                    <ArrowRight className="w-6 h-6 text-gray-400" />
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Process details */}
        <div className="mt-20">
          <div className="bg-gray-50 dark:bg-gray-900 rounded-2xl p-8">
            <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-8 text-center">
              Advanced Analysis Pipeline
            </h3>
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              <div className="space-y-4">
                <h4 className="text-lg font-semibold text-gray-900 dark:text-white">
                  Static Analysis
                </h4>
                <ul className="space-y-2 text-sm text-gray-600 dark:text-gray-300">
                  <li>• Slither vulnerability detection</li>
                  <li>• Semgrep pattern matching</li>
                  <li>• Custom rule validation</li>
                  <li>• Code quality assessment</li>
                </ul>
              </div>
              
              <div className="space-y-4">
                <h4 className="text-lg font-semibold text-gray-900 dark:text-white">
                  Dynamic Analysis
                </h4>
                <ul className="space-y-2 text-sm text-gray-600 dark:text-gray-300">
                  <li>• Foundry invariant testing</li>
                  <li>• Echidna fuzz testing</li>
                  <li>• Storage layout analysis</li>
                  <li>• Gas optimization checks</li>
                </ul>
              </div>
              
              <div className="space-y-4">
                <h4 className="text-lg font-semibold text-gray-900 dark:text-white">
                  AI Processing
                </h4>
                <ul className="space-y-2 text-sm text-gray-600 dark:text-gray-300">
                  <li>• RAG-powered explanations</li>
                  <li>• Risk categorization</li>
                  <li>• Citation generation</li>
                  <li>• Context-aware insights</li>
                </ul>
              </div>
            </div>
          </div>
        </div>

        {/* CTA Section */}
        <div className="mt-16 text-center">
          <div className="bg-primary-50 dark:bg-primary-900/10 rounded-2xl p-8 border border-primary-200 dark:border-primary-800">
            <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
              Ready to Analyze Your Smart Contract?
            </h3>
            <p className="text-gray-600 dark:text-gray-300 mb-6 max-w-2xl mx-auto">
              Join thousands of developers, auditors, and security researchers who trust ClauseLens AI for comprehensive smart contract analysis.
            </p>
            <button className="bg-primary-600 hover:bg-primary-700 text-white font-semibold py-3 px-8 rounded-lg transition-colors duration-200">
              Start Free Analysis
            </button>
          </div>
        </div>
      </div>
    </section>
  );
}
