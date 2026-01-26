---
name: ui-interactions-animations
description: Micro-interactions, hover states, transitions, loading states, Framer Motion, GSAP, CSS animations, and delightful UI feedback patterns. Use when adding interactivity, animations, transitions, or improving user feedback.
---

# UI Interactions & Animations

Create delightful, performant animations and interactions.

## 1. CSS Transitions & Transforms

### Basic Transitions
```css
.button {
  background: #3b82f6;
  transform: translateY(0);
  transition: all 0.2s ease;
}

.button:hover {
  background: #2563eb;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
}

.button:active {
  transform: translateY(0);
}
```

### Easing Functions
```css
/* Built-in easings */
.element {
  transition: transform 0.3s ease-in-out;
  /* ease, ease-in, ease-out, ease-in-out, linear */
}

/* Custom cubic-bezier */
.smooth {
  transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
  /* https://cubic-bezier.com for visualization */
}
```

## 2. CSS Keyframe Animations

### Fade In
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

### Loading Spinner
```css
@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #f3f4f6;
  border-top-color: #3b82f6;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}
```

### Pulse Effect
```css
@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

.loading {
  animation: pulse 2s ease-in-out infinite;
}
```

## 3. Framer Motion (React)

### Basic Animation
```typescript
import { motion } from 'framer-motion';

function Card() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      transition={{ duration: 0.3 }}
      className="card"
    >
      Content
    </motion.div>
  );
}
```

### Hover & Tap Animations
```typescript
<motion.button
  whileHover={{ scale: 1.05 }}
  whileTap={{ scale: 0.95 }}
  transition={{ type: "spring", stiffness: 400, damping: 17 }}
>
  Click Me
</motion.button>
```

### Variants
```typescript
const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1
    }
  }
};

const itemVariants = {
  hidden: { opacity: 0, x: -20 },
  visible: { opacity: 1, x: 0 }
};

function List() {
  return (
    <motion.ul
      variants={containerVariants}
      initial="hidden"
      animate="visible"
    >
      {items.map(item => (
        <motion.li key={item.id} variants={itemVariants}>
          {item.name}
        </motion.li>
      ))}
    </motion.ul>
  );
}
```

### Layout Animations
```typescript
<motion.div layout>
  {/* Content that changes size */}
</motion.div>

<motion.div layoutId="shared-element">
  {/* Shared element animations between pages */}
</motion.div>
```

## 4. Micro-Interactions

### Button States
```typescript
function Button({ children, onClick }: ButtonProps) {
  const [isPressed, setIsPressed] = useState(false);
  
  return (
    <motion.button
      onMouseDown={() => setIsPressed(true)}
      onMouseUp={() => setIsPressed(false)}
      animate={{
        scale: isPressed ? 0.95 : 1,
        boxShadow: isPressed
          ? "0 2px 4px rgba(0,0,0,0.1)"
          : "0 4px 12px rgba(0,0,0,0.15)"
      }}
      transition={{ duration: 0.1 }}
      onClick={onClick}
    >
      {children}
    </motion.button>
  );
}
```

### Toggle Switch
```typescript
function Toggle({ checked, onChange }: ToggleProps) {
  return (
    <button
      onClick={() => onChange(!checked)}
      className={`relative w-14 h-8 rounded-full transition-colors ${
        checked ? 'bg-blue-500' : 'bg-gray-300'
      }`}
    >
      <motion.div
        className="absolute top-1 w-6 h-6 bg-white rounded-full"
        animate={{
          left: checked ? '28px' : '4px'
        }}
        transition={{ type: 'spring', stiffness: 500, damping: 30 }}
      />
    </button>
  );
}
```

### Card Flip
```typescript
function FlipCard() {
  const [isFlipped, setIsFlipped] = useState(false);
  
  return (
    <motion.div
      className="card-container"
      animate={{ rotateY: isFlipped ? 180 : 0 }}
      transition={{ duration: 0.6 }}
      style={{ transformStyle: 'preserve-3d' }}
      onClick={() => setIsFlipped(!isFlipped)}
    >
      <div className="card-front">Front</div>
      <div className="card-back" style={{ transform: 'rotateY(180deg)' }}>
        Back
      </div>
    </motion.div>
  );
}
```

## 5. Loading States

### Skeleton Screens
```typescript
function SkeletonCard() {
  return (
    <div className="animate-pulse">
      <div className="h-48 bg-gray-200 rounded-lg mb-4" />
      <div className="h-4 bg-gray-200 rounded w-3/4 mb-2" />
      <div className="h-4 bg-gray-200 rounded w-1/2" />
    </div>
  );
}
```

### Progress Indicators
```typescript
function ProgressBar({ progress }: { progress: number }) {
  return (
    <div className="w-full bg-gray-200 rounded-full h-2">
      <motion.div
        className="bg-blue-500 h-2 rounded-full"
        initial={{ width: 0 }}
        animate={{ width: `${progress}%` }}
        transition={{ duration: 0.3 }}
      />
    </div>
  );
}
```

## 6. Page Transitions

### Route Animations
```typescript
import { AnimatePresence, motion } from 'framer-motion';

function App() {
  return (
    <AnimatePresence mode="wait">
      <Routes>
        <Route
          path="/"
          element={
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: 20 }}
              transition={{ duration: 0.3 }}
            >
              <HomePage />
            </motion.div>
          }
        />
      </Routes>
    </AnimatePresence>
  );
}
```

## 7. Scroll Animations

### Intersection Observer
```typescript
function ScrollReveal({ children }: { children: React.ReactNode }) {
  const ref = useRef(null);
  const isInView = useInView(ref, { once: true });
  
  return (
    <motion.div
      ref={ref}
      initial={{ opacity: 0, y: 50 }}
      animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 50 }}
      transition={{ duration: 0.5 }}
    >
      {children}
    </motion.div>
  );
}
```

## Best Practices

1. **Performance first** - Use transforms and opacity (GPU-accelerated)
2. **Meaningful motion** - Every animation serves a purpose
3. **Respect reduced motion** - Check prefers-reduced-motion
4. **Keep it subtle** - Less is more with animations
5. **Consistent easing** - Use same easing functions
6. **60fps target** - Smooth animations are crucial
7. **Loading feedback** - Always show something is happening
8. **Natural timing** - Real-world physics feels better
