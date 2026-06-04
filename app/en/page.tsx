import HeroCarousel from '@/components/HeroCarousel';
import { getHomeHero } from '@/lib/content';

export default function EnHomePage() {
  const hero = getHomeHero('en-us');
  if (!hero) return <div className="p-12">No homepage content.</div>;

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
      buttonSlug={`en/${hero.buttonSlug}`}
    />
  );
}
