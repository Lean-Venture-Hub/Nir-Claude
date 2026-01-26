---
name: advanced-ui-patterns
description: Advanced patterns like infinite scroll, drag-and-drop, virtualization, modals, portals, toast notifications, and complex interactions. Use when implementing advanced UI features, optimizing long lists, or creating rich interactions.
---

# Advanced UI Patterns

Implement sophisticated user interface patterns.

## 1. Infinite Scroll

```typescript
import { useInfiniteQuery } from '@tanstack/react-query';
import { useInView } from 'react-intersection-observer';

function InfiniteScroll() {
  const { ref, inView } = useInView();
  
  const {
    data,
    fetchNextPage,
    hasNextPage,
    isFetchingNextPage
  } = useInfiniteQuery({
    queryKey: ['posts'],
    queryFn: ({ pageParam = 0 }) => fetchPosts(pageParam),
    getNextPageParam: (lastPage, pages) => lastPage.nextCursor
  });
  
  useEffect(() => {
    if (inView && hasNextPage) {
      fetchNextPage();
    }
  }, [inView, hasNextPage, fetchNextPage]);
  
  return (
    <div>
      {data?.pages.map(page =>
        page.items.map(item => <Item key={item.id} {...item} />)
      )}
      <div ref={ref}>
        {isFetchingNextPage ? 'Loading...' : hasNextPage ? 'Load More' : 'No more items'}
      </div>
    </div>
  );
}
```

## 2. Virtual Scrolling

```typescript
import { useVirtualizer } from '@tanstack/react-virtual';

function VirtualList({ items }: { items: any[] }) {
  const parentRef = useRef<HTMLDivElement>(null);
  
  const virtualizer = useVirtualizer({
    count: items.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 50,
    overscan: 5
  });
  
  return (
    <div ref={parentRef} style={{ height: '600px', overflow: 'auto' }}>
      <div
        style={{
          height: `${virtualizer.getTotalSize()}px`,
          position: 'relative'
        }}
      >
        {virtualizer.getVirtualItems().map(virtualItem => (
          <div
            key={virtualItem.key}
            style={{
              position: 'absolute',
              top: 0,
              left: 0,
              width: '100%',
              height: `${virtualItem.size}px`,
              transform: `translateY(${virtualItem.start}px)`
            }}
          >
            <Item data={items[virtualItem.index]} />
          </div>
        ))}
      </div>
    </div>
  );
}
```

## 3. Drag and Drop

```typescript
import { DndContext, useDraggable, useDroppable } from '@dnd-kit/core';

function Draggable({ id, children }: { id: string; children: React.ReactNode }) {
  const { attributes, listeners, setNodeRef, transform } = useDraggable({ id });
  
  const style = transform ? {
    transform: `translate3d(${transform.x}px, ${transform.y}px, 0)`,
  } : undefined;
  
  return (
    <div ref={setNodeRef} style={style} {...listeners} {...attributes}>
      {children}
    </div>
  );
}

function Droppable({ id, children }: { id: string; children: React.ReactNode }) {
  const { setNodeRef } = useDroppable({ id });
  return <div ref={setNodeRef}>{children}</div>;
}

function DragDropExample() {
  const [items, setItems] = useState(['A', 'B', 'C']);
  
  const handleDragEnd = (event: any) => {
    const { active, over } = event;
    if (over && active.id !== over.id) {
      // Reorder items
      const oldIndex = items.indexOf(active.id);
      const newIndex = items.indexOf(over.id);
      const newItems = arrayMove(items, oldIndex, newIndex);
      setItems(newItems);
    }
  };
  
  return (
    <DndContext onDragEnd={handleDragEnd}>
      {items.map(item => (
        <Draggable key={item} id={item}>
          <div>{item}</div>
        </Draggable>
      ))}
    </DndContext>
  );
}
```

## 4. Modal / Dialog with Portal

