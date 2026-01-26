---
name: api-integration
description: REST API integration, GraphQL (Apollo Client), WebSockets, tRPC, authentication (JWT, OAuth), error handling, and retry logic. Use when integrating with backend APIs, handling real-time data, or implementing authentication.
---

# API Integration

Connect frontend to backend services efficiently and reliably.

## 1. REST API with Fetch

```typescript
// GET request
async function getUsers() {
  const response = await fetch('/api/users', {
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    }
  });
  
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  
  return await response.json();
}

// POST request
async function createUser(user: User) {
  const response = await fetch('/api/users', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify(user)
  });
  
  return await response.json();
}
```

## 2. GraphQL with Apollo

```typescript
import { ApolloClient, InMemoryCache, gql, useQuery, useMutation } from '@apollo/client';

const client = new ApolloClient({
  uri: '/graphql',
  cache: new InMemoryCache()
});

// Query
const GET_USERS = gql`
  query GetUsers {
    users {
      id
      name
      email
    }
  }
`;

function UserList() {
  const { loading, error, data } = useQuery(GET_USERS);
  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error.message}</p>;
  
  return <ul>{data.users.map(user => <li key={user.id}>{user.name}</li>)}</ul>;
}

// Mutation
const CREATE_USER = gql`
  mutation CreateUser($name: String!, $email: String!) {
    createUser(name: $name, email: $email) {
      id
      name
    }
  }
`;

function CreateUserForm() {
  const [createUser] = useMutation(CREATE_USER);
  
  return <button onClick={() => createUser({
    variables: { name: 'Alice', email: 'alice@example.com' }
  })}>Create</button>;
}
```

## 3. WebSockets (Real-time)

```typescript
function Chat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const ws = useRef<WebSocket | null>(null);
  
  useEffect(() => {
    ws.current = new WebSocket('ws://localhost:3000');
    
    ws.current.onmessage = (event) => {
      const message = JSON.parse(event.data);
      setMessages(prev => [...prev, message]);
    };
    
    return () => ws.current?.close();
  }, []);
  
  const sendMessage = (text: string) => {
    ws.current?.send(JSON.stringify({ text }));
  };
  
  return <div>{/* Chat UI */}</div>;
}
```

## 4. Authentication

```typescript
// JWT Storage and Refresh
function useAuth() {
  const [token, setToken] = useState(localStorage.getItem('token'));
  
  const login = async (credentials) => {
    const response = await fetch('/api/auth/login', {
      method: 'POST',
      body: JSON.stringify(credentials)
    });
    const { token, refreshToken } = await response.json();
    localStorage.setItem('token', token);
    localStorage.setItem('refreshToken', refreshToken);
    setToken(token);
  };
  
  const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('refreshToken');
    setToken(null);
  };
  
  return { token, login, logout };
}

// Protected API calls with automatic refresh
async function fetchWithAuth(url: string, options = {}) {
  let token = localStorage.getItem('token');
  
  const response = await fetch(url, {
    ...options,
    headers: {
      'Authorization': `Bearer ${token}`,
      ...options.headers
    }
  });
  
  if (response.status === 401) {
    // Token expired, refresh it
    const refreshToken = localStorage.getItem('refreshToken');
    const refreshResponse = await fetch('/api/auth/refresh', {
      method: 'POST',
      body: JSON.stringify({ refreshToken })
    });
    const { token: newToken } = await refreshResponse.json();
    localStorage.setItem('token', newToken);
    
    // Retry original request
    return fetch(url, {
      ...options,
      headers: {
        'Authorization': `Bearer ${newToken}`,
        ...options.headers
      }
    });
  }
  
  return response;
}
```

## 5. Error Handling

```typescript
class APIError extends Error {
  constructor(public status: number, message: string) {
    super(message);
  }
}

async function apiCall(url: string) {
  try {
    const response = await fetch(url);
    
    if (!response.ok) {
      const error = await response.json();
      throw new APIError(response.status, error.message);
    }
    
    return await response.json();
  } catch (error) {
    if (error instanceof APIError) {
      // Handle specific API errors
      if (error.status === 404) console.error('Not found');
      if (error.status === 500) console.error('Server error');
    }
    throw error;
  }
}
```

## Best Practices

1. **Use Tanstack Query** - Better than manual fetch for data fetching
2. **Error boundaries** - Catch and display API errors gracefully
3. **Loading states** - Always show loading indicators
4. **Retry logic** - Retry failed requests with exponential backoff
5. **Request cancellation** - Cancel requests on component unmount
6. **Type safety** - TypeScript for API responses
7. **Secure tokens** - HttpOnly cookies > localStorage for tokens
8. **Rate limiting** - Implement client-side rate limiting
