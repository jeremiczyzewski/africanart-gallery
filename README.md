# African Art Gallery

Klon strony [african-art-gallery.netlify.app](https://african-art-gallery.netlify.app/) — Next.js 14 + Tailwind + treści w plikach markdown / JSON edytowanych przez Sveltia CMS (panel w przeglądarce dla osoby nietechnicznej).

## Stack

- **Next.js 14** (App Router, SSG)
- **Tailwind CSS**
- **Sveltia CMS** pod `/admin/` — darmowy edytor w przeglądarce, commit do Git, GitHub OAuth login
- **Cormorant Garamond** + **Inter** (Google Fonts)
- **Hosting**: Netlify (auto-deploy z gałęzi `main`)

## Lokalny rozwój

```bash
npm install
npm run dev    # http://localhost:3700
```

Panel CMS pod `/admin/index.html` (lokalnie) lub `/admin/` (na produkcji).

## Struktura

```
content/
├── exhibits/          # 21 eksponatów (markdown z frontmatter)
│   └── {slug}_pl.md
├── pages/             # strony statyczne (JSON Prismic slices)
└── settings/          # footer, nav, social (JSON)

public/
├── assets/            # logo SVG, ikony social, strzałki
├── uploads/
│   ├── images/        # zdjęcia eksponatów + slidery
│   └── pdfs/          # dokumentacje
└── admin/             # Sveltia CMS (index.html + config.yml)

components/            # Header, Footer, HeroCarousel, RichText, SliceRenderer
app/                   # routing: /, /gallery, /gallery/[slug], /o-galerii, /tworcy-galerii, /kontakt
lib/content.ts         # czytanie markdownów + JSONów
prismic-export/        # extract.py — bulk-import z Prismic (jednorazowy)
```

## Deploy na Netlify (instrukcja dla początkującego)

1. **Stwórz repo na GitHub** (private lub public — bez znaczenia):
   ```bash
   gh repo create africanart-gallery --private --source=. --remote=origin --push
   ```

2. **Połącz z Netlify**:
   - Wejdź na [app.netlify.com](https://app.netlify.com/)
   - "Add new site" → "Import existing project" → wybierz GitHub repo
   - Build settings są już w `netlify.toml`, klikasz "Deploy"
   - Po 2-3 minutach strona jest live pod `https://<random-name>.netlify.app`

3. **Podepnij własną domenę** (np. `africanart.gallery`):
   - W Netlify: Domain management → "Add custom domain"
   - W panelu rejestratora domeny: dodaj rekordy DNS pokazane przez Netlify (zazwyczaj `A` + `CNAME`)
   - SSL certyfikat załatwia Netlify automatycznie (~10 min)

4. **Skonfiguruj Sveltia CMS** (panel dla osoby nietechnicznej):
   - W repo na GitHub: Settings → Developer settings → OAuth Apps → "New OAuth App"
     - Homepage URL: `https://<twoja-strona>.netlify.app`
     - Callback URL: `https://api.netlify.com/auth/done`
   - W Netlify: Site settings → Access control → OAuth → "Install provider" → GitHub, wklej Client ID + Client Secret
   - Otwórz `public/admin/config.yml` w repo → zmień `YOUR_GITHUB_USERNAME/africanart-gallery` na realny `<user>/<repo>`
   - Commit + Netlify zrobi rebuild
   - Teraz znajomy wchodzi na `https://<twoja-strona>.netlify.app/admin/`, klika "Login with GitHub" (raz), i edytuje eksponaty

## Bulk-import eksponatów (gdy dojdą nowe PDFy)

```bash
# Wrzuć PDF do prismic-export/source/
# Wrzuć zdjęcia do prismic-export/source-photos/
python prismic-export/extract.py  # generuje content/exhibits/<slug>_pl.md + kopiuje pliki
git add content public
git commit -m "Add 30 nowych eksponatów"
git push   # Netlify auto-deploy
```

## Co zostało do zrobienia

- [ ] Search bar w headerze — działająca wyszukiwarka po nazwach eksponatów
- [ ] Przełącznik PL/EN — dane są w Prismic API (`en-us`), wystarczy dorobić `[lang]` route
- [ ] Strona 404 z linkiem do galerii
- [ ] Sitemap + robots.txt
- [ ] Open Graph image dla każdego eksponatu

Wszystkie te dodatki są kompatybilne z obecną architekturą i nie wymagają refactoru.
