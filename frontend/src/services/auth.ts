/**
 * Authentication service for TaskFlow Intelligence Platform
 * Handles API calls for authentication and token management
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export interface User {
  id: string
  email: string
  created_at: string
  updated_at: string
}

export interface LoginCredentials {
  email: string
  password: string
}

export interface RegisterCredentials {
  email: string
  password: string
}

export interface TokenResponse {
  access_token: string
  refresh_token: string
  token_type: string
  expires_in: number
}

class AuthService {
  private readonly ACCESS_TOKEN_KEY = 'taskflow_access_token'
  private readonly REFRESH_TOKEN_KEY = 'taskflow_refresh_token'

  /**
   * Register a new user
   */
  async register(credentials: RegisterCredentials): Promise<TokenResponse> {
    const response = await fetch(`${API_BASE_URL}/api/auth/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(credentials),
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Registration failed')
    }

    const data: TokenResponse = await response.json()
    this.setTokens(data.access_token, data.refresh_token)
    return data
  }

  /**
   * Login with email and password
   */
  async login(credentials: LoginCredentials): Promise<TokenResponse> {
    const response = await fetch(`${API_BASE_URL}/api/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(credentials),
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Login failed')
    }

    const data: TokenResponse = await response.json()
    this.setTokens(data.access_token, data.refresh_token)
    return data
  }

  /**
   * Logout current user
   */
  logout(): void {
    this.clearTokens()
  }

  /**
   * Get current authenticated user
   */
  async getCurrentUser(): Promise<User> {
    const accessToken = this.getAccessToken()
    if (!accessToken) {
      throw new Error('No access token found')
    }

    const response = await fetch(`${API_BASE_URL}/api/auth/me`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${accessToken}`,
        'Content-Type': 'application/json',
      },
    })

    if (!response.ok) {
      if (response.status === 401) {
        // Try to refresh token
        await this.refreshAccessToken()
        return this.getCurrentUser()
      }
      throw new Error('Failed to fetch user info')
    }

    return response.json()
  }

  /**
   * Refresh access token using refresh token
   */
  async refreshAccessToken(): Promise<TokenResponse> {
    const refreshToken = this.getRefreshToken()
    if (!refreshToken) {
      throw new Error('No refresh token found')
    }

    const response = await fetch(`${API_BASE_URL}/api/auth/refresh`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ refresh_token: refreshToken }),
    })

    if (!response.ok) {
      this.clearTokens()
      throw new Error('Failed to refresh token')
    }

    const data: TokenResponse = await response.json()
    this.setTokens(data.access_token, data.refresh_token)
    return data
  }

  /**
   * Store tokens in localStorage
   */
  setTokens(accessToken: string, refreshToken: string): void {
    if (typeof window !== 'undefined') {
      localStorage.setItem(this.ACCESS_TOKEN_KEY, accessToken)
      localStorage.setItem(this.REFRESH_TOKEN_KEY, refreshToken)
    }
  }

  /**
   * Get access token from localStorage
   */
  getAccessToken(): string | null {
    if (typeof window !== 'undefined') {
      return localStorage.getItem(this.ACCESS_TOKEN_KEY)
    }
    return null
  }

  /**
   * Get refresh token from localStorage
   */
  getRefreshToken(): string | null {
    if (typeof window !== 'undefined') {
      return localStorage.getItem(this.REFRESH_TOKEN_KEY)
    }
    return null
  }

  /**
   * Clear all tokens
   */
  clearTokens(): void {
    if (typeof window !== 'undefined') {
      localStorage.removeItem(this.ACCESS_TOKEN_KEY)
      localStorage.removeItem(this.REFRESH_TOKEN_KEY)
    }
  }

  /**
   * Check if user is authenticated
   */
  isAuthenticated(): boolean {
    return !!this.getAccessToken()
  }
}

export const authService = new AuthService()
