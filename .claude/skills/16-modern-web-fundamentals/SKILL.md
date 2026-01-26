---
name: modern-web-fundamentals
description: HTML5 semantic markup, modern CSS3 (Grid, Flexbox, custom properties), JavaScript ES6+ features, TypeScript basics, and web platform APIs. Use when building any web interface, writing semantic HTML, using modern CSS features, or working with vanilla JavaScript/TypeScript fundamentals.
---

# Modern Web Fundamentals

Master the core building blocks of modern web development.

## 1. Semantic HTML5

**Semantic Elements:**
```html
<!-- Page Structure -->
<header>
  <nav>
    <ul>
      <li><a href="/">Home</a></li>
    </ul>
  </nav>
</header>

<main>
  <article>
    <h1>Article Title</h1>
    <section>
      <h2>Section Heading</h2>
      <p>Content...</p>
    </section>
  </article>
  
  <aside>
    <h2>Related Links</h2>
  </aside>
</main>

<footer>
  <p>&copy; 2024 Company</p>
</footer>
```

**Form Elements:**
```html
<form>
  <label for="email">Email:</label>
  <input type="email" id="email" name="email" required />
  
  <label for="date">Date:</label>
  <input type="date" id="date" name="date" />
  
  <label for="quantity">Quantity:</label>
  <input type="number" id="quantity" min="1" max="10" />
  
  <button type="submit">Submit</button>
</form>
```

**Media Elements:**
```html
<figure>
  <img src="image.jpg" alt="Descriptive alt text" loading="lazy" />
  <figcaption>Image caption</figcaption>
</figure>

<video controls width="640">
  <source src="video.mp4" type="video/mp4" />
  <track kind="captions" src="captions.vtt" />
</video>
```

## 2. Modern CSS3

### CSS Grid
```css
.container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
}

/* Named Grid Areas */
.layout {
  display: grid;
  grid-template-areas:
    "header header header"
    "sidebar main main"
    "footer footer footer";
  grid-template-columns: 200px 1fr 1fr;
  gap: 1rem;
}

.header { grid-area: header; }
.sidebar { grid-area: sidebar; }
.main { grid-area: main; }
.footer { grid-area: footer; }
```

### Flexbox
```css
.flex-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
}

.flex-item {
  flex: 1 1 300px; /* grow shrink basis */
}
```

### CSS Custom Properties (Variables)
```css
:root {
  --color-primary: #3b82f6;
  --color-secondary: #8b5cf6;
  --spacing-unit: 8px;
  --font-size-base: 16px;
  --border-radius: 8px;
}

.button {
  background: var(--color-primary);
  padding: calc(var(--spacing-unit) * 2);
  border-radius: var(--border-radius);
  font-size: var(--font-size-base);
}

/* Dark mode */
@media (prefers-color-scheme: dark) {
  :root {
    --color-primary: #60a5fa;
  }
}
```

### Modern CSS Features
```css
/* Container Queries */
@container (min-width: 400px) {
  .card { 
    display: grid;
    grid-template-columns: 1fr 2fr;
  }
}

/* :has() Selector */
.card:has(img) {
  display: grid;
}

/* Nesting (native CSS) */
.card {
  padding: 1rem;
  
  & h2 {
    margin-top: 0;
  }
  
  &:hover {
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  }
}

/* Logical Properties */
.element {
  margin-inline: auto; /* left and right in LTR */
  padding-block: 2rem; /* top and bottom */
  border-inline-start: 2px solid; /* left in LTR, right in RTL */
}
```

## 3. Modern JavaScript (ES6+)

### Variables & Destructuring
```javascript
// const and let (no var)
const API_URL = 'https://api.example.com';
let counter = 0;

// Destructuring
const user = { name: 'Alice', age: 30, email: 'alice@example.com' };
const { name, email } = user;

const colors = ['red', 'green', 'blue'];
const [first, second, ...rest] = colors;

// Default parameters
function greet(name = 'Guest') {
  return `Hello, ${name}!`;
}
```

### Arrow Functions
```javascript
// Arrow function syntax
const add = (a, b) => a + b;

const multiply = (a, b) => {
  const result = a * b;
  return result;
};

// Array methods
const numbers = [1, 2, 3, 4, 5];
const doubled = numbers.map(n => n * 2);
const evens = numbers.filter(n => n % 2 === 0);
const sum = numbers.reduce((acc, n) => acc + n, 0);
```

### Template Literals
```javascript
const name = 'Alice';
const age = 30;

// Template strings
const message = `Hello, ${name}! You are ${age} years old.`;

// Multi-line strings
const html = `
  <div class="card">
    <h2>${name}</h2>
    <p>Age: ${age}</p>
  </div>
`;
```

