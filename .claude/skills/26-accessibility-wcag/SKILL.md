---
name: accessibility-wcag
description: WCAG 2.1 Level AA compliance, ARIA patterns, keyboard navigation, screen reader support, and accessible forms. Use when ensuring accessibility, implementing ARIA, supporting keyboard users, or meeting compliance standards.
---

# Accessibility & WCAG Compliance

Build inclusive interfaces that work for everyone.

## 1. Semantic HTML

```html
<!-- ✅ Good: Semantic structure -->
<header>
  <nav aria-label="Main navigation">
    <ul>
      <li><a href="/">Home</a></li>
    </ul>
  </nav>
</header>

<main>
  <article>
    <h1>Article Title</h1>
    <p>Content...</p>
  </article>
</main>

<!-- ❌ Bad: Div soup -->
<div class="header">
  <div class="nav">
    <div class="link">Home</div>
  </div>
</div>
```

## 2. ARIA Patterns

```html
<!-- Button (if not using <button>) -->
<div role="button" tabindex="0" aria-label="Close dialog" 
     onclick="close()" onkeypress="handleKey(event)">
  ×
</div>

<!-- Dialog/Modal -->
<div role="dialog" aria-labelledby="dialog-title" aria-modal="true">
  <h2 id="dialog-title">Confirm Action</h2>
  <p>Are you sure?</p>
  <button>Yes</button>
  <button>No</button>
</div>

<!-- Tab Panel -->
<div role="tablist">
  <button role="tab" aria-selected="true" aria-controls="panel-1">Tab 1</button>
  <button role="tab" aria-selected="false" aria-controls="panel-2">Tab 2</button>
</div>
<div role="tabpanel" id="panel-1">Content 1</div>
<div role="tabpanel" id="panel-2" hidden>Content 2</div>
```

## 3. Keyboard Navigation

```typescript
function Dialog({ isOpen, onClose }: DialogProps) {
  const dialogRef = useRef<HTMLDivElement>(null);
  
  useEffect(() => {
    if (!isOpen) return;
    
    // Focus first focusable element
    const firstFocusable = dialogRef.current?.querySelector(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
    (firstFocusable as HTMLElement)?.focus();
    
    // Trap focus inside dialog
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
      if (e.key === 'Tab') {
        // Trap focus logic
      }
    };
    
    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onClose]);
  
  return <div ref={dialogRef} role="dialog">{/* ... */}</div>;
}
```

## 4. Color Contrast

```css
/* WCAG AA: Minimum 4.5:1 for normal text */
.text-normal {
  color: #1a1a1a; /* Against white: 16.1:1 ✅ */
  background: #ffffff;
}

/* WCAG AA: Minimum 3:1 for large text (18px+ or 14px+ bold) */
.text-large {
  font-size: 18px;
  color: #595959; /* Against white: 7.0:1 ✅ */
  background: #ffffff;
}

/* ❌ Fails WCAG AA */
.text-poor-contrast {
  color: #999999; /* Against white: 2.8:1 ❌ */
  background: #ffffff;
}
```

## 5. Screen Reader Support

```typescript
// Live regions for dynamic updates
function Notification({ message }: { message: string }) {
  return (
    <div
      role="status"
      aria-live="polite"
      aria-atomic="true"
    >
      {message}
    </div>
  );
}

// Skip links
function Header() {
  return (
    <>
      <a href="#main-content" className="skip-link">
        Skip to main content
      </a>
      <nav>{/* Navigation */}</nav>
    </>
  );
}
```

## 6. Accessible Forms

```html
<form>
  <!-- Always use labels -->
  <label for="email">Email address</label>
  <input
    type="email"
    id="email"
    name="email"
    required
    aria-required="true"
    aria-describedby="email-hint"
  />
  <span id="email-hint">We'll never share your email</span>
  
  <!-- Error messages -->
  <span id="email-error" role="alert" aria-live="assertive">
    Please enter a valid email
  </span>
</form>
```

## Best Practices

1. **Semantic HTML first** - Use correct elements
2. **Keyboard accessible** - All interactions work with keyboard
3. **Color contrast** - Meet WCAG AA minimum (4.5:1)
4. **Alt text** - Descriptive text for all images
5. **Focus management** - Visible focus indicators, logical order
6. **ARIA when needed** - Enhance, don't replace semantics
7. **Test with screen readers** - NVDA, JAWS, VoiceOver
8. **Automated testing** - axe, Lighthouse, eslint-plugin-jsx-a11y
