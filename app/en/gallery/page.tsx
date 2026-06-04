import Link from 'next/link';
import Image from 'next/image';
import { getExhibits } from '@/lib/content';

export const metadata = { title: 'Exhibits — African Art Gallery' };

export default function EnGalleryPage() {
  const exhibits = getExhibits('en-us');

  return (
    <div className="max-w-8xl mx-auto px-4 sm:px-6 lg:px-12 py-10 sm:py-16">
      <h1 className="serif italic font-light text-4xl sm:text-5xl md:text-6xl text-center mb-10 sm:mb-16 tracking-wide">
        Exhibits
      </h1>

      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-x-4 sm:gap-x-8 gap-y-8 sm:gap-y-12">
        {exhibits.map(ex => (
          <Link key={ex.slug} href={`/en/gallery/${ex.slug}`} className="group block">
            <div className="aspect-[3/4] relative overflow-hidden bg-white">
              {ex.image && (
                <Image
                  src={ex.image}
                  alt={ex.imageAlt}
                  fill
                  sizes="(max-width:768px) 50vw, (max-width:1024px) 33vw, 25vw"
                  className="object-contain p-2 group-hover:scale-105 transition-transform duration-500"
                />
              )}
            </div>
            <div className="mt-3 sm:mt-4">
              <h2 className="serif italic text-xl sm:text-2xl mb-1">{ex.title}</h2>
              <p className="text-xs sm:text-sm opacity-70 line-clamp-2">{ex.shortDescription}</p>
              <span className="inline-block mt-2 text-xs uppercase tracking-wider opacity-50 group-hover:opacity-100">
                See more
              </span>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}
