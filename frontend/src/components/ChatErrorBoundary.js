import React from 'react'

class ChatErrorBoundary extends React.Component {
  constructor(props) {
    super(props)
    this.state = { hasError: false, error: null }
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error }
  }

  componentDidCatch(error, errorInfo) {
    console.error('Chat Error:', error, errorInfo)
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="flex-1 flex items-center justify-center bg-brand-bg p-8">
          <div className="max-w-md bg-white border-2 border-red-400 rounded-2xl p-6 text-center animate-scaleIn">
            <div className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg className="w-8 h-8 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h3 className="text-xl font-bold text-brand-chat mb-2">Chat Error</h3>
            <p className="text-brand-chat/70 mb-4">
              Something went wrong with the chat interface.
            </p>
            <button
              onClick={() => window.location.reload()}
              className="px-6 py-2 bg-brand-button hover:bg-brand-button-hover text-white rounded-xl transition-all duration-300"
            >
              Reload Chat
            </button>
          </div>
        </div>
      )
    }

    return this.props.children
  }
}

export default ChatErrorBoundary
