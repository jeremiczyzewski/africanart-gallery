import SliceRenderer from '@/components/SliceRenderer';
import { getPage } from '@/lib/content';

export const metadata = { title: 'Curators — African Art Gallery' };

export default function EnCurators() {
  const page = getPage('tworcy-galerii', 'en-us');
  if (!page) return <div className="p-12">No content.</div>;
  return (
    <div className="pb-12">
      <SliceRenderer slices={page.slices} />
    </div>
  );
}
