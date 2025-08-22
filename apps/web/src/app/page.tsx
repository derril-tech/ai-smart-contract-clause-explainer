import { ContractAnalyzer } from '@/components/contract/ContractAnalyzer';
import { HeroSection } from '@/components/home/HeroSection';
import { FeaturesSection } from '@/components/home/FeaturesSection';
import { HowItWorksSection } from '@/components/home/HowItWorksSection';

export default function HomePage() {
  return (
    <div className="min-h-screen">
      {/* Hero Section with Contract Analyzer */}
      <HeroSection />
      
      {/* Main Contract Analysis Interface */}
      <section className="py-16 bg-white dark:bg-gray-900">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
              Analyze Your Smart Contract
            </h2>
            <p className="text-lg text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
              Paste a contract address, upload source code, or link to a repository. 
              Get instant plain-English explanations of obligations, risks, and rights.
            </p>
          </div>
          
          <ContractAnalyzer />
        </div>
      </section>
      
      {/* Features Section */}
      <FeaturesSection />
      
      {/* How It Works Section */}
      <HowItWorksSection />
    </div>
  );
}
