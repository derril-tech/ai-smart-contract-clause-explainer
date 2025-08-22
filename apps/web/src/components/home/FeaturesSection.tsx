import { Brain, Shield, Zap, BarChart3, FileText, Users, Lock, Globe } from 'lucide-react';

const features = [
  {
    icon: Brain,
    title: 'AI-Powered Explanations',
    description: 'Get plain-English explanations of complex smart contract functions, modifiers, and events with AI-generated insights.',
    color: 'text-blue-600 bg-blue-100 dark:bg-blue-900/20'
  },
  {
    icon: Shield,
    title: 'Comprehensive Security Analysis',
    description: 'Advanced static and dynamic analysis using industry-standard tools like Slither, Semgrep, and Foundry.',
    color: 'text-green-600 bg-green-100 dark:bg-green-900/20'
  },
  {
    icon: BarChart3,
    title: 'Risk Assessment & Mapping',
    description: 'Visual risk heatmaps and privilege mapping to identify potential vulnerabilities and access control issues.',
    color: 'text-red-600 bg-red-100 dark:bg-red-900/20'
  },
  {
    icon: Zap,
    title: 'Instant Results',
    description: 'Get analysis results in seconds, not hours. Real-time processing with streaming explanations.',
    color: 'text-yellow-600 bg-yellow-100 dark:bg-yellow-900/20'
  },
  {
    icon: FileText,
    title: 'Detailed Reports',
    description: 'Generate comprehensive PDF and Markdown reports with citations, diagrams, and actionable recommendations.',
    color: 'text-purple-600 bg-purple-100 dark:bg-purple-900/20'
  },
  {
    icon: Users,
    title: 'Multi-Chain Support',
    description: 'Analyze contracts across Ethereum, Polygon, BSC, Arbitrum, Optimism, and other major blockchains.',
    color: 'text-indigo-600 bg-indigo-100 dark:bg-indigo-900/20'
  },
  {
    icon: Lock,
    title: 'Enterprise Security',
    description: 'Bank-grade security with JWT authentication, role-based access control, and audit logging.',
    color: 'text-gray-600 bg-gray-100 dark:bg-gray-900/20'
  },
  {
    icon: Globe,
    title: 'Global Accessibility',
    description: 'Access from anywhere with our cloud-based platform. No local setup or installation required.',
    color: 'text-teal-600 bg-teal-100 dark:bg-teal-900/20'
  }
];

export function FeaturesSection() {
  return (
    <section className="py-20 bg-gray-50 dark:bg-gray-900">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
            Powerful Features for Smart Contract Analysis
          </h2>
          <p className="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
            Everything you need to understand, analyze, and secure smart contracts with AI-powered insights.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {features.map((feature, index) => (
            <div
              key={index}
              className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-lg border border-gray-200 dark:border-gray-700 hover:shadow-xl transition-shadow duration-300"
            >
              <div className={`w-12 h-12 rounded-lg flex items-center justify-center mb-4 ${feature.color}`}>
                <feature.icon className="w-6 h-6" />
              </div>
              
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">
                {feature.title}
              </h3>
              
              <p className="text-gray-600 dark:text-gray-300 text-sm leading-relaxed">
                {feature.description}
              </p>
            </div>
          ))}
        </div>

        {/* Additional capabilities */}
        <div className="mt-20">
          <div className="bg-white dark:bg-gray-800 rounded-2xl p-8 shadow-lg border border-gray-200 dark:border-gray-700">
            <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-6 text-center">
              Advanced Capabilities
            </h3>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <div className="text-center">
                <div className="w-16 h-16 bg-primary-100 dark:bg-primary-900/20 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Brain className="w-8 h-8 text-primary-600" />
                </div>
                <h4 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                  RAG-Powered Insights
                </h4>
                <p className="text-gray-600 dark:text-gray-300 text-sm">
                  Retrieval-Augmented Generation ensures all explanations are grounded in actual source code and documentation.
                </p>
              </div>
              
              <div className="text-center">
                <div className="w-16 h-16 bg-success-100 dark:bg-success-900/20 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Shield className="w-8 h-8 text-success-600" />
                </div>
                <h4 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                  SWC Compliance
                </h4>
                <p className="text-gray-600 dark:text-gray-300 text-sm">
                  Aligned with Smart Contract Weakness Classification (SWC) standards for comprehensive vulnerability detection.
                </p>
              </div>
              
              <div className="text-center">
                <div className="w-16 h-16 bg-warning-100 dark:bg-warning-900/20 rounded-full flex items-center justify-center mx-auto mb-4">
                  <BarChart3 className="w-8 h-8 text-warning-600" />
                </div>
                <h4 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                  Differential Analysis
                </h4>
                <p className="text-gray-600 dark:text-gray-300 text-sm">
                  Compare contract versions to identify changes, storage layout impacts, and new security risks.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
