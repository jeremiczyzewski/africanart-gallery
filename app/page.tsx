import HeroCarousel from '@/components/HeroCarousel';
import { getHomeHero } from '@/lib/content';

export default function HomePage() {
  const hero = getHomeHero('pl');
  if (!hero) return <div className="p-12">Brak treści homepage.</div>;

  // Karuzela: jesli sa photos uzywamy ich, inaczej fallback na backgroundImage
  const photos =
    hero.photos.length > 0
      ? hero.photos
      : hero.backgroundImage
        ? [{ url: hero.backgroundImage, alt: hero.backgroundAlt }]
        : [];

  return (
    <HeroCarousel
      photos={photos}
      title={hero.title}
      buttonText={hero.buttonText}
      buttonSlug={hero.buttonSlug}
    />
  );
}
