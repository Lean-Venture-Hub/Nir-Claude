---
name: frontend-testing
description: Unit testing (Jest, Vitest), integration testing (Testing Library), E2E testing (Playwright, Cypress), and testing best practices. Use when writing tests, implementing TDD, or ensuring code quality.
---

# Frontend Testing

Comprehensive testing strategies for reliable applications.

## 1. Unit Testing (Vitest/Jest)

```typescript
// sum.ts
export function sum(a: number, b: number) {
  return a + b;
}

// sum.test.ts
import { describe, it, expect } from 'vitest';
import { sum } from './sum';

describe('sum', () => {
  it('adds two numbers', () => {
    expect(sum(2, 3)).toBe(5);
  });
  
  it('handles negative numbers', () => {
    expect(sum(-1, 1)).toBe(0);
  });
});
```

## 2. Component Testing (Testing Library)

```typescript
import { render, screen, fireEvent } from '@testing-library/react';
import { Counter } from './Counter';

describe('Counter', () => {
  it('renders initial count', () => {
    render(<Counter initialCount={0} />);
    expect(screen.getByText('Count: 0')).toBeInTheDocument();
  });
  
  it('increments count on button click', () => {
    render(<Counter initialCount={0} />);
    const button = screen.getByRole('button', { name: /increment/i });
    fireEvent.click(button);
    expect(screen.getByText('Count: 1')).toBeInTheDocument();
  });
  
  it('calls onIncrement callback', () => {
    const handleIncrement = vi.fn();
    render(<Counter initialCount={0} onIncrement={handleIncrement} />);
    const button = screen.getByRole('button', { name: /increment/i });
    fireEvent.click(button);
    expect(handleIncrement).toHaveBeenCalledWith(1);
  });
});
```

## 3. E2E Testing (Playwright)

```typescript
import { test, expect } from '@playwright/test';

test('user can sign up and log in', async ({ page }) => {
  // Navigate to signup
  await page.goto('/signup');
  
  // Fill form
  await page.fill('input[name="email"]', 'test@example.com');
  await page.fill('input[name="password"]', 'password123');
  await page.click('button[type="submit"]');
  
  // Verify redirect to dashboard
  await expect(page).toHaveURL('/dashboard');
  await expect(page.locator('h1')).toContainText('Welcome');
});

test('displays error for invalid login', async ({ page }) => {
  await page.goto('/login');
  await page.fill('input[name="email"]', 'wrong@example.com');
  await page.fill('input[name="password"]', 'wrong');
  await page.click('button[type="submit"]');
  
  await expect(page.locator('.error')).toContainText('Invalid credentials');
});
```

## 4. Mocking

```typescript
// Mock API calls
import { vi } from 'vitest';

global.fetch = vi.fn();

it('fetches users', async () => {
  const mockUsers = [{ id: 1, name: 'Alice' }];
  (fetch as any).mockResolvedValueOnce({
    ok: true,
    json: async () => mockUsers
  });
  
  const users = await getUsers();
  expect(users).toEqual(mockUsers);
  expect(fetch).toHaveBeenCalledWith('/api/users');
});
```

## Best Practices

1. **Write tests first** - TDD approach when possible
2. **Test behavior, not implementation** - Focus on user interactions
3. **Use Testing Library queries** - getByRole, getByLabelText
4. **Mock external dependencies** - APIs, date, random
5. **Keep tests isolated** - Independent, repeatable
6. **Test edge cases** - Error states, empty data, loading
7. **Avoid testing internal details** - Test public API only
8. **Run tests in CI** - Automated testing on every commit
