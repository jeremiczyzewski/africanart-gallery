import Image from 'next/image';
import RichText from './RichText';

function prismicImg(url: string) {
  // Jezeli URL z images.prismic.io, mamy lokalna kopie - dopasuj
  // Jezeli juz /uploads/ - przepuscic
  if (!url) return '';
  if (url.startsWith('/uploads/')) return url;
  if (url.includes('images.prismic.io')) {
    // wypisuje tylko ID + nazwe pliku
    const m = url.match(/images\.prismic\.io\/[^/]+\/([^?]+)/);
    if (m) return `/uploads/images/${m[1]}`;
  }
  return url;
}

export default function SliceRenderer({ slices }: { slices: any[] }) {
  if (!Array.isArray(slices)) return null;
  return (
    <>
      {slices.map((s, i) => {
        const type = s.slice_type;
        const variation = s.variation;
        const p = s.primary || {};

        if (type === 'header') {
          return (
            <header key={i} className="max-w-4xl mx-auto text-center py-16 px-6">
              <h1 className="serif italic font-light text-5xl md:text-6xl tracking-wide">
                {p.title || ''}
              </h1>
              {Array.isArray(p.text) && <RichText blocks={p.text} className="mt-6 opacity-80" />}
            </header>
          );
        }

        if (type === 'image') {
          if (!p.image?.url) return null;
          return (
            <div key={i} className="max-w-6xl mx-auto px-6 mb-12">
              <div className="relative aspect-[21/9] w-full">
                <Image
                  src={prismicImg(p.image.url)}
                  alt={p.image.alt || ''}
                  fill
                  className="object-cover"
                  sizes="(max-width:1024px) 100vw, 1100px"
                />
              </div>
            </div>
          );
        }

        if (type === 'text') {
          const cols = variation === 'twoColumns' ? 'md:columns-2 md:gap-12' : '';
          const center = variation === 'oneColumnCentered' ? 'text-center mx-auto' : '';
          return (
            <section key={i} className={`max-w-4xl mx-auto px-6 py-8 ${center}`}>
              <RichText blocks={p.text} className={cols} />
            </section>
          );
        }

        if (type === 'text_with_image') {
          return (
            <section key={i} className="max-w-5xl mx-auto px-6 py-10 grid md:grid-cols-[1fr,2fr] gap-8 items-start">
              {p.image?.url && (
                <div className="relative aspect-[3/4] w-full bg-white">
                  <Image
                    src={prismicImg(p.image.url)}
                    alt={p.image.alt || p.title || ''}
                    fill
                    className="object-cover"
                    sizes="(max-width:768px) 100vw, 350px"
                  />
                </div>
              )}
              <div>
                {p.title && (
                  <h2 className="serif italic text-3xl md:text-4xl mb-4">{p.title}</h2>
                )}
                <RichText blocks={p.text} className="opacity-90" />
              </div>
            </section>
          );
        }

        if (type === 'contact_form') {
          return (
            <section key={i} className="max-w-2xl mx-auto px-6 py-12">
              <form className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <input
                    type="text"
                    placeholder={p.nameLabel || 'Imię'}
                    className="border-b border-aag-black bg-transparent p-2 text-sm focus:outline-none"
                  />
                  <input
                    type="text"
                    placeholder={p.lastNameLabel || 'Nazwisko'}
                    className="border-b border-aag-black bg-transparent p-2 text-sm focus:outline-none"
                  />
                </div>
                <input
                  type="email"
                  placeholder={p.emailLabel || 'Email'}
                  className="w-full border-b border-aag-black bg-transparent p-2 text-sm focus:outline-none"
                />
                <input
                  type="tel"
                  placeholder={p.phoneLabel || 'Telefon'}
                  className="w-full border-b border-aag-black bg-transparent p-2 text-sm focus:outline-none"
                />
                <textarea
                  placeholder={p.messageLabel || 'Wiadomość'}
                  rows={5}
                  className="w-full border border-aag-black bg-transparent p-3 text-sm focus:outline-none"
                />
                <button type="submit" className="btn-outline">
                  Wyślij
                </button>
              </form>
            </section>
          );
        }

        return null;
      })}
    </>
  );
}
