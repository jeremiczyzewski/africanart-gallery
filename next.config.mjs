/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    remotePatterns: [
      { protocol: 'https', hostname: 'images.prismic.io' },
      { protocol: 'https', hostname: 'african-art-gallery.cdn.prismic.io' },
    ],
  },
  // Sveltia CMS pod /admin/ — Next.js inaczej probuje matchowac jako route i zwraca 404
  async rewrites() {
    return [
      { source: '/admin', destination: '/admin/index.html' },
      { source: '/admin/', destination: '/admin/index.html' },
    ];
  },
};
export default nextConfig;
