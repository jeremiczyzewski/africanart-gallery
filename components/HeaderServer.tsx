import { getNavigation, getSocial } from '@/lib/content';
import Header from './Header';

export default function HeaderServer({ lang = 'pl' }: { lang?: 'pl' | 'en-us' }) {
  const nav = getNavigation(lang);
  const social = getSocial(lang);
  return <Header nav={nav} social={social} lang={lang} />;
}
