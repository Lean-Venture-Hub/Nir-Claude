---
name: database-fullstack
description: SQL fundamentals (PostgreSQL, MySQL), Prisma ORM, MongoDB basics, Next.js server actions with database, and database design patterns. Use when integrating databases, writing queries, designing schemas, or building full-stack features with Next.js.
---

# Database & Full-Stack Integration

Connect your frontend to databases with type-safe ORMs.

## 1. Prisma ORM

### Schema Definition
```prisma
// schema.prisma
datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

generator client {
  provider = "prisma-client-js"
}

model User {
  id        String   @id @default(uuid())
  email     String   @unique
  name      String?
  posts     Post[]
  createdAt DateTime @default(now())
}

model Post {
  id        String   @id @default(uuid())
  title     String
  content   String?
  published Boolean  @default(false)
  author    User     @relation(fields: [authorId], references: [id])
  authorId  String
  createdAt DateTime @default(now())
}
```

### CRUD Operations
```typescript
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

// Create
const user = await prisma.user.create({
  data: {
    email: 'alice@example.com',
    name: 'Alice',
    posts: {
      create: { title: 'My first post' }
    }
  }
});

// Read
const users = await prisma.user.findMany({
  where: { email: { contains: 'alice' } },
  include: { posts: true }
});

// Update
const updated = await prisma.user.update({
  where: { id: userId },
  data: { name: 'Alice Smith' }
});

// Delete
await prisma.user.delete({ where: { id: userId } });
```

## 2. Next.js Server Actions

```typescript
// app/actions.ts
'use server';

import { prisma } from '@/lib/prisma';
import { revalidatePath } from 'next/cache';

export async function createPost(formData: FormData) {
  const title = formData.get('title') as string;
  const content = formData.get('content') as string;
  
  await prisma.post.create({
    data: { title, content, authorId: 'user-id' }
  });
  
  revalidatePath('/posts');
  return { success: true };
}

export async function getPosts() {
  return await prisma.post.findMany({
    include: { author: true },
    orderBy: { createdAt: 'desc' }
  });
}

// app/posts/page.tsx
import { getPosts } from '../actions';

export default async function PostsPage() {
  const posts = await getPosts();
  return <div>{posts.map(post => <Post key={post.id} {...post} />)}</div>;
}
```

## 3. SQL Basics

```sql
-- Select
SELECT * FROM users WHERE email LIKE '%alice%';

-- Join
SELECT u.name, p.title
FROM users u
JOIN posts p ON u.id = p.author_id
WHERE p.published = true;

-- Aggregate
SELECT author_id, COUNT(*) as post_count
FROM posts
GROUP BY author_id
HAVING COUNT(*) > 5;

-- Index for performance
CREATE INDEX idx_posts_author_id ON posts(author_id);
```

## 4. MongoDB with Mongoose

```typescript
import mongoose from 'mongoose';

const userSchema = new mongoose.Schema({
  email: { type: String, required: true, unique: true },
  name: String,
  posts: [{ type: mongoose.Schema.Types.ObjectId, ref: 'Post' }]
});

const User = mongoose.model('User', userSchema);

// CRUD
const user = await User.create({ email: 'alice@example.com', name: 'Alice' });
const users = await User.find({ name: /alice/i }).populate('posts');
```

## Best Practices

1. **Use Prisma for type safety** - TypeScript types from schema
2. **Validate input** - Never trust user input
3. **Use transactions** - For multi-step operations
4. **Index frequently queried fields** - Performance optimization
5. **Connection pooling** - Reuse database connections
6. **Migrations** - Version control for database schema
7. **Environment variables** - Never commit DATABASE_URL
8. **Error handling** - Catch and handle database errors gracefully
