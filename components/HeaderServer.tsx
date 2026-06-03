import { getNavigation, getSocial } from '@/lib/content';
import Header from './Header';

export default function HeaderServer() {
  const nav = getNavigation('pl');
  const social = getSocial('pl');
  return <Header nav={nav} social={social} />;
}
