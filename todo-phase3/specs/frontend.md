# Frontend Specification

## Overview

Phase-2 frontend is a Next.js application using App Router, providing a modern web interface for multi-user todo management.

**Framework:** Next.js (App Router)
**Language:** TypeScript
**Styling:** Tailwind CSS (optional, for hackathon simplicity)
**State Management:** React hooks (useState, useEffect)
**HTTP Client:** Fetch API or Axios

## Project Structure

```
frontend/
├── app/
│   ├── layout.tsx          # Root layout
│   ├── page.tsx            # Landing page
│   ├── login/
│   │   └── page.tsx        # Login page
│   ├── register/
│   │   └── page.tsx        # Registration page
│   └── dashboard/
│       ├── page.tsx        # Todo list (protected)
│       └── loading.tsx     # Loading state
├── components/
│   ├── Layout.tsx          # Common layout
│   ├── Navbar.tsx          # Navigation bar
│   ├── TaskList.tsx        # Task list component
│   ├── TaskItem.tsx        # Individual task
│   ├── TaskForm.tsx        # Add/edit task form
│   ├── AuthForm.tsx        # Login/register form
│   └── ProtectedRoute.tsx  # Route protection wrapper
├── lib/
│   ├── api.ts              # API client functions
│   ├── auth.ts             # Auth utilities
│   └── types.ts            # TypeScript types
└── public/
    └── favicon.ico
```

## Pages and Routes

### 1. Landing Page (`/`)

**Route:** `/`

**Purpose:** Landing page that redirects based on authentication status

**Behavior:**
- If user is authenticated (has valid tokens), redirect to `/dashboard`
- If not authenticated, redirect to `/login`

**Implementation:**
```typescript
// app/page.tsx
'use client'
import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { isAuthenticated } from '@/lib/auth'

export default function HomePage() {
  const router = useRouter()

  useEffect(() => {
    if (isAuthenticated()) {
      router.push('/dashboard')
    } else {
      router.push('/login')
    }
  }, [router])

  return <div>Loading...</div>
}
```

---

### 2. Login Page (`/login`)

**Route:** `/login`

**Purpose:** User authentication

**Component:** `AuthForm` with mode="login"

**Features:**
- Username and password input fields
- Submit button
- Error message display
- Link to registration page
- Redirect to dashboard on successful login
- Prevent access if already authenticated (redirect to dashboard)

**State:**
```typescript
{
  username: string,
  password: string,
  loading: boolean,
  error: string | null
}
```

**Flow:**
1. User enters credentials
2. Validates required fields
3. Calls `api.login(username, password)`
4. On success: Store tokens in localStorage, redirect to `/dashboard`
5. On error: Display error message, clear password field

---

### 3. Registration Page (`/register`)

**Route:** `/register`

**Purpose:** New user registration

**Component:** `AuthForm` with mode="register"

**Features:**
- Username and password input fields
- Password confirmation field
- Submit button
- Error message display
- Link to login page
- Redirect to dashboard on successful registration
- Prevent access if already authenticated (redirect to dashboard)

**State:**
```typescript
{
  username: string,
  password: string,
  confirmPassword: string,
  loading: boolean,
  error: string | null
}
```

**Validation:**
- Username: 3-50 characters, alphanumeric + underscores
- Password: Minimum 8 characters
- Password confirmation: Must match password

**Flow:**
1. User enters registration details
2. Validates all fields client-side
3. Calls `api.register(username, password)`
4. On success: Store tokens in localStorage, redirect to `/dashboard`
5. On error: Display error message

---

### 4. Dashboard (`/dashboard`)

**Route:** `/dashboard`

**Purpose:** Main todo list interface

**Protection:** Protected route (requires authentication)

**Components:**
- `Navbar` (top navigation with logout button)
- `TaskForm` (add new task)
- `TaskList` (display and manage tasks)

**Features:**
- Display all user's tasks
- Filter by completion status (All/Active/Completed)
- Add new tasks
- Toggle task completion
- Delete tasks
- Optional: Edit tasks
- Logout button
- Display username

**State:**
```typescript
{
  tasks: Task[],
  filter: 'all' | 'active' | 'completed',
  loading: boolean,
  error: string | null
}
```

