/**
 * Sidebar Navigation Component for TaskFlow Intelligence Platform
 * Provides main navigation with icons
 */

import { FC } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/router'
import { useAuth } from '@/contexts/AuthContext'

interface NavItem {
  id: string
  label: string
  icon: JSX.Element
  href: string
}

const Sidebar: FC = () => {
  const router = useRouter()
  const { logout } = useAuth()

  const navItems: NavItem[] = [
    {
      id: 'dashboard',
      label: 'Dashboard',
      href: '/dashboard',
      icon: (
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
        </svg>
      )
    },
    {
      id: 'projects',
      label: 'Projects',
      href: '/projects',
      icon: (
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" />
        </svg>
      )
    },
    {
      id: 'analytics',
      label: 'Analytics',
      href: '/analytics',
      icon: (
        <svg className='w-6 h-6' fill='none' stroke='currentColor' viewBox='0 0 24 24'>
          <path strokeLinecap='round' strokeLinejoin='round' strokeWidth={2} d='M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z' />
        </svg>
      )
    },
    {
      id: 'chat',
      label: 'AI Chat',
      href: '/chat',
      icon: (
        <svg className='w-6 h-6' fill='none' stroke='currentColor' viewBox='0 0 24 24'>
          <path strokeLinecap='round' strokeLinejoin='round' strokeWidth={2} d='M13 10V3L4 14h7v7l9-11h-7z' />
        </svg>
      )
    },
    {
      id: 'support',
      label: 'Support',
      href: '/support',
      icon: (
        <svg className='w-6 h-6' fill='none' stroke='currentColor' viewBox='0 0 24 24'>
          <path strokeLinecap='round' strokeLinejoin='round' strokeWidth={2} d='M18.364 5.636l-3.536 3.536m0 5.656l3.536 3.536M9.172 9.172L5.636 5.636m3.536 9.192l-3.536 3.536M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-5 0a4 4 0 11-8 0 4 4 0 018 0z' />
        </svg>
      )
    },
    {
      id: 'settings',
      label: 'Settings',
      href: '/settings',
      icon: (
        <svg className='w-6 h-6' fill='none' stroke='currentColor' viewBox='0 0 24 24'>
          <path strokeLinecap='round' strokeLinejoin='round' strokeWidth={2} d='M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z' />
          <path strokeLinecap='round' strokeLinejoin='round' strokeWidth={2} d='M15 12a3 3 0 11-6 0 3 3 0 016 0z' />
        </svg>
      )
    }
  ]

  const isActive = (href: string) => router.pathname === href

  const handleLogout = () => {
    logout()
    router.push('/')
  }

  return (
    <div className="w-20 bg-brand-card-bg border-r border-brand-card-border flex flex-col items-center py-6 space-y-1 animate-slideInLeft">
      {/* Logo */}
      <Link href="/dashboard">
        <div className="w-12 h-12 bg-gradient-to-br from-brand-button to-brand-button-hover rounded-xl flex items-center justify-center mb-8 cursor-pointer hover:shadow-lg hover:shadow-brand-button/30 transition-all hover-lift animate-pulse">
          <svg className="w-7 h-7 text-white" fill="currentColor" viewBox="0 0 20 20">
            <path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z" />
            <path fillRule="evenodd" d="M4 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v11a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm9.707 5.707a1 1 0 00-1.414-1.414L9 12.586l-1.293-1.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
          </svg>
        </div>
      </Link>

      {/* Navigation Items */}
      <div className="flex-1 flex flex-col space-y-2 w-full px-3 stagger-children">
        {navItems.map((item) => (
          <Link key={item.id} href={item.href}>
            <div
              className={`w-14 h-14 rounded-xl flex items-center justify-center cursor-pointer transition-all group relative hover-lift ${
                isActive(item.href) ? 'bg-brand-button/10 text-brand-button animate-scaleIn' : 'text-white/60 hover:text-brand-button hover:bg-brand-card-border'
              }`}
              title={item.label}
            >
              {item.icon}
              {isActive(item.href) && (
                <div className='absolute left-0 w-1 h-6 bg-brand-button rounded-r-full shadow-[0_0_8px_rgba(219, 118, 248, 0.8)]' />
              )}

              {/* Tooltip */}
              <div className="absolute left-full ml-4 px-3 py-2 bg-brand-card-bg text-white text-sm rounded-lg opacity-0 group-hover:opacity-100 pointer-events-none whitespace-nowrap transition-all z-50 border border-brand-card-border transform group-hover:translate-x-1">
                {item.label}
                <div className="absolute right-full top-1/2 -translate-y-1/2 border-8 border-transparent border-r-brand-card-bg"></div>
              </div>
            </div>
          </Link>
        ))}
      </div>

      {/* Logout Button */}
      <button
        onClick={handleLogout}
        className="w-14 h-14 rounded-xl flex items-center justify-center text-red-400 hover:bg-red-500/10 hover:border-2 hover:border-red-500 transition-all group relative hover-lift animate-fadeIn animate-delay-500"
        title="Logout"
      >
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
        </svg>

        {/* Tooltip */}
        <div className="absolute left-full ml-4 px-3 py-2 bg-brand-card-bg text-white text-sm rounded-lg opacity-0 group-hover:opacity-100 pointer-events-none whitespace-nowrap transition-opacity z-50 border border-brand-card-border">
          Logout
          <div className="absolute right-full top-1/2 -translate-y-1/2 border-8 border-transparent border-r-brand-card-bg"></div>
        </div>
      </button>
    </div>
  )
}

export default Sidebar
