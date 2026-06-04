import SliceRenderer from '@/components/SliceRenderer';
import { getPage } from '@/lib/content';

export const metadata = { title: 'Contact — African Art Gallery' };

export default function EnContact() {
  const page = getPage('kontakt', 'en-us');
  if (!page) return <div className="p-12">No content.</div>;
  return (
    <div className="pb-12">
      <SliceRenderer slices={page.slices} />
    </div>
  );
}
