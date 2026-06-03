'use client';

import { useEffect, useState } from 'react';
import Image from 'next/image';
import Link from 'next/link';

type Photo = { url: string; alt: string };

export default function HeroCarousel({
  photos,
  title,
  buttonText,
  buttonSlug,
  intervalMs = 5000,
}: {
  photos: Photo[];
  title: string;
  buttonText: string;
  buttonSlug: string;
  intervalMs?: number;
}) {
  const [active, setActive] = useState(0);

  useEffect(() => {
    if (photos.length <= 1) return;
    const t = setInterval(() => {
      setActive(i => (i + 1) % photos.length);
    }, intervalMs);
    return () => clearInterval(t);
  }, [photos.length, intervalMs]);

  if (!photos.length) return null;

  return (
    <section className="relative w-full h-[calc(100vh-100px)] min-h-[500px] overflow-hidden">
      {photos.map((p, i) => (
        <div
          key={p.url}
          className={`absolute inset-0 transition-opacity duration-1000 ease-in-out ${
            i === active ? 'opacity-100 z-0' : 'opacity-0 z-0'
          }`}
          aria-hidden={i !== active}
        >
          <Image
            src={p.url}
            alt={p.alt}
            fill
            priority={i === 0}
            className="object-cover"
            sizes="100vw"
          />
        </div>
      ))}

      <div className="absolute inset-0 bg-black/30 z-10" />

      <div className="relative z-20 h-full flex items-center justify-center lg:justify-end px-6 lg:px-16">
        <div className="text-center lg:text-right text-white max-w-2xl">
          <h1 className="serif italic font-light text-4xl sm:text-5xl md:text-6xl lg:text-7xl xl:text-8xl leading-tight mb-6 lg:mb-8 whitespace-pre-line">
            {title}
          </h1>
          <Link
            href={`/${buttonSlug}`}
            className="inline-block border border-white px-6 lg:px-8 py-2.5 lg:py-3 text-xs lg:text-sm uppercase tracking-wider text-white hover:bg-white hover:text-aag-black transition-colors"
          >
            {buttonText}
          </Link>
        </div>
      </div>

      {photos.length > 1 && (
        <div className="absolute bottom-8 left-1/2 -translate-x-1/2 z-30 flex gap-3">
          {photos.map((_, i) => (
            <button
              key={i}
              onClick={() => setActive(i)}
              aria-label={`Slide ${i + 1}`}
              className={`w-2.5 h-2.5 rounded-full border border-white transition-all ${
                i === active ? 'bg-white scale-110' : 'bg-transparent hover:bg-white/50'
              }`}
            />
          ))}
        </div>
      )}
    </section>
  );
}
