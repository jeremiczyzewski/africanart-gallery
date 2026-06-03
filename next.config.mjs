/** @type {import('next').NextConfig} */
const nextConfig = {
  // Static export do GitHub Pages — kazda strona jako pre-rendered HTML
  output: 'export',
  // Wymaga `unoptimized: true` przy `output: 'export'` (brak runtime do resize obrazow)
  images: {
    unoptimized: true,
    remotePatterns: [
      { protocol: 'https', hostname: 'images.prismic.io' },
      { protocol: 'https', hostname: 'african-art-gallery.cdn.prismic.io' },
    ],
  },
  // GitHub Pages oczekuje URLi z trailing slash (folder/index.html)
  trailingSlash: true,
};
export default nextConfig;
