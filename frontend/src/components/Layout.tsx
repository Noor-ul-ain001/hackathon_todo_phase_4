/**
 * Main Layout Component for TaskFlow Intelligence Platform
 * Conditionally shows sidebar only for authenticated users
 */

import { FC, ReactNode } from 'react'
import { useAuth } from '@/contexts/AuthContext'
import Sidebar from '@/components/Sidebar'

interface LayoutProps {
  children: ReactNode
}

const Layout: FC<LayoutProps> = ({ children }) => {
  const { isAuthenticated, loading } = useAuth()

  // If loading, show minimal layout
  if (loading) {
    return (
      <div className="min-h-screen bg-brand-bg">
        {children}
      </div>
    )
  }

  // If authenticated, show layout with sidebar
  if (isAuthenticated) {
    return (
      <div className="min-h-screen bg-brand-bg flex">
        <Sidebar />
        <div className="flex-1 flex flex-col overflow-hidden">
          {children}
        </div>
      </div>
    )
  }

  // If not authenticated, show layout without sidebar
  return (
    <div className="min-h-screen bg-brand-bg">
      {children}
    </div>
  )
}

export default Layout