**Flow:**
1. Check authentication on mount
   - If not authenticated, redirect to `/login`
2. Fetch user's tasks via `api.getTasks()`
3. Display tasks according to selected filter
4. Handle task operations (create, toggle, delete)
5. Refetch tasks after each operation

## Components

### AuthForm Component

**Purpose:** Reusable form for login and registration

**Props:**
```typescript
interface AuthFormProps {
  mode: 'login' | 'register'
  onSuccess?: () => void
}
```

**Features:**
- Dynamic form fields based on mode
- Client-side validation
- Loading state during API call
- Error display
- Links between login and register

---

### Navbar Component

**Purpose:** Top navigation bar

**Features:**
- Display application title
- Display logged-in username
- Logout button
- Links (if any)

---

### TaskList Component

**Purpose:** Display list of tasks

**Props:**
```typescript
interface TaskListProps {
  tasks: Task[]
  onToggle: (taskId: string) => void
  onDelete: (taskId: string) => void
  loading?: boolean
}
```

**Features:**
- Empty state message when no tasks
- Display tasks with completion indicator
- Checkbox for toggling completion
- Delete button
- Optional: Edit button
- Loading spinner

---

### TaskItem Component

**Purpose:** Individual task display

**Props:**
```typescript
interface TaskItemProps {
  task: Task
  onToggle: () => void
  onDelete: () => void
}
```

**Features:**
- Display task title
- Display description (if present)
- Completed styling (strikethrough, grayed out)
- Toggle checkbox
- Delete button
- Optional: Edit button

---

### TaskForm Component

**Purpose:** Form for adding new tasks

**Props:**
```typescript
interface TaskFormProps {
  onSubmit: (title: string, description?: string) => void
  loading?: boolean
}
```

**Features:**
- Title input (required, max 200 chars)
- Description textarea (optional, max 1000 chars)
- Submit button
- Client-side validation
- Loading state

---

### ProtectedRoute Component

**Purpose:** Wrapper to protect routes requiring authentication

**Usage:**
```typescript
<ProtectedRoute>
  <Dashboard />
</ProtectedRoute>
```

**Implementation:**
```typescript
'use client'
import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { isAuthenticated } from '@/lib/auth'

export function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const router = useRouter()

  useEffect(() => {
    if (!isAuthenticated()) {
      router.push('/login')
    }
  }, [router])

  if (!isAuthenticated()) {
    return <div>Loading...</div>
  }

  return <>{children}</>
}
```

---

## Type Definitions

**File:** `lib/types.ts`

```typescript
export interface User {
  id: string
  username: string
}

export interface Task {
  id: string
  user_id: string
  title: string
  description: string | null
  completed: boolean
  created_at: string
  updated_at: string
}

export interface AuthResponse {
  access_token: string
  refresh_token: string
  user_id: string
  username: string
}

export interface LoginRequest {
  username: string
  password: string
}

export interface RegisterRequest {
  username: string
  password: string
}

export interface CreateTaskRequest {
  title: string
  description?: string
}

export interface UpdateTaskRequest {
  title?: string
  description?: string
  completed?: boolean
}

export interface TasksResponse {
  tasks: Task[]
  count: number
}

export interface TaskResponse {
  task: Task
}

export interface ErrorResponse {
  error: string
  message: string
  details?: string
}
```

## API Client

**File:** `lib/api.ts`

### Base Configuration

```typescript
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
```

### Helper Functions

```typescript
async function fetchAPI<T>(
  endpoint: string,
  options?: RequestInit
): Promise<T> {
  const token = localStorage.getItem('access_token')

  const headers: HeadersInit = {
    'Content-Type': 'application/json',
    ...(token && { Authorization: `Bearer ${token}` }),
    ...options?.headers,
  }

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  })

  if (!response.ok) {
    const error: ErrorResponse = await response.json()
    throw new Error(error.message || 'Request failed')
  }

  // Handle 204 No Content
  if (response.status === 204) {
    return {} as T
  }

  return response.json()
}
```

### Auth API Functions

