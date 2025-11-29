# JWT Authentication Implementation

## ✅ Authentication System Updated

The authentication system has been **changed from Firebase to JWT-based authentication**.

## 🔄 What Changed

### Backend Changes

1. **Removed Firebase Admin SDK**
   - Removed `firebase-admin` from `requirements.txt`
   - Removed Firebase credentials configuration

2. **Updated User Model**
   - Removed `firebase_uid` field
   - Added `password_hash` field for storing hashed passwords
   - Added `set_password()` method to hash passwords
   - Added `check_password()` method to verify passwords
   - Uses Werkzeug's password hashing utilities

3. **Updated Authentication Endpoints**
   - `/api/auth/register` - Now accepts email, password, and role
   - `/api/auth/login` - Authenticates with email/password, returns JWT tokens
   - `/api/auth/refresh` - Refreshes access token using refresh token
   - `/api/auth/logout` - Logout endpoint
   - `/api/auth/verify` - Verifies JWT token validity
   - `/api/auth/user` - Gets current user from JWT token

4. **JWT Token Management**
   - Access tokens expire in 1 hour
   - Refresh tokens expire in 30 days
   - Tokens include user ID as identity

### Frontend Changes

1. **Removed Firebase**
   - Removed `firebase` package from `package.json`
   - Deleted `src/services/firebase.js`
   - Removed Firebase configuration

2. **Updated AuthContext**
   - Now uses JWT tokens stored in localStorage
   - Stores `access_token`, `refresh_token`, and `user` data
   - Automatically adds JWT token to API requests
   - Handles token refresh on 401 errors

3. **Updated API Service**
   - Automatically includes JWT token in Authorization header
   - Automatically refreshes token on 401 errors
   - Redirects to login if refresh fails

## 🔐 How It Works

### Registration Flow

1. User fills registration form (email, password, role)
2. Frontend sends POST request to `/api/auth/register`
3. Backend validates input, hashes password, creates user
4. Backend returns JWT tokens (access + refresh) and user data
5. Frontend stores tokens in localStorage
6. User is automatically logged in

### Login Flow

1. User fills login form (email, password)
2. Frontend sends POST request to `/api/auth/login`
3. Backend verifies email and password hash
4. Backend returns JWT tokens (access + refresh) and user data
5. Frontend stores tokens in localStorage
6. User is redirected to appropriate dashboard

### API Request Flow

1. Frontend makes API request
2. Axios interceptor adds JWT token to Authorization header: `Bearer <token>`
3. Backend verifies JWT token using Flask-JWT-Extended
4. Backend processes request with authenticated user context

### Token Refresh Flow

1. Access token expires (after 1 hour)
2. API request returns 401 Unauthorized
3. Frontend automatically tries to refresh token
4. Sends refresh token to `/api/auth/refresh`
5. Backend validates refresh token and returns new access token
6. Frontend retries original request with new token
7. If refresh fails, user is logged out and redirected to login

## 📋 Environment Variables

### Backend (.env)

```env
# JWT Configuration
JWT_SECRET_KEY=your-secret-key-change-in-production
SECRET_KEY=your-secret-key-change-in-production

# Database
DATABASE_URL=postgresql://user:pass@localhost/dbname

# CORS (for frontend)
CORS_ORIGINS=http://localhost:3000
```

**No Firebase credentials needed anymore!**

### Frontend (.env)

```env
# Backend API URL (optional, defaults to /api)
VITE_API_BASE_URL=/api
```

**No Firebase configuration needed anymore!**

## 🔧 Setup Instructions

### Backend Setup

1. Update environment variables (remove Firebase, add JWT_SECRET_KEY)
2. Install dependencies: `pip install -r requirements.txt`
3. Run database migrations (User model changed - need new migration)
4. Start server: `python run.py`

### Frontend Setup

1. Remove Firebase from environment variables
2. Install dependencies: `npm install` (Firebase will be removed)
3. Start dev server: `npm run dev`

## 🚨 Important Notes

### Security Considerations

1. **JWT Secret Key**: Must be strong and unique in production
   ```python
   # Generate a secure random key:
   import secrets
   print(secrets.token_urlsafe(32))
   ```

2. **HTTPS**: Always use HTTPS in production to protect tokens in transit

3. **Token Storage**: Tokens are stored in localStorage
   - Consider httpOnly cookies for enhanced security (optional upgrade)

4. **Password Hashing**: Uses Werkzeug's secure password hashing (PBKDF2)

### Database Migration

Since the User model changed (removed `firebase_uid`, added `password_hash`), you need to create a new migration:

```bash
cd backend
flask db migrate -m "Switch from Firebase to JWT authentication"
flask db upgrade
```

**Note**: This will require migrating existing users or starting fresh.

## 📚 API Endpoints Reference

### POST `/api/auth/register`
Register new user.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "secure_password",
  "role": "patient"
}
```

**Response:**
```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "role": "patient",
    ...
  },
  "access_token": "eyJ...",
  "refresh_token": "eyJ..."
}
```

### POST `/api/auth/login`
Login user.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "secure_password"
}
```

**Response:**
```json
{
  "message": "Login successful",
  "user": {...},
  "access_token": "eyJ...",
  "refresh_token": "eyJ..."
}
```

### POST `/api/auth/refresh`
Refresh access token.

**Headers:**
```
Authorization: Bearer <refresh_token>
```

**Response:**
```json
{
  "access_token": "eyJ..."
}
```

### GET `/api/auth/user`
Get current user (requires authentication).

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "role": "patient",
  ...
}
```

## ✅ Benefits of JWT Over Firebase

1. **Simpler Setup**: No need for Firebase project
2. **More Control**: Full control over authentication logic
3. **No External Dependencies**: Everything runs on your server
4. **Cost**: No Firebase usage costs
5. **Easier Testing**: Can test authentication without Firebase setup
6. **Stateless**: JWT tokens are stateless, no session storage needed

## 🔄 Migration from Firebase (if needed)

If you had Firebase users, you would need to:
1. Export user data from Firebase
2. Hash their passwords (if available)
3. Import into new User table
4. Or require password reset for all users

For new projects, just start fresh with JWT authentication!

## 📞 Support

For issues, refer to:
- `backend/README.md` - Backend authentication setup
- `frontend/README.md` - Frontend authentication setup

