import SliceRenderer from '@/components/SliceRenderer';
import { getPage } from '@/lib/content';

export const metadata = { title: 'Twórcy galerii — African Art Gallery' };

export default function Tworcy() {
  const page = getPage('tworcy-galerii', 'pl');
  if (!page) return <div className="p-12">Brak treści.</div>;
  return (
    <div className="pb-12">
      <SliceRenderer slices={page.slices} />
    </div>
  );
}
