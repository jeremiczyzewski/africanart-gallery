import HeaderServer from '@/components/HeaderServer';
import Footer from '@/components/Footer';

export default function PlLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <HeaderServer lang="pl" />
      <main className="flex-1">{children}</main>
      <Footer lang="pl" />
    </>
  );
}
