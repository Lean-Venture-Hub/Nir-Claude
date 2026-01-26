---
name: react-nextjs-development
description: React fundamentals, hooks (useState, useEffect, useContext, custom hooks), Next.js App Router, Server Components, server actions, routing, data fetching, and React best practices. Use when building React applications, Next.js projects, or implementing React patterns.
---

# React & Next.js Development

Modern React and Next.js patterns for building scalable applications.

## 1. React Hooks Essentials

### useState
```typescript
import { useState } from 'react';

function Counter() {
  const [count, setCount] = useState(0);
  const [user, setUser] = useState({ name: '', email: '' });
  
  // Functional updates
  const increment = () => setCount(prev => prev + 1);
  
  return (
    <button onClick={increment}>
      Count: {count}
    </button>
  );
}
```

### useEffect
```typescript
import { useEffect, useState } from 'react';

function UserProfile({ userId }: { userId: string }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    let cancelled = false;
    
    async function fetchUser() {
      try {
        const response = await fetch(`/api/users/${userId}`);
        const data = await response.json();
        if (!cancelled) {
          setUser(data);
          setLoading(false);
        }
      } catch (error) {
        if (!cancelled) {
          console.error(error);
          setLoading(false);
        }
      }
    }
    
    fetchUser();
    
    // Cleanup function
    return () => {
      cancelled = true;
    };
  }, [userId]); // Dependency array
  
  if (loading) return <div>Loading...</div>;
  return <div>{user?.name}</div>;
}
```

### useContext
```typescript
import { createContext, useContext, useState } from 'react';

const ThemeContext = createContext({ theme: 'light', toggleTheme: () => {} });

function ThemeProvider({ children }) {
  const [theme, setTheme] = useState('light');
  
  const toggleTheme = () => {
    setTheme(prev => prev === 'light' ? 'dark' : 'light');
  };
  
  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

// Using the context
function ThemedButton() {
  const { theme, toggleTheme } = useContext(ThemeContext);
  return <button onClick={toggleTheme}>{theme}</button>;
}
```

### Custom Hooks
```typescript
// useLocalStorage hook
function useLocalStorage<T>(key: string, initialValue: T) {
  const [value, setValue] = useState<T>(() => {
    const stored = localStorage.getItem(key);
    return stored ? JSON.parse(stored) : initialValue;
  });
  
  useEffect(() => {
    localStorage.setItem(key, JSON.stringify(value));
  }, [key, value]);
  
  return [value, setValue] as const;
}

// Usage
function App() {
  const [theme, setTheme] = useLocalStorage('theme', 'light');
  return <div>Theme: {theme}</div>;
}

// useFetch hook
function useFetch<T>(url: string) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);
  
  useEffect(() => {
    fetch(url)
      .then(res => res.json())
      .then(setData)
      .catch(setError)
      .finally(() => setLoading(false));
  }, [url]);
  
  return { data, loading, error };
}
```

## 2. Next.js App Router

### File-based Routing
```
app/
├── page.tsx              # / route
├── about/
│   └── page.tsx          # /about route
├── blog/
│   ├── page.tsx          # /blog route
│   └── [slug]/
│       └── page.tsx      # /blog/[slug] route
└── dashboard/
    ├── layout.tsx        # Shared layout
    └── page.tsx          # /dashboard route
```

### Server Components (Default)
```typescript
// app/blog/page.tsx
async function BlogPage() {
  // Fetch data directly in Server Component
  const posts = await fetch('https://api.example.com/posts')
    .then(res => res.json());
  
  return (
    <div>
      <h1>Blog Posts</h1>
      {posts.map(post => (
        <article key={post.id}>
          <h2>{post.title}</h2>
          <p>{post.excerpt}</p>
        </article>
      ))}
    </div>
  );
}

export default BlogPage;
```

### Client Components
```typescript
'use client'; // Mark as Client Component

import { useState } from 'react';

export function Counter() {
  const [count, setCount] = useState(0);
  
  return (
    <button onClick={() => setCount(count + 1)}>
      Count: {count}
    </button>
  );
}
```

### Server Actions
```typescript
// app/actions.ts
'use server';

import { revalidatePath } from 'next/cache';

export async function createPost(formData: FormData) {
  const title = formData.get('title');
  const content = formData.get('content');
  
  // Save to database
  await db.posts.create({
    data: { title, content }
  });
  
  revalidatePath('/blog');
  return { success: true };
}

// app/new/page.tsx
import { createPost } from '../actions';

export default function NewPost() {
  return (
    <form action={createPost}>
      <input name="title" required />
      <textarea name="content" required />
      <button type="submit">Create Post</button>
    </form>
  );
}
```

### Dynamic Routes
```typescript
// app/blog/[slug]/page.tsx
interface PageProps {
  params: { slug: string };
  searchParams: { [key: string]: string | undefined };
}

export default async function BlogPost({ params }: PageProps) {
  const post = await getPost(params.slug);
  
  return (
    <article>
      <h1>{post.title}</h1>
      <div>{post.content}</div>
    </article>
  );
}

// Generate static paths
export async function generateStaticParams() {
  const posts = await getAllPosts();
  return posts.map(post => ({ slug: post.slug }));
}
```

