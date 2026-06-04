'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import Image from 'next/image';

type NavItem = { label: string; slug: string };
type SocialItem = { label: string; url: string; iconAlt: string };

export default function Header({
  nav,
  social,
  lang = 'pl',
}: {
  nav: NavItem[];
  social: SocialItem[];
  lang?: 'pl' | 'en-us';
}) {
  const [open, setOpen] = useState(false);
  const isEn = lang === 'en-us';
  const homeHref = isEn ? '/en' : '/';
  const navHref = (slug: string) => (isEn ? `/en/${slug}` : `/${slug}`);
  const langLabel = isEn ? 'ENGLISH' : 'POLSKI';
  const otherLangHref = isEn ? '/' : '/en';
  const otherLangLabel = isEn ? 'Polski' : 'English';
  const searchPlaceholder = isEn ? 'Search' : '';
  const menuLabelOpen = isEn ? 'Open menu' : 'Otwórz menu';
  const menuLabelClose = isEn ? 'Close menu' : 'Zamknij menu';

  // Zablokuj scroll body kiedy drawer otwarty
  useEffect(() => {
    document.body.style.overflow = open ? 'hidden' : '';
    return () => { document.body.style.overflow = ''; };
  }, [open]);

  // Zamknij drawer po zmianie route (nawigacja)
  useEffect(() => {
    const close = () => setOpen(false);
    window.addEventListener('popstate', close);
    return () => window.removeEventListener('popstate', close);
  }, []);

  const socialIconSize: Record<string, { w: number; h: number }> = {
    Facebook: { w: 9, h: 18 },
    Instagram: { w: 18, h: 18 },
    Youtube: { w: 20, h: 15 },
  };

  return (
    <header className="w-full border-b border-gray-300 bg-aag-beige relative z-40">
      <div className="max-w-8xl mx-auto px-4 lg:px-12 py-5 flex items-center gap-4 lg:gap-8">
        <Link href={homeHref} className="flex-shrink-0" onClick={() => setOpen(false)}>
          <Image
            src="/assets/logo.svg"
            alt="African Art Gallery"
            width={120}
            height={48}
            priority
            style={{ height: 'auto', width: 'auto', maxHeight: 48 }}
          />
        </Link>

        {/* Desktop nav */}
        <nav className="hidden lg:flex items-center gap-8 ml-auto">
          {nav.map(item => (
            <Link key={item.slug} href={navHref(item.slug)} className="nav-link">
              {item.label}
            </Link>
          ))}
        </nav>

        <div className="hidden lg:flex items-center gap-3 ml-6">
          <button aria-label="Szukaj" className="p-1">
            <Image src="/assets/search-icon.svg" alt="" width={16} height={16} style={{ height: 'auto' }} />
          </button>
          <input
            type="text"
            placeholder=""
            className="border-b border-gray-400 bg-transparent text-sm w-32 px-1 py-0.5 focus:outline-none focus:border-aag-black"
          />
        </div>

        <div className="hidden lg:flex items-center gap-4 ml-6">
          {social.map(s => {
            const sz = socialIconSize[s.label] || { w: 18, h: 18 };
            return (
              <a key={s.label} href={s.url} target="_blank" rel="noopener noreferrer" aria-label={s.label}>
                <Image
                  src={`/assets/${s.label.toLowerCase()}-icon.svg`}
                  alt={s.iconAlt}
                  width={sz.w}
                  height={sz.h}
                  style={{ height: 'auto' }}
                />
              </a>
            );
          })}
        </div>

        <div className="hidden lg:flex items-center gap-3 ml-6 text-sm uppercase tracking-wider">
          <span className="opacity-80">{langLabel}</span>
          <Link href={otherLangHref} className="text-xs hover:underline opacity-70 hover:opacity-100">
            {otherLangLabel}
          </Link>
        </div>

        {/* Mobile hamburger */}
        <button
          onClick={() => setOpen(v => !v)}
          aria-label={open ? menuLabelClose : menuLabelOpen}
          aria-expanded={open}
          className="lg:hidden ml-auto p-2 flex flex-col justify-center items-center gap-1.5 w-10 h-10"
        >
          <span className={`block w-6 h-[2px] bg-aag-black transition-all ${open ? 'rotate-45 translate-y-[7px]' : ''}`} />
          <span className={`block w-6 h-[2px] bg-aag-black transition-all ${open ? 'opacity-0' : ''}`} />
          <span className={`block w-6 h-[2px] bg-aag-black transition-all ${open ? '-rotate-45 -translate-y-[7px]' : ''}`} />
        </button>
      </div>

      {/* Mobile drawer */}
      <div
        className={`lg:hidden fixed inset-0 top-[73px] bg-aag-beige z-30 transition-transform duration-300 ${
          open ? 'translate-x-0' : 'translate-x-full'
        }`}
        aria-hidden={!open}
      >
        <div className="flex flex-col h-full px-6 py-8 gap-2 overflow-y-auto">
          {nav.map(item => (
            <Link
              key={item.slug}
              href={navHref(item.slug)}
              onClick={() => setOpen(false)}
              className="serif italic text-3xl py-4 border-b border-gray-300"
            >
              {item.label}
            </Link>
          ))}

          <div className="mt-8 flex items-center gap-6">
            {social.map(s => {
              const sz = socialIconSize[s.label] || { w: 18, h: 18 };
              return (
                <a key={s.label} href={s.url} target="_blank" rel="noopener noreferrer" aria-label={s.label}>
                  <Image
                    src={`/assets/${s.label.toLowerCase()}-icon.svg`}
                    alt={s.iconAlt}
                    width={sz.w * 1.5}
                    height={sz.h * 1.5}
                    style={{ height: 'auto' }}
                  />
                </a>
              );
            })}
          </div>

          <div className="mt-6 text-sm uppercase tracking-wider flex items-center gap-3">
            <span className="opacity-80">{langLabel}</span>
            <Link href={otherLangHref} onClick={() => setOpen(false)} className="text-xs underline opacity-80">
              {otherLangLabel}
            </Link>
          </div>
        </div>
      </div>
    </header>
  );
}
