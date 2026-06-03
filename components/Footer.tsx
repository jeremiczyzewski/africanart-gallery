import { getFooter } from '@/lib/content';

export default function Footer() {
  const f = getFooter('pl');
  if (!f) return null;

  return (
    <footer className="bg-aag-dark text-white mt-20">
      <div className="max-w-8xl mx-auto px-6 lg:px-12 py-12 sm:py-16 grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-8 sm:gap-10">
        {f.phone && (
          <div>
            <h3 className="serif italic text-xl mb-3">{f.phone.title}</h3>
            <p className="text-sm">{f.phone.text}</p>
          </div>
        )}
        {f.email && (
          <div>
            <h3 className="serif italic text-xl mb-3">{f.email.title}</h3>
            <a href={`mailto:${f.email.text}`} className="text-sm hover:underline">
              {f.email.text}
            </a>
          </div>
        )}
        {f.address && (
          <div>
            <h3 className="serif italic text-xl mb-3">{f.address.title}</h3>
            <p className="text-sm">{f.address.address1}</p>
            <p className="text-sm">{f.address.address2}</p>
          </div>
        )}
        {f.socialMedia && (
          <div>
            <h3 className="serif italic text-xl mb-3">{f.socialMedia.title}</h3>
            <ul className="text-sm space-y-1">
              {(f.socialMedia.link || []).map((l: any) => (
                <li key={l.url}>
                  <a href={l.url} target="_blank" rel="noopener noreferrer" className="hover:underline">
                    {l.text}
                  </a>
                </li>
              ))}
            </ul>
          </div>
        )}
        {f.openingHours && (
          <div>
            <h3 className="serif italic text-xl mb-3">{f.openingHours.title}</h3>
            <p className="text-sm">{f.openingHours.hours1}</p>
            <p className="text-sm">{f.openingHours.hours2}</p>
          </div>
        )}
      </div>
      <div className="border-t border-white/10">
        <div className="max-w-8xl mx-auto px-6 lg:px-12 py-4 text-xs opacity-60">
          © {new Date().getFullYear()} African Art Gallery
        </div>
      </div>
    </footer>
  );
}
