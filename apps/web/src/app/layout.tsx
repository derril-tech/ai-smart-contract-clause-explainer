import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';

// Import providers and components
import { Providers } from '@/components/providers';
import { Header } from '@/components/layout/Header';
import { Footer } from '@/components/layout/Footer';
import { Toaster } from '@/components/ui/Toaster';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'ClauseLens AI - Smart Contract Clause Explainer',
  description: 'Turn on-chain code into plain-English obligations, risks, and rights—instantly. AI-powered smart contract analysis and explanation platform.',
  keywords: 'smart contracts, blockchain, security, AI, analysis, DeFi, audit',
  authors: [{ name: 'ClauseLens AI Team' }],
  creator: 'ClauseLens AI',
  publisher: 'ClauseLens AI',
  formatDetection: {
    email: false,
    address: false,
    telephone: false,
  },
  metadataBase: new URL(process.env.NEXT_PUBLIC_APP_URL || 'http://localhost:3000'),
  openGraph: {
    title: 'ClauseLens AI - Smart Contract Clause Explainer',
    description: 'Turn on-chain code into plain-English obligations, risks, and rights—instantly.',
    url: '/',
    siteName: 'ClauseLens AI',
    images: [
      {
        url: '/og-image.png',
        width: 1200,
        height: 630,
        alt: 'ClauseLens AI - Smart Contract Analysis',
      },
    ],
    locale: 'en_US',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'ClauseLens AI - Smart Contract Clause Explainer',
    description: 'Turn on-chain code into plain-English obligations, risks, and rights—instantly.',
    images: ['/og-image.png'],
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
  verification: {
    google: 'your-google-verification-code',
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="h-full">
      <body className={`${inter.className} h-full bg-gray-50 dark:bg-gray-900`}>
        <Providers>
          <div className="min-h-screen flex flex-col">
            <Header />
            <main className="flex-1">
              {children}
            </main>
            <Footer />
          </div>
          <Toaster />
        </Providers>
      </body>
    </html>
  );
}
