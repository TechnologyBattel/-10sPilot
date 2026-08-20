import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  transpilePackages: ['@10spilot/core', '@10spilot/ai'],
  typedRoutes: true,
};

export default nextConfig;
