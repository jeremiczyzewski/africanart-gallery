import SliceRenderer from '@/components/SliceRenderer';
import { getPage } from '@/lib/content';

export const metadata = { title: 'Kontakt — African Art Gallery' };

export default function Kontakt() {
  const page = getPage('kontakt', 'pl');
  if (!page) return <div className="p-12">Brak treści.</div>;
  return (
    <div className="pb-12">
      <SliceRenderer slices={page.slices} />
    </div>
  );
}
