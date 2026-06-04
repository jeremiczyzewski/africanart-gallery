import Link from 'next/link';
import Image from 'next/image';
import { notFound } from 'next/navigation';
import { getExhibit, getExhibits } from '@/lib/content';
import InlineMarkdown from '@/components/InlineMarkdown';

export async function generateStaticParams() {
  return getExhibits('en-us').map(ex => ({ slug: ex.slug }));
}

export async function generateMetadata({ params }: { params: { slug: string } }) {
  const ex = getExhibit(params.slug, 'en-us');
  if (!ex) return {};
  return { title: `${ex.title} — African Art Gallery` };
}

export default function EnExhibitPage({ params }: { params: { slug: string } }) {
  const ex = getExhibit(params.slug, 'en-us');
  if (!ex) notFound();

  return (
    <article className="max-w-8xl mx-auto px-6 lg:px-12 py-12">
      <div className="relative mb-10">
        <div className="relative w-full max-w-2xl aspect-[3/4] mx-auto bg-white">
          {ex.image && (
            <Image
              src={ex.image}
              alt={ex.imageAlt}
              fill
              priority
              sizes="(max-width:1024px) 90vw, 600px"
              className="object-contain p-4"
            />
          )}

          {ex.prevSlug && (
            <Link
              href={`/en/gallery/${ex.prevSlug}`}
              aria-label="Previous"
              className="absolute left-1 sm:-left-8 lg:-left-12 top-1/2 -translate-y-1/2 p-2 opacity-50 hover:opacity-100 transition-opacity bg-aag-beige/70 sm:bg-transparent rounded-full"
            >
              <Image src="/assets/left-arrow.svg" alt="" width={20} height={32} style={{ height: 'auto' }} />
            </Link>
          )}

          {ex.nextSlug && (
            <Link
              href={`/en/gallery/${ex.nextSlug}`}
              aria-label="Next"
              className="absolute right-1 sm:-right-8 lg:-right-12 top-1/2 -translate-y-1/2 p-2 opacity-50 hover:opacity-100 transition-opacity bg-aag-beige/70 sm:bg-transparent rounded-full"
            >
              <Image src="/assets/right-arrow.svg" alt="" width={20} height={32} style={{ height: 'auto' }} />
            </Link>
          )}
        </div>
      </div>

      <div className="text-center max-w-3xl mx-auto px-2">
        <h1 className="serif italic font-light text-4xl sm:text-5xl md:text-6xl mb-6">{ex.title}</h1>
        <div className="text-xs sm:text-sm uppercase tracking-wider leading-relaxed mb-8 whitespace-pre-line opacity-80">
          {ex.metadata}
        </div>
        {ex.body && (
          <InlineMarkdown className="text-sm leading-relaxed mb-10 opacity-90 max-w-2xl mx-auto text-left">
            {ex.body}
          </InlineMarkdown>
        )}
        {ex.pdfUrl && (
          <a href={ex.pdfUrl} target="_blank" rel="noopener noreferrer" className="btn-outline">
            {ex.pdfLabel || 'Download PDF documentation'}
          </a>
        )}
      </div>
    </article>
  );
}
