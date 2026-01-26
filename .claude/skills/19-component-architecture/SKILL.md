---
name: component-architecture
description: Component design patterns (atomic design, container/presentational), composition strategies, prop design, component reusability, and single responsibility principle. Use when designing component APIs, organizing component structure, or building component libraries.
---

# Component Architecture

Design scalable, reusable component systems.

## 1. Atomic Design

### Atoms (Basic building blocks)
```typescript
// Button.tsx
interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  children: React.ReactNode;
  onClick?: () => void;
}

export function Button({
  variant = 'primary',
  size = 'md',
  children,
  onClick
}: ButtonProps) {
  const baseClasses = 'font-medium rounded';
  const variantClasses = {
    primary: 'bg-blue-500 text-white hover:bg-blue-600',
    secondary: 'bg-gray-200 text-gray-900 hover:bg-gray-300',
    ghost: 'bg-transparent hover:bg-gray-100'
  };
  const sizeClasses = {
    sm: 'px-2 py-1 text-sm',
    md: 'px-4 py-2',
    lg: 'px-6 py-3 text-lg'
  };
  
  return (
    <button
      className={`${baseClasses} ${variantClasses[variant]} ${sizeClasses[size]}`}
      onClick={onClick}
    >
      {children}
    </button>
  );
}
```

### Molecules (Simple combinations)
```typescript
// SearchInput.tsx
import { Input } from './Input';
import { Button } from './Button';

interface SearchInputProps {
  onSearch: (query: string) => void;
  placeholder?: string;
}

export function SearchInput({ onSearch, placeholder }: SearchInputProps) {
  const [query, setQuery] = useState('');
  
  return (
    <div className="flex gap-2">
      <Input
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder={placeholder}
      />
      <Button onClick={() => onSearch(query)}>Search</Button>
    </div>
  );
}
```

### Organisms (Complex components)
```typescript
// UserCard.tsx
import { Avatar } from './Avatar';
import { Button } from './Button';
import { Badge } from './Badge';

interface UserCardProps {
  user: {
    name: string;
    email: string;
    avatar: string;
    role: string;
  };
  onMessage: () => void;
  onFollow: () => void;
}

export function UserCard({ user, onMessage, onFollow }: UserCardProps) {
  return (
    <div className="border rounded-lg p-4">
      <div className="flex items-center gap-4">
        <Avatar src={user.avatar} alt={user.name} />
        <div className="flex-1">
          <h3 className="font-semibold">{user.name}</h3>
          <p className="text-sm text-gray-600">{user.email}</p>
          <Badge>{user.role}</Badge>
        </div>
      </div>
      <div className="flex gap-2 mt-4">
        <Button onClick={onMessage}>Message</Button>
        <Button variant="secondary" onClick={onFollow}>Follow</Button>
      </div>
    </div>
  );
}
```

## 2. Component Patterns

### Container/Presentational
```typescript
// UserListContainer.tsx (Smart Component)
export function UserListContainer() {
  const { data: users, loading } = useFetch<User[]>('/api/users');
  const [searchQuery, setSearchQuery] = useState('');
  
  const filteredUsers = users?.filter(user =>
    user.name.toLowerCase().includes(searchQuery.toLowerCase())
  );
  
  if (loading) return <Spinner />;
  
  return (
    <UserList
      users={filteredUsers}
      searchQuery={searchQuery}
      onSearchChange={setSearchQuery}
    />
  );
}

// UserList.tsx (Presentational Component)
interface UserListProps {
  users?: User[];
  searchQuery: string;
  onSearchChange: (query: string) => void;
}

export function UserList({ users, searchQuery, onSearchChange }: UserListProps) {
  return (
    <div>
      <SearchInput value={searchQuery} onChange={onSearchChange} />
      <div className="space-y-4">
        {users?.map(user => (
          <UserCard key={user.id} user={user} />
        ))}
      </div>
    </div>
  );
}
```

### Composition
```typescript
// Card component with slots
interface CardProps {
  header?: React.ReactNode;
  footer?: React.ReactNode;
  children: React.ReactNode;
}

export function Card({ header, footer, children }: CardProps) {
  return (
    <div className="border rounded-lg overflow-hidden">
      {header && <div className="border-b p-4 bg-gray-50">{header}</div>}
      <div className="p-4">{children}</div>
      {footer && <div className="border-t p-4 bg-gray-50">{footer}</div>}
    </div>
  );
}

// Usage with composition
<Card
  header={<h2>User Profile</h2>}
  footer={<Button>Edit</Button>}
>
  <UserInfo user={user} />
</Card>
```

## 3. Prop Design

### Good Prop APIs
```typescript
// ❌ Bad: Too many props
interface BadButtonProps {
  color: string;
  backgroundColor: string;
  borderColor: string;
  hoverColor: string;
  // ... many more
}

// ✅ Good: Semantic variants
interface GoodButtonProps {
  variant?: 'primary' | 'secondary' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  fullWidth?: boolean;
  disabled?: boolean;
  children: React.ReactNode;
}

// ✅ Better: Extend native props
interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary';
  isLoading?: boolean;
}

export function Button({ variant = 'primary', isLoading, children, ...props }: ButtonProps) {
  return (
    <button {...props} disabled={isLoading || props.disabled}>
      {isLoading ? <Spinner /> : children}
    </button>
  );
}
```

## 4. Component Reusability

### Polymorphic Components
```typescript
type AsProp<C extends React.ElementType> = {
  as?: C;
};

type PropsToOmit<C extends React.ElementType, P> = keyof (AsProp<C> & P);

type PolymorphicComponentProp<
  C extends React.ElementType,
  Props = {}
> = React.PropsWithChildren<Props & AsProp<C>> &
  Omit<React.ComponentPropsWithoutRef<C>, PropsToOmit<C, Props>>;

interface TextProps {
  color?: 'primary' | 'secondary';
}

export function Text<C extends React.ElementType = 'span'>({
  as,
  color = 'primary',
  children,
  ...props
}: PolymorphicComponentProp<C, TextProps>) {
  const Component = as || 'span';
  return (
    <Component className={`text-${color}`} {...props}>
      {children}
    </Component>
  );
}

// Usage
<Text>Span by default</Text>
<Text as="p">Paragraph</Text>
<Text as="h1">Heading</Text>
<Text as={Link} href="/about">Link</Text>
```

## Best Practices

1. **Single Responsibility** - One component, one job
2. **Composition over configuration** - Compose small pieces
3. **Semantic props** - variant, size, not colors and pixels
4. **Extend native props** - Don't reinvent HTML attributes
5. **Explicit is better than implicit** - Clear prop names
6. **Colocate related code** - Keep component files together
7. **Document component APIs** - JSDoc or Storybook
8. **Think in systems** - Build for reuse, not one-offs