### Async/Await
```javascript
// Async/await (modern async pattern)
async function fetchUser(id) {
  try {
    const response = await fetch(`/api/users/${id}`);
    if (!response.ok) throw new Error('User not found');
    const user = await response.json();
    return user;
  } catch (error) {
    console.error('Error:', error);
    throw error;
  }
}

// Parallel requests
async function fetchMultiple() {
  const [users, posts] = await Promise.all([
    fetch('/api/users').then(r => r.json()),
    fetch('/api/posts').then(r => r.json())
  ]);
  return { users, posts };
}
```

### Modules
```javascript
// Export
export const API_KEY = 'abc123';
export function formatDate(date) { /*...*/ }
export default class User { /*...*/ }

// Import
import User, { API_KEY, formatDate } from './user.js';
import * as utils from './utils.js';
```

### Modern Array/Object Methods
```javascript
// Array methods
const users = [
  { id: 1, name: 'Alice', active: true },
  { id: 2, name: 'Bob', active: false }
];

const activeUser = users.find(u => u.active);
const hasInactive = users.some(u => !u.active);
const allActive = users.every(u => u.active);

// Object methods
const obj1 = { a: 1, b: 2 };
const obj2 = { b: 3, c: 4 };
const merged = { ...obj1, ...obj2 }; // { a: 1, b: 3, c: 4 }

const entries = Object.entries(obj1); // [['a', 1], ['b', 2]]
const fromEntries = Object.fromEntries(entries);
```

## 4. TypeScript Basics

### Type Annotations
```typescript
// Basic types
let name: string = 'Alice';
let age: number = 30;
let isActive: boolean = true;
let tags: string[] = ['typescript', 'react'];

// Object types
interface User {
  id: number;
  name: string;
  email: string;
  age?: number; // optional
}

const user: User = {
  id: 1,
  name: 'Alice',
  email: 'alice@example.com'
};

// Function types
function greet(name: string): string {
  return `Hello, ${name}!`;
}

const add = (a: number, b: number): number => a + b;

// Union types
type Status = 'pending' | 'approved' | 'rejected';
let status: Status = 'pending';

// Type alias
type ID = string | number;
let userId: ID = '123';
```

### Interfaces & Types
```typescript
interface Product {
  id: string;
  name: string;
  price: number;
  category: string;
}

type CartItem = Product & {
  quantity: number;
};

// Generics
function getFirst<T>(items: T[]): T | undefined {
  return items[0];
}

const firstNumber = getFirst([1, 2, 3]); // type: number | undefined
const firstName = getFirst(['a', 'b']); // type: string | undefined
```

## 5. Web Platform APIs

### Fetch API
```javascript
// GET request
const response = await fetch('/api/users');
const users = await response.json();

// POST request
const newUser = { name: 'Alice', email: 'alice@example.com' };
const response = await fetch('/api/users', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(newUser)
});
```

### LocalStorage & SessionStorage
```javascript
// LocalStorage (persists)
localStorage.setItem('theme', 'dark');
const theme = localStorage.getItem('theme');
localStorage.removeItem('theme');

// SessionStorage (session only)
sessionStorage.setItem('token', 'abc123');

// Store objects
const user = { name: 'Alice', id: 1 };
localStorage.setItem('user', JSON.stringify(user));
const stored = JSON.parse(localStorage.getItem('user'));
```

### Intersection Observer
```javascript
// Lazy loading images
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const img = entry.target;
      img.src = img.dataset.src;
      observer.unobserve(img);
    }
  });
});

document.querySelectorAll('img[data-src]').forEach(img => {
  observer.observe(img);
});
```

### Web Components Basics
```javascript
class MyButton extends HTMLElement {
  connectedCallback() {
    this.innerHTML = `<button>${this.textContent}</button>`;
    this.querySelector('button').addEventListener('click', () => {
      this.dispatchEvent(new CustomEvent('myclick'));
    });
  }
}

customElements.define('my-button', MyButton);

// Usage: <my-button>Click me</my-button>
```

## Best Practices

1. **Always use semantic HTML** - Helps SEO and accessibility
2. **Mobile-first CSS** - Design for mobile, enhance for desktop
3. **Avoid inline styles** - Use classes and external CSS
4. **Use const by default** - Only use let when you need to reassign
5. **Async/await over callbacks** - More readable async code
6. **Type your JavaScript** - Use TypeScript or JSDoc
7. **Modern CSS over JS** - Use CSS for animations, layout
8. **Web standards first** - Use platform APIs before libraries

## Common Pitfalls

❌ Using `var` instead of `const`/`let`
❌ Non-semantic divs everywhere (`<div>` soup)
❌ Forgetting alt text on images
❌ Not handling async errors
❌ Using `==` instead of `===`
❌ Mutating objects/arrays directly
❌ Not using CSS custom properties
❌ Ignoring browser compatibility
