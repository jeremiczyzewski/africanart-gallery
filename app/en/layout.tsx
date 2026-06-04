import HeaderServer from '@/components/HeaderServer';
import Footer from '@/components/Footer';

export default function EnLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <HeaderServer lang="en-us" />
      <main className="flex-1">{children}</main>
      <Footer lang="en-us" />
    </>
  );
}
