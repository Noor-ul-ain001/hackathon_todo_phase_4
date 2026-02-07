# TaskFlow Intelligence Platform - Authentication Guide

Complete authentication system with JWT tokens, secure password hashing, and protected routes.

## Features

### Backend
- **JWT Authentication**: Secure token-based authentication
- **Password Hashing**: Bcrypt password hashing with salt
- **Token Refresh**: Automatic token refresh mechanism
- **Protected Endpoints**: Middleware for route protection
- **User Management**: Registration, login, logout, and user info

### Frontend
- **Auth Context**: React context for global auth state
- **Protected Routes**: Component wrapper for authenticated pages
- **Token Storage**: Secure localStorage token management
- **Auto Refresh**: Automatic token refresh on 401
- **Login/Signup Pages**: Beautiful TypeScript auth pages

## API Endpoints

### Authentication Endpoints

#### Register New User
```http
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword123"
}

Response:
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

#### Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword123"
}

Response:
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

#### Refresh Token
```http
POST /api/auth/refresh
Content-Type: application/json

{
  "refresh_token": "eyJ..."
}

Response:
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

#### Get Current User
```http
GET /api/auth/me
Authorization: Bearer <access_token>

Response:
{
  "id": "user_abc123",
  "email": "user@example.com",
  "created_at": "2025-12-28T10:00:00Z",
  "updated_at": "2025-12-28T10:00:00Z"
}
```

#### Logout
```http
POST /api/auth/logout

Response:
{
  "message": "Successfully logged out"
}
```

## Backend Usage

### Protect a Route

```python
from fastapi import APIRouter, Depends
from src.auth.dependencies import get_current_user
from src.models.user import User

router = APIRouter()

@router.get("/protected")
async def protected_route(current_user: User = Depends(get_current_user)):
    return {"message": f"Hello {current_user.email}!"}
```

### Optional Authentication

```python
from src.auth.dependencies import get_optional_current_user

@router.get("/optional-auth")
async def optional_auth_route(user: User = Depends(get_optional_current_user)):
    if user:
        return {"message": f"Authenticated as {user.email}"}
    return {"message": "Public access"}
```

## Frontend Usage

### Use Auth Context

```typescript
import { useAuth } from '@/contexts/AuthContext'

function MyComponent() {
  const { user, login, logout, isAuthenticated } = useAuth()

  if (!isAuthenticated) {
    return <div>Please login</div>
  }

  return (
    <div>
      <p>Welcome {user.email}</p>
      <button onClick={logout}>Logout</button>
    </div>
  )
}
```

### Protect a Page

```typescript
import ProtectedRoute from '@/components/ProtectedRoute'

function DashboardPage() {
  return (
    <ProtectedRoute>
      <div>
        <h1>Protected Dashboard</h1>
        {/* Your dashboard content */}
      </div>
    </ProtectedRoute>
  )
}

export default DashboardPage
```

### Login Example

```typescript
import { useAuth } from '@/contexts/AuthContext'
import { useState } from 'react'

function LoginForm() {
  const { login } = useAuth()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      await login({ email, password })
      // Redirect to dashboard
    } catch (error) {
      console.error('Login failed:', error)
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <button type="submit">Login</button>
    </form>
  )
}
```

## Setup Instructions

### Backend Setup

1. **Install Dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env and set:
   # - DATABASE_URL
   # - JWT_SECRET_KEY (use a strong random string)
   ```

3. **Run Migrations**
   ```bash
   alembic upgrade head
   ```

4. **Start Server**
   ```bash
   uvicorn src.main:app --reload
   ```

### Frontend Setup

1. **Install Dependencies**
   ```bash
   cd frontend
   npm install
   ```

2. **Configure Environment**
   ```bash
   cp .env.example .env.local
   # Edit .env.local and set:
   # - NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

3. **Start Development Server**
   ```bash
   npm run dev
   ```

## Security Features

### Password Security
- **Bcrypt Hashing**: Industry-standard password hashing
- **Salt Rounds**: Configurable cost factor for hashing
- **No Plain Text**: Passwords never stored in plain text

### Token Security
- **JWT Tokens**: Cryptographically signed tokens
- **Token Expiration**: Access tokens expire in 30 minutes
- **Refresh Tokens**: Long-lived tokens for renewal (7 days)
- **Token Validation**: Signature and expiration verification

### API Security
- **CORS Protection**: Configured allowed origins
- **Bearer Authentication**: Standard HTTP authentication
- **Token Type Checking**: Validates access vs refresh tokens

## Testing Authentication

### Test Registration
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'
```

### Test Login
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'
```

### Test Protected Endpoint
```bash
# First get a token from login, then:
curl -X GET http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## File Structure

```
backend/
├── src/
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── security.py       # JWT and password utilities
│   │   └── dependencies.py   # Auth middleware
│   ├── api/
│   │   └── auth.py           # Auth endpoints
│   └── models/
│       └── user.py           # User model

frontend/
├── src/
│   ├── contexts/
│   │   └── AuthContext.tsx   # Auth state management
│   ├── services/
│   │   └── auth.ts           # Auth API service
│   └── components/
│       └── ProtectedRoute.tsx # Route protection
├── pages/
│   ├── login.tsx             # Login page
│   ├── signup.tsx            # Signup page
│   └── _app.tsx              # App with AuthProvider
```

## Token Management

### Token Lifecycle

1. **Registration/Login**: User receives access + refresh token
2. **API Requests**: Include access token in Authorization header
3. **Token Expiry**: Access token expires after 30 minutes
4. **Auto Refresh**: Frontend automatically refreshes on 401
5. **Logout**: Tokens removed from localStorage

### Token Storage

- **Access Token**: `taskflow_access_token` in localStorage
- **Refresh Token**: `taskflow_refresh_token` in localStorage

### Security Best Practices

- Never expose JWT secret key
- Use HTTPS in production
- Implement token rotation
- Add token blacklisting for logout (optional)
- Monitor for suspicious activity

## Troubleshooting

### Common Issues

**401 Unauthorized**
- Check if token is included in Authorization header
- Verify token hasn't expired
- Ensure JWT_SECRET_KEY matches between requests

**CORS Errors**
- Add frontend URL to CORS_ORIGINS in backend .env
- Check CORS middleware configuration

**Token Not Persisting**
- Check browser localStorage
- Verify localStorage isn't blocked
- Check for incognito/private mode

## Next Steps

- [ ] Add email verification
- [ ] Implement password reset
- [ ] Add OAuth providers (Google, GitHub)
- [ ] Implement token blacklisting
- [ ] Add rate limiting
- [ ] Add multi-factor authentication (MFA)
- [ ] Implement session management
- [ ] Add audit logging

## Support

For issues or questions:
- Check API docs at http://localhost:8000/docs
- Review error messages in browser console
- Check backend logs for detailed errors
