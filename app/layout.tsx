import type { Metadata } from 'next';
import { Cormorant_Garamond, Inter } from 'next/font/google';
import './globals.css';

const serif = Cormorant_Garamond({
  subsets: ['latin', 'latin-ext'],
  weight: ['400', '500', '600', '700'],
  style: ['normal', 'italic'],
  variable: '--font-serif',
  display: 'swap',
});

const sans = Inter({
  subsets: ['latin', 'latin-ext'],
  variable: '--font-sans',
  display: 'swap',
});

export const metadata: Metadata = {
  title: 'African Art Gallery',
  description:
    'Jedna z najciekawszych prywatnych kolekcji sztuki afrykańskiej w Polsce. Ponad 240 obiektów z Afryki Zachodniej i Centralnej.',
  icons: { icon: '/assets/favicon.png' },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="pl" className={`${serif.variable} ${sans.variable}`}>
      <body className="min-h-screen flex flex-col">{children}</body>
    </html>
  );
}
