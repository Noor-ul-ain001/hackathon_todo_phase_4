/**
 * Protected Route Component for TaskFlow Intelligence Platform
 * Wraps pages that require authentication
 */

import { FC, ReactNode, useEffect } from 'react'
import { useRouter } from 'next/router'
import { useAuth } from '@/contexts/AuthContext'

interface ProtectedRouteProps {
  children: ReactNode
}

const ProtectedRoute: FC<ProtectedRouteProps> = ({ children }) => {
  const router = useRouter()
  const { isAuthenticated, loading } = useAuth()

  useEffect(() => {
    if (!loading && !isAuthenticated) {
      // Redirect to login page with return URL
      router.push(`/login?returnUrl=${encodeURIComponent(router.asPath)}`)
    }
  }, [isAuthenticated, loading, router])

  // Show loading state
  if (loading) {
    return (
      <div className="min-h-screen bg-brand-bg flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-brand-button border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-white">Loading...</p>
        </div>
      </div>
    )
  }

  // Show nothing while redirecting
  if (!isAuthenticated) {
    return null
  }

  // Render protected content
  return <>{children}</>
}

export default ProtectedRoute
