---
name: css-styling-systems
description: Modern CSS techniques, Tailwind CSS utility-first approach, CSS architecture (BEM, CSS Modules), responsive design patterns, and CSS animations. Use when styling components, implementing responsive layouts, using Tailwind, or creating animations.
---

# CSS & Styling Systems

Master modern CSS and utility-first styling with Tailwind.

## 1. Tailwind CSS Essentials

### Basic Utilities
```html
<!-- Layout -->
<div class="flex items-center justify-between gap-4">
  <div class="w-full md:w-1/2 lg:w-1/3"></div>
</div>

<!-- Spacing (4px increments) -->
<div class="p-4 m-2 mx-auto my-8">
  <div class="space-y-4"><!-- Vertical spacing between children --></div>
</div>

<!-- Typography -->
<h1 class="text-4xl font-bold text-gray-900 dark:text-white">
  Title
</h1>
<p class="text-base leading-relaxed text-gray-600">
  Paragraph text
</p>

<!-- Colors -->
<button class="bg-blue-500 hover:bg-blue-700 text-white">
  Button
</button>
```

### Responsive Design
```html
<!-- Mobile-first breakpoints: sm, md, lg, xl, 2xl -->
<div class="text-sm md:text-base lg:text-lg">
  <!-- Small on mobile, larger on desktop -->
</div>

<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  <!-- 1 column on mobile, 2 on tablet, 3 on desktop -->
</div>
```

### Custom Configuration
```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#f0f9ff',
          500: '#0ea5e9',
          900: '#0c4a6e',
        }
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
      spacing: {
        '128': '32rem',
      }
    }
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ]
}
```

## 2. CSS Modules

```css
/* styles.module.css */
.container {
  max-width: 1200px;
  margin: 0 auto;
}

.card {
  border: 1px solid var(--border-color);
  border-radius: 8px;
}

.card:hover {
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}
```

```typescript
// Component.tsx
import styles from './styles.module.css';

export function Card() {
  return (
    <div className={styles.card}>
      <h2>Title</h2>
    </div>
  );
}
```

## 3. CSS Animations

### Transitions
```css
.button {
  background: blue;
  transition: all 0.3s ease;
}

.button:hover {
  background: darkblue;
  transform: translateY(-2px);
}
```

### Keyframe Animations
```css
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.card {
  animation: fadeIn 0.5s ease-out;
}
```

### Tailwind Animations
```html
<div class="animate-spin">Loading...</div>
<div class="animate-pulse">Skeleton</div>
<div class="animate-bounce">Bounce</div>

<!-- Custom animation -->
<div class="animate-fade-in"><!-- Custom defined in config --></div>
```

## 4. Responsive Patterns

### Mobile-First Approach
```css
/* Base (mobile) styles */
.container {
  padding: 1rem;
}

/* Tablet and up */
@media (min-width: 768px) {
  .container {
    padding: 2rem;
  }
}

/* Desktop */
@media (min-width: 1024px) {
  .container {
    padding: 3rem;
  }
}
```

### Container Queries
```css
.card-container {
  container-type: inline-size;
}

@container (min-width: 400px) {
  .card {
    display: grid;
    grid-template-columns: 1fr 2fr;
  }
}
```

## Best Practices

1. **Mobile-first** - Design for mobile, enhance for desktop
2. **Use Tailwind utilities** - Faster than writing custom CSS
3. **Custom properties for theming** - Easy dark mode
4. **Semantic class names** - When using CSS modules
5. **Avoid !important** - Indicates architecture problems
6. **Group related utilities** - Use @apply sparingly in Tailwind
7. **Responsive typography** - Use clamp() for fluid type
8. **Performance** - Minimize unused CSS, tree-shake Tailwind
