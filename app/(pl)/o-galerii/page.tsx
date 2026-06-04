import SliceRenderer from '@/components/SliceRenderer';
import { getPage } from '@/lib/content';

export const metadata = { title: 'O galerii — African Art Gallery' };

export default function OGalerii() {
  const page = getPage('o-galerii', 'pl');
  if (!page) return <div className="p-12">Brak treści.</div>;
  return (
    <div className="pb-12">
      <SliceRenderer slices={page.slices} />
    </div>
  );
}