```typescript
import { createPortal } from 'react-dom';

function Modal({ isOpen, onClose, children }: ModalProps) {
  const modalRef = useRef<HTMLDivElement>(null);
  
  useEffect(() => {
    if (!isOpen) return;
    
    // Focus trap
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
      if (e.key === 'Tab') {
        const focusable = modalRef.current?.querySelectorAll(
          'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
        );
        // Handle focus trap logic
      }
    };
    
    document.addEventListener('keydown', handleKeyDown);
    document.body.style.overflow = 'hidden';
    
    return () => {
      document.removeEventListener('keydown', handleKeyDown);
      document.body.style.overflow = '';
    };
  }, [isOpen, onClose]);
  
  if (!isOpen) return null;
  
  return createPortal(
    <div
      className="fixed inset-0 bg-black/50 flex items-center justify-center z-50"
      onClick={onClose}
    >
      <div
        ref={modalRef}
        role="dialog"
        aria-modal="true"
        className="bg-white rounded-lg p-6 max-w-lg"
        onClick={(e) => e.stopPropagation()}
      >
        {children}
      </div>
    </div>,
    document.body
  );
}
```

## 5. Toast Notifications

```typescript
import { toast, Toaster } from 'react-hot-toast';

function App() {
  return (
    <>
      <Toaster position="top-right" />
      <button onClick={() => toast.success('Saved successfully!')}>
        Save
      </button>
      <button onClick={() => toast.error('Something went wrong')}>
        Error
      </button>
      <button onClick={() => {
        const promise = saveData();
        toast.promise(promise, {
          loading: 'Saving...',
          success: 'Saved!',
          error: 'Failed to save'
        });
      }}>
        Async Save
      </button>
    </>
  );
}

// Custom toast
function CustomToast() {
  return (
    <button onClick={() => toast.custom(
      <div className="bg-blue-500 text-white p-4 rounded">
        Custom message
      </div>
    )}>
      Custom
    </button>
  );
}
```

## 6. Command Palette

```typescript
import { useEffect, useState } from 'react';

function CommandPalette() {
  const [isOpen, setIsOpen] = useState(false);
  const [query, setQuery] = useState('');
  
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        setIsOpen(true);
      }
    };
    
    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, []);
  
  const commands = [
    { name: 'New Post', action: () => {} },
    { name: 'Settings', action: () => {} },
    { name: 'Logout', action: () => {} }
  ];
  
  const filtered = commands.filter(cmd =>
    cmd.name.toLowerCase().includes(query.toLowerCase())
  );
  
  if (!isOpen) return null;
  
  return (
    <div className="fixed inset-0 bg-black/50 flex items-start justify-center pt-20">
      <div className="bg-white rounded-lg w-full max-w-lg">
        <input
          type="text"
          placeholder="Type a command..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="w-full p-4 border-b"
          autoFocus
        />
        <div className="max-h-96 overflow-auto">
          {filtered.map(cmd => (
            <button
              key={cmd.name}
              onClick={() => {
                cmd.action();
                setIsOpen(false);
              }}
              className="w-full text-left p-4 hover:bg-gray-100"
            >
              {cmd.name}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
```

## 7. Skeleton Loading

```typescript
function SkeletonCard() {
  return (
    <div className="animate-pulse">
      <div className="h-48 bg-gray-200 rounded-lg mb-4" />
      <div className="space-y-2">
        <div className="h-4 bg-gray-200 rounded w-3/4" />
        <div className="h-4 bg-gray-200 rounded w-1/2" />
      </div>
    </div>
  );
}

function ContentWithSkeleton() {
  const { data, isLoading } = useQuery({
    queryKey: ['content'],
    queryFn: fetchContent
  });
  
  if (isLoading) return <SkeletonCard />;
  return <Card data={data} />;
}
```

## Best Practices

1. **Virtual scrolling for large lists** - Render only visible items
2. **Intersection Observer** - Better than scroll events
3. **Portal for modals** - Avoid z-index issues
4. **Focus management** - Trap focus in modals
5. **Keyboard shortcuts** - Cmd+K for command palette
6. **Optimistic updates** - Update UI before server response
7. **Skeleton screens** - Better than spinners for content
8. **Debounce search** - Reduce API calls