```typescript
// Register
export async function register(
  username: string,
  password: string
): Promise<AuthResponse> {
  return fetchAPI<AuthResponse>('/api/auth/register', {
    method: 'POST',
    body: JSON.stringify({ username, password }),
  })
}

// Login
export async function login(
  username: string,
  password: string
): Promise<AuthResponse> {
  return fetchAPI<AuthResponse>('/api/auth/login', {
    method: 'POST',
    body: JSON.stringify({ username, password }),
  })
}

// Refresh token
export async function refreshToken(
  refreshToken: string
): Promise<{ access_token: string; refresh_token: string }> {
  return fetchAPI<{ access_token: string; refresh_token: string }>(
    '/api/auth/refresh',
    {
      method: 'POST',
      body: JSON.stringify({ refresh_token: refreshToken }),
    }
  )
}

// Logout
export async function logout(refreshToken: string): Promise<void> {
  return fetchAPI<void>('/api/auth/logout', {
    method: 'POST',
    body: JSON.stringify({ refresh_token: refreshToken }),
  })
}
```

### Task API Functions

```typescript
// Get all tasks
export async function getTasks(filter?: {
  completed?: boolean
}): Promise<TasksResponse> {
  const params = new URLSearchParams()
  if (filter?.completed !== undefined) {
    params.append('completed', filter.completed.toString())
  }

  const endpoint = params.toString()
    ? `/api/tasks?${params.toString()}`
    : '/api/tasks'

  return fetchAPI<TasksResponse>(endpoint)
}

// Get single task
export async function getTask(taskId: string): Promise<TaskResponse> {
  return fetchAPI<TaskResponse>(`/api/tasks/${taskId}`)
}

// Create task
export async function createTask(
  title: string,
  description?: string
): Promise<TaskResponse> {
  return fetchAPI<TaskResponse>('/api/tasks', {
    method: 'POST',
    body: JSON.stringify({ title, description }),
  })
}

// Update task
export async function updateTask(
  taskId: string,
  data: UpdateTaskRequest
): Promise<TaskResponse> {
  return fetchAPI<TaskResponse>(`/api/tasks/${taskId}`, {
    method: 'PUT',
    body: JSON.stringify(data),
  })
}

// Toggle task
export async function toggleTask(taskId: string): Promise<TaskResponse> {
  return fetchAPI<TaskResponse>(`/api/tasks/${taskId}/toggle`, {
    method: 'PATCH',
  })
}

// Delete task
export async function deleteTask(taskId: string): Promise<void> {
  return fetchAPI<void>(`/api/tasks/${taskId}`, {
    method: 'DELETE',
  })
}
```

## Authentication Utilities

**File:** `lib/auth.ts`

```typescript
export interface StoredAuth {
  access_token: string
  refresh_token: string
  user_id: string
  username: string
}

// Check if user is authenticated
export function isAuthenticated(): boolean {
  const token = localStorage.getItem('access_token')
  return !!token && isTokenValid(token)
}

// Get stored auth data
export function getAuth(): StoredAuth | null {
  const access_token = localStorage.getItem('access_token')
  const refresh_token = localStorage.getItem('refresh_token')
  const user_id = localStorage.getItem('user_id')
  const username = localStorage.getItem('username')

  if (!access_token || !refresh_token || !user_id || !username) {
    return null
  }

  return { access_token, refresh_token, user_id, username }
}

// Store auth data
export function setAuth(auth: StoredAuth): void {
  localStorage.setItem('access_token', auth.access_token)
  localStorage.setItem('refresh_token', auth.refresh_token)
  localStorage.setItem('user_id', auth.user_id)
  localStorage.setItem('username', auth.username)
}

// Clear auth data
export function clearAuth(): void {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  localStorage.removeItem('user_id')
  localStorage.removeItem('username')
}

// Check if token is expired
export function isTokenValid(token: string): boolean {
  try {
    const payload = JSON.parse(atob(token.split('.')[1]))
    const now = Date.now() / 1000
    return payload.exp > now
  } catch {
    return false
  }
}

// Get current user
export function getCurrentUser(): { user_id: string; username: string } | null {
  const user_id = localStorage.getItem('user_id')
  const username = localStorage.getItem('username')

  if (!user_id || !username) {
    return null
  }

  return { user_id, username }
}
```

## Token Refresh Mechanism

### Automatic Token Refresh

**Implementation:**