### Loading & Error States
```typescript
// app/blog/loading.tsx
export default function Loading() {
  return <div>Loading blog posts...</div>;
}

// app/blog/error.tsx
'use client';

export default function Error({
  error,
  reset,
}: {
  error: Error;
  reset: () => void;
}) {
  return (
    <div>
      <h2>Something went wrong!</h2>
      <button onClick={reset}>Try again</button>
    </div>
  );
}
```

### Layouts
```typescript
// app/dashboard/layout.tsx
export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="dashboard">
      <nav>
        <a href="/dashboard">Dashboard</a>
        <a href="/dashboard/settings">Settings</a>
      </nav>
      <main>{children}</main>
    </div>
  );
}
```

## 3. React Patterns

### Compound Components
```typescript
interface TabsProps {
  children: React.ReactNode;
  defaultValue: string;
}

interface TabsContextType {
  activeTab: string;
  setActiveTab: (tab: string) => void;
}

const TabsContext = createContext<TabsContextType | null>(null);

function Tabs({ children, defaultValue }: TabsProps) {
  const [activeTab, setActiveTab] = useState(defaultValue);
  
  return (
    <TabsContext.Provider value={{ activeTab, setActiveTab }}>
      <div className="tabs">{children}</div>
    </TabsContext.Provider>
  );
}

function TabList({ children }: { children: React.ReactNode }) {
  return <div className="tab-list">{children}</div>;
}

function Tab({ value, children }: { value: string; children: React.ReactNode }) {
  const context = useContext(TabsContext);
  const isActive = context?.activeTab === value;
  
  return (
    <button
      className={isActive ? 'tab active' : 'tab'}
      onClick={() => context?.setActiveTab(value)}
    >
      {children}
    </button>
  );
}

function TabPanel({ value, children }: { value: string; children: React.ReactNode }) {
  const context = useContext(TabsContext);
  if (context?.activeTab !== value) return null;
  return <div className="tab-panel">{children}</div>;
}

// Compound export
Tabs.List = TabList;
Tabs.Tab = Tab;
Tabs.Panel = TabPanel;

// Usage
<Tabs defaultValue="tab1">
  <Tabs.List>
    <Tabs.Tab value="tab1">Tab 1</Tabs.Tab>
    <Tabs.Tab value="tab2">Tab 2</Tabs.Tab>
  </Tabs.List>
  <Tabs.Panel value="tab1">Content 1</Tabs.Panel>
  <Tabs.Panel value="tab2">Content 2</Tabs.Panel>
</Tabs>
```

### Render Props
```typescript
interface MousePosition {
  x: number;
  y: number;
}

function MouseTracker({
  render
}: {
  render: (position: MousePosition) => React.ReactNode;
}) {
  const [position, setPosition] = useState({ x: 0, y: 0 });
  
  useEffect(() => {
    const handleMove = (e: MouseEvent) => {
      setPosition({ x: e.clientX, y: e.clientY });
    };
    window.addEventListener('mousemove', handleMove);
    return () => window.removeEventListener('mousemove', handleMove);
  }, []);
  
  return <>{render(position)}</>;
}

// Usage
<MouseTracker
  render={({ x, y }) => (
    <div>Mouse: {x}, {y}</div>
  )}
/>
```

## 4. Performance Optimization

### React.memo
```typescript
const ExpensiveComponent = React.memo(function ExpensiveComponent({
  data
}: {
  data: string;
}) {
  console.log('ExpensiveComponent rendered');
  return <div>{data}</div>;
});
```

### useMemo & useCallback
```typescript
function DataList({ items }: { items: Item[] }) {
  // Memoize expensive computation
  const sortedItems = useMemo(() => {
    return items.sort((a, b) => a.name.localeCompare(b.name));
  }, [items]);
  
  // Memoize callback
  const handleClick = useCallback((id: string) => {
    console.log('Clicked:', id);
  }, []);
  
  return (
    <ul>
      {sortedItems.map(item => (
        <li key={item.id} onClick={() => handleClick(item.id)}>
          {item.name}
        </li>
      ))}
    </ul>
  );
}
```

### Code Splitting
```typescript
import dynamic from 'next/dynamic';

const HeavyComponent = dynamic(() => import('./HeavyComponent'), {
  loading: () => <p>Loading...</p>,
  ssr: false // Disable SSR for this component
});

function Page() {
  return <HeavyComponent />;
}
```

## Best Practices

1. **Server Components by default** - Use 'use client' only when needed
2. **Fetch data close to where it's used** - Colocation in Server Components
3. **Use TypeScript** - Type safety prevents bugs
4. **Composition over inheritance** - Build with small, reusable components
5. **Keep components pure** - Same props = same output
6. **Extract custom hooks** - Reuse stateful logic
7. **Use Next.js conventions** - Follow file-based routing, layouts
8. **Optimize images** - Use next/image component

## Common Pitfalls

❌ Forgetting dependency arrays in useEffect
❌ Mutating state directly
❌ Using index as key in lists
❌ Not cleaning up effects
❌ Overusing useEffect (often not needed)
❌ Client Components when Server Components would work
❌ Not using React.memo where needed
❌ Prop drilling instead of context/composition
