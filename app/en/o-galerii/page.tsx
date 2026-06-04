import SliceRenderer from '@/components/SliceRenderer';
import { getPage } from '@/lib/content';

export const metadata = { title: 'About — African Art Gallery' };

export default function EnAbout() {
  const page = getPage('o-galerii', 'en-us');
  if (!page) return <div className="p-12">No content.</div>;
  return (
    <div className="pb-12">
      <SliceRenderer slices={page.slices} />
    </div>
  );
}
