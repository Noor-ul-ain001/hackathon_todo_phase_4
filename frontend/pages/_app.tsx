/**
 * Main App Component for TaskFlow Intelligence Platform
 * Provides global providers and layout
 */

import { FC } from 'react'
import type { AppProps } from 'next/app'
import { AuthProvider } from '@/contexts/AuthContext'
import '../styles/globals.css'
import '../styles/animations.css'
import Layout from '@/components/Layout'

const MyApp: FC<AppProps> = ({ Component, pageProps }) => {
  return (
    <AuthProvider>
      <Layout>
        <Component {...pageProps} />
      </Layout>
    </AuthProvider>
  )
}

export default MyApp
