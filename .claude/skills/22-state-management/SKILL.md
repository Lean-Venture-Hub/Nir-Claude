---
name: state-management
description: React state patterns (useState, useReducer, useContext), Redux Toolkit, Zustand, Tanstack Query for server state, and state management best practices. Use when managing application state, handling complex state logic, or integrating server data.
---

# State Management

Master client and server state management patterns.

## 1. React State Basics

### useState
```typescript
const [count, setCount] = useState(0);
const [user, setUser] = useState<User | null>(null);

// Functional updates
setCount(prev => prev + 1);
```

### useReducer
```typescript
type State = { count: number; step: number };
type Action = { type: 'increment' } | { type: 'decrement' } | { type: 'setStep'; step: number };

function reducer(state: State, action: Action): State {
  switch (action.type) {
    case 'increment':
      return { ...state, count: state.count + state.step };
    case 'decrement':
      return { ...state, count: state.count - state.step };
    case 'setStep':
      return { ...state, step: action.step };
    default:
      return state;
  }
}

function Counter() {
  const [state, dispatch] = useReducer(reducer, { count: 0, step: 1 });
  return (
    <div>
      <p>Count: {state.count}</p>
      <button onClick={() => dispatch({ type: 'increment' })}>+</button>
    </div>
  );
}
```

## 2. Zustand (Lightweight State)

```typescript
import { create } from 'zustand';

interface BearStore {
  bears: number;
  increase: () => void;
  reset: () => void;
}

const useBearStore = create<BearStore>((set) => ({
  bears: 0,
  increase: () => set((state) => ({ bears: state.bears + 1 })),
  reset: () => set({ bears: 0 })
}));

// Usage
function BearCounter() {
  const bears = useBearStore((state) => state.bears);
  const increase = useBearStore((state) => state.increase);
  return <button onClick={increase}>Bears: {bears}</button>;
}
```

## 3. Redux Toolkit

```typescript
import { createSlice, configureStore } from '@reduxjs/toolkit';

const counterSlice = createSlice({
  name: 'counter',
  initialState: { value: 0 },
  reducers: {
    increment: (state) => { state.value += 1; },
    decrement: (state) => { state.value -= 1; },
    incrementByAmount: (state, action) => { state.value += action.payload; }
  }
});

export const { increment, decrement, incrementByAmount } = counterSlice.actions;

const store = configureStore({
  reducer: { counter: counterSlice.reducer }
});

// Usage
import { useSelector, useDispatch } from 'react-redux';

function Counter() {
  const count = useSelector((state) => state.counter.value);
  const dispatch = useDispatch();
  return <button onClick={() => dispatch(increment())}>{count}</button>;
}
```

## 4. Tanstack Query (Server State)

```typescript
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

// Fetching data
function Posts() {
  const { data, isLoading, error } = useQuery({
    queryKey: ['posts'],
    queryFn: () => fetch('/api/posts').then(res => res.json())
  });
  
  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;
  
  return <div>{data.map(post => <Post key={post.id} {...post} />)}</div>;
}

// Mutations
function CreatePost() {
  const queryClient = useQueryClient();
  
  const mutation = useMutation({
    mutationFn: (newPost) => fetch('/api/posts', {
      method: 'POST',
      body: JSON.stringify(newPost)
    }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['posts'] });
    }
  });
  
  return <button onClick={() => mutation.mutate({ title: 'New Post' })}>
    Create Post
  </button>;
}
```

## Best Practices

1. **Local state first** - Use useState for component-specific state
2. **Lift state up** - Share state by lifting to common ancestor
3. **Context for global state** - Theme, auth, etc.
4. **Zustand for client state** - Simpler than Redux for most cases
5. **Tanstack Query for server state** - Caching, refetching, mutations
6. **Avoid prop drilling** - Use composition or context
7. **Immutable updates** - Never mutate state directly (except Redux Toolkit)
8. **Normalize data** - Store entities by ID for easy updates
