---
name: performance-optimization
description: Web Vitals optimization (LCP, FID, CLS), code splitting, bundle optimization, image optimization, caching strategies, and performance monitoring. Use when optimizing load times, improving Core Web Vitals, or reducing bundle size.
---

# Performance Optimization

Build fast, efficient web applications.

## 1. Core Web Vitals

### LCP (Largest Contentful Paint) - Target: <2.5s
```typescript
// Optimize images
<Image
  src="/hero.jpg"
  alt="Hero"
  priority // Load immediately
  width={1200}
  height={600}
/>

// Preload critical resources
<link rel="preload" href="/font.woff2" as="font" type="font/woff2" crossorigin />
```

### FID (First Input Delay) - Target: <100ms
```typescript
// Code split heavy components
const HeavyChart = dynamic(() => import('./HeavyChart'), {
  loading: () => <Skeleton />,
  ssr: false
});

// Debounce expensive operations
const debouncedSearch = useMemo(
  () => debounce((query) => search(query), 300),
  []
);
```

### CLS (Cumulative Layout Shift) - Target: <0.1
```html
<!-- Always specify dimensions -->
<img src="image.jpg" width="800" height="600" alt="" />

<!-- Reserve space for dynamic content -->
<div style="min-height: 400px">
  {loading ? <Skeleton /> : <Content />}
</div>
```

## 2. Code Splitting

```typescript
// Route-based splitting (Next.js automatic)
// pages/about.tsx - auto code-split

// Component-based splitting
const Modal = dynamic(() => import('./Modal'));
const Chart = dynamic(() => import('./Chart'), { ssr: false });

// Conditional loading
function Page() {
  const [showModal, setShowModal] = useState(false);
  
  return (
    <>
      <button onClick={() => setShowModal(true)}>Open</button>
      {showModal && <Modal />} {/* Only loads when needed */}
    </>
  );
}
```

## 3. Bundle Optimization

```javascript
// next.config.js
module.exports = {
  compiler: {
    removeConsole: process.env.NODE_ENV === 'production'
  },
  webpack: (config) => {
    // Analyze bundle
    if (process.env.ANALYZE) {
      const { BundleAnalyzerPlugin } = require('webpack-bundle-analyzer');
      config.plugins.push(new BundleAnalyzerPlugin());
    }
    return config;
  }
};

// Tree-shaking: Import only what you need
import { Button } from '@/components'; // ❌ Imports entire library
import Button from '@/components/Button'; // ✅ Imports only Button
```

## 4. Image Optimization

```typescript
// Next.js Image component
<Image
  src="/photo.jpg"
  alt="Description"
  width={800}
  height={600}
  quality={85} // 75-85 optimal
  placeholder="blur"
  blurDataURL="data:image/..."
/>

// Lazy loading
<img src="image.jpg" loading="lazy" alt="" />

// Responsive images
<picture>
  <source srcset="image-large.webp" media="(min-width: 1024px)" type="image/webp" />
  <source srcset="image-small.webp" type="image/webp" />
  <img src="image.jpg" alt="" />
</picture>
```

## 5. Caching Strategies

```typescript
// SWR pattern with Tanstack Query
const { data } = useQuery({
  queryKey: ['user', userId],
  queryFn: () => fetchUser(userId),
  staleTime: 5 * 60 * 1000, // Consider fresh for 5 minutes
  cacheTime: 10 * 60 * 1000 // Keep in cache for 10 minutes
});

// Service Worker caching (Next.js)
// public/sw.js
self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request).then((response) => {
      return response || fetch(event.request);
    })
  );
});
```

## 6. React Performance

```typescript
// Memoization
const ExpensiveComponent = memo(function ExpensiveComponent({ data }) {
  return <div>{/* expensive render */}</div>;
});

// useMemo for expensive computations
const sorted = useMemo(() => {
  return items.sort((a, b) => a.name.localeCompare(b.name));
}, [items]);

// useCallback for stable function references
const handleClick = useCallback((id) => {
  doSomething(id);
}, []);

// Virtual scrolling for long lists
import { useVirtualizer } from '@tanstack/react-virtual';

function LongList({ items }) {
  const virtualizer = useVirtualizer({
    count: items.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 50
  });
  
  return <div>{virtualizer.getVirtualItems().map(/* ... */)}</div>;
}
```

## Best Practices

1. **Measure first** - Use Lighthouse, Web Vitals
2. **Optimize images** - WebP format, lazy loading, sizing
3. **Code split** - Route and component level
4. **Minimize JavaScript** - Ship less code
5. **Use CDN** - For static assets
6. **Compress assets** - Gzip/Brotli
7. **Monitor performance** - Real User Monitoring (RUM)
8. **Lazy load non-critical** - Load what's needed when needed