```typescript
// Add this to fetchAPI helper
async function fetchAPI<T>(
  endpoint: string,
  options?: RequestInit,
  isRetry = false
): Promise<T> {
  const token = localStorage.getItem('access_token')

  // Check if token is about to expire (within 5 minutes)
  if (token && !isRetry && isTokenExpiringSoon(token)) {
    await refreshAccessToken()
  }

  const headers: HeadersInit = {
    'Content-Type': 'application/json',
    ...(token && { Authorization: `Bearer ${token}` }),
    ...options?.headers,
  }

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  })

  // If 401 and not retried yet, try refreshing token
  if (response.status === 401 && !isRetry) {
    await refreshAccessToken()
    return fetchAPI<T>(endpoint, options, true) // Retry with new token
  }

  if (!response.ok) {
    const error: ErrorResponse = await response.json()

    // If refresh failed, clear auth and redirect
    if (error.error === 'invalid_token' && isRetry) {
      clearAuth()
      window.location.href = '/login'
      throw new Error('Session expired')
    }

    throw new Error(error.message || 'Request failed')
  }

  if (response.status === 204) {
    return {} as T
  }

  return response.json()
}

// Check if token expires within 5 minutes
function isTokenExpiringSoon(token: string): boolean {
  try {
    const payload = JSON.parse(atob(token.split('.')[1]))
    const now = Date.now() / 1000
    const fiveMinutes = 5 * 60
    return payload.exp - now < fiveMinutes
  } catch {
    return false
  }
}

// Refresh access token
async function refreshAccessToken(): Promise<void> {
  const refreshToken = localStorage.getItem('refresh_token')

  if (!refreshToken) {
    throw new Error('No refresh token')
  }

  try {
    const response = await fetch(`${API_BASE_URL}/api/auth/refresh`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ refresh_token: refreshToken }),
    })

    if (!response.ok) {
      throw new Error('Failed to refresh token')
    }

    const { access_token, refresh_token: new_refresh_token } = await response.json()

    localStorage.setItem('access_token', access_token)
    localStorage.setItem('refresh_token', new_refresh_token)
  } catch (error) {
    clearAuth()
    window.location.href = '/login'
    throw error
  }
}
```

## State Management

### Dashboard Component State

```typescript
'use client'
import { useState, useEffect } from 'react'
import { getTasks, createTask, toggleTask, deleteTask } from '@/lib/api'

export default function Dashboard() {
  const [tasks, setTasks] = useState<Task[]>([])
  const [filter, setFilter] = useState<'all' | 'active' | 'completed'>('all')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchTasks()
  }, [filter])

  const fetchTasks = async () => {
    try {
      setLoading(true)
      const query = filter === 'all' ? {} : { completed: filter === 'completed' }
      const response = await getTasks(query)
      setTasks(response.tasks)
      setError(null)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load tasks')
    } finally {
      setLoading(false)
    }
  }

  const handleCreateTask = async (title: string, description?: string) => {
    try {
      await createTask(title, description)
      await fetchTasks() // Refresh task list
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create task')
    }
  }

  const handleToggleTask = async (taskId: string) => {
    try {
      await toggleTask(taskId)
      await fetchTasks() // Refresh task list
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to update task')
    }
  }

  const handleDeleteTask = async (taskId: string) => {
    try {
      await deleteTask(taskId)
      await fetchTasks() // Refresh task list
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to delete task')
    }
  }

  // Filter tasks based on selected filter
  const filteredTasks = tasks.filter((task) => {
    if (filter === 'active') return !task.completed
    if (filter === 'completed') return task.completed
    return true
  })

  return (
    // Render UI with tasks
  )
}
```

## Environment Variables

**File:** `.env.local` (frontend root)

```bash
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Styling Guidelines

**For Hackathon:**
- Keep styling minimal and functional
- Use standard CSS modules or Tailwind CSS
- Focus on functionality over aesthetics
- Ensure responsive design works on mobile

**Required Elements:**
- Clear visual distinction between completed and incomplete tasks
- Loading indicators for async operations
- Error messages displayed prominently
- Accessible form labels and buttons

## Build and Deployment

**Development:**
```bash
cd frontend
npm run dev
# Runs on http://localhost:3000
```

**Build:**
```bash
cd frontend
npm run build
```

**Start Production:**
```bash
cd frontend
npm start
```
