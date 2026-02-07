import Head from 'next/head'
import { useState } from 'react'

export default function Support() {
  const [activeTab, setActiveTab] = useState('contact')
  const [expandedFaq, setExpandedFaq] = useState(null)
  const [ticketForm, setTicketForm] = useState({
    name: '',
    email: '',
    subject: '',
    issueType: 'technical',
    description: ''
  })
  const [ticketSubmitted, setTicketSubmitted] = useState(false)
  const [newFaq, setNewFaq] = useState({ question: '', answer: '' })
  const [faqs, setFaqs] = useState([
    {
      id: 1,
      question: "How do I create a new task?",
      answer: "You can create a new task by clicking the 'Add Task' button in the dashboard or by using the AI chat assistant. Simply type a command like 'Add task: Review documentation' and the AI will create the task for you."
    },
    {
      id: 2,
      question: "Can I set due dates for tasks?",
      answer: "Yes, you can set due dates when creating or editing tasks. The AI assistant can also parse natural language to set due dates, for example: 'Add task: Submit report due tomorrow'."
    },
    {
      id: 3,
      question: "How do I mark a task as complete?",
      answer: "You can mark a task as complete by clicking the checkbox next to the task in the dashboard, or by using the AI chat assistant with commands like 'Complete task #3' or 'Mark task Review documentation as done'."
    },
    {
      id: 4,
      question: "Can I collaborate with others on tasks?",
      answer: "Yes, TaskFlow supports team collaboration. You can assign tasks to team members, add comments, and track progress together. Create a project to start collaborating with your team."
    }
  ])

  const supportOptions = [
    {
      id: 1,
      title: "Email Support",
      description: "Send us an email and we'll respond within 24 hours.",
      contact: "support@taskflow.example.com",
      icon: (
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
        </svg>
      )
    },
    {
      id: 2,
      title: "Live Chat",
      description: "Chat with our support team in real-time during business hours.",
      contact: "Start Chat",
      icon: (
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
        </svg>
      )
    },
    {
      id: 3,
      title: "Documentation",
      description: "Browse our comprehensive documentation for detailed guides.",
      contact: "View Documentation",
      icon: (
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      )
    },
    {
      id: 4,
      title: "Community Forum",
      description: "Connect with other users and find solutions in our community forum.",
      contact: "Visit Forum",
      icon: (
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0z" />
        </svg>
      )
    }
  ]

  const handleFaqToggle = (id) => {
    setExpandedFaq(expandedFaq === id ? null : id)
  }

  const handleTicketSubmit = (e) => {
    e.preventDefault()
    // In a real app, this would submit to an API
    console.log('Ticket submitted:', ticketForm)
    setTicketSubmitted(true)
    // Reset form
    setTicketForm({
      name: '',
      email: '',
      subject: '',
      issueType: 'technical',
      description: ''
    })
    // Reset success message after 5 seconds
    setTimeout(() => setTicketSubmitted(false), 5000)
  }

  const handleTicketChange = (e) => {
    const { name, value } = e.target
    setTicketForm(prev => ({
      ...prev,
      [name]: value
    }))
  }

  const handleAddFaq = (e) => {
    e.preventDefault()
    if (newFaq.question.trim() && newFaq.answer.trim()) {
      const newFaqItem = {
        id: faqs.length + 1,
        question: newFaq.question,
        answer: newFaq.answer
      }
      setFaqs(prev => [...prev, newFaqItem])
      setNewFaq({ question: '', answer: '' })
    }
  }

  const handleNewFaqChange = (e) => {
    const { name, value } = e.target
    setNewFaq(prev => ({
      ...prev,
      [name]: value
    }))
  }

  return (
    <>
      <Head>
        <title>Support - TaskFlow</title>
        <meta name="description" content="TaskFlow Support Center" />
      </Head>

      {/* Header */}
      <div className="bg-brand-card-bg/80 backdrop-blur-sm border-b border-brand-card-border px-4 py-3 md:px-8 md:py-6 animate-fadeInDown">
        <h1 className="text-3xl font-bold text-white mb-1">
          <span className="bg-gradient-to-r from-brand-button to-brand-button-hover bg-clip-text text-transparent">Support</span>
        </h1>
        <p className="text-white/70 text-sm">Get help with TaskFlow</p>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-y-auto px-4 py-3 md:px-8 md:py-6">
        <div className="max-w-4xl mx-auto">
          {/* Support Tabs */}
          <div className="flex space-x-8 mb-8 border-b border-brand-card-border/50">
            {['contact', 'faq', 'troubleshooting', 'submit-ticket'].map((tab, index) => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`pb-4 px-1 capitalize font-semibold transition-all animate-fadeInDown ${
                  activeTab === tab
                    ? 'text-brand-button border-b-2 border-brand-button'
                    : 'text-white/70 hover:text-brand-button'
                }`}
                style={{animationDelay: `${index * 0.1}s`}}
              >
                {tab === 'submit-ticket' ? 'Submit Ticket' : tab.charAt(0).toUpperCase() + tab.slice(1)}
              </button>
            ))}
          </div>

          {/* Tab Content */}
          <div className="bg-brand-card-bg/50 backdrop-blur-sm border border-brand-card-border rounded-2xl p-4 md:p-6 hover-lift transition-all animate-fadeInUp">
            {activeTab === 'contact' && (
              <div>
                <h2 className="text-xl font-bold text-white mb-6">Get in Touch</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {supportOptions.map((option, index) => (
                    <div
                      key={option.id}
                      className="bg-brand-card-bg/30 backdrop-blur-sm border border-brand-card-border/50 rounded-xl p-6 hover-lift transition-all animate-fadeInUp"
                      style={{animationDelay: `${index * 0.1}s`}}
                    >
                      <div className="w-12 h-12 bg-brand-button/20 rounded-lg flex items-center justify-center mb-4 shadow-md">
                        {option.icon}
                      </div>
                      <h3 className="text-lg font-semibold text-white mb-2">{option.title}</h3>
                      <p className="text-white/70 mb-4">{option.description}</p>
                      <button className="text-brand-button hover:text-brand-button-hover font-semibold transition-colors">
                        {option.contact}
                      </button>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {activeTab === 'faq' && (
              <div>
                <h2 className="text-xl font-bold text-white mb-6">Frequently Asked Questions</h2>

                {/* Add new FAQ form */}
                <div className="mb-8 bg-brand-card-bg/30 backdrop-blur-sm border border-brand-card-border/50 rounded-xl p-6">
                  <h3 className="text-lg font-semibold text-white mb-4">Add a new FAQ</h3>
                  <form onSubmit={handleAddFaq} className="space-y-4">
                    <div>
                      <label className="block text-white/80 mb-2">Question</label>
                      <input
                        type="text"
                        name="question"
                        value={newFaq.question}
                        onChange={handleNewFaqChange}
                        className="w-full px-4 py-2 rounded-lg bg-brand-card-bg/50 border border-brand-card-border text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-brand-button"
                        placeholder="Enter a frequently asked question"
                      />
                    </div>
                    <div>
                      <label className="block text-white/80 mb-2">Answer</label>
                      <textarea
                        name="answer"
                        value={newFaq.answer}
                        onChange={handleNewFaqChange}
                        rows="3"
                        className="w-full px-4 py-2 rounded-lg bg-brand-card-bg/50 border border-brand-card-border text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-brand-button"
                        placeholder="Enter the answer"
                      />
                    </div>
                    <button
                      type="submit"
                      className="px-6 py-2 bg-brand-button hover:bg-brand-button-hover text-white rounded-lg font-semibold transition-colors"
                    >
                      Add FAQ
                    </button>
                  </form>
                </div>

                {/* FAQ List */}
                <div className="space-y-4">
                  {faqs.map((faq, index) => (
                    <div
                      key={faq.id}
                      className="border-b border-brand-card-border/30 pb-4 last:border-0 animate-fadeInLeft"
                      style={{animationDelay: `${index * 0.1}s`}}
                    >
                      <div
                        className="flex justify-between items-start cursor-pointer"
                        onClick={() => handleFaqToggle(faq.id)}
                      >
                        <h3 className="text-lg font-semibold text-white">{faq.question}</h3>
                        <button className="text-brand-button hover:text-brand-button-hover">
                          {expandedFaq === faq.id ? '−' : '+'}
                        </button>
                      </div>
                      {expandedFaq === faq.id && (
                        <div className="mt-2 pt-2">
                          <p className="text-white/70">{faq.answer}</p>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {activeTab === 'troubleshooting' && (
              <div>
                <h2 className="text-xl font-bold text-white mb-6">Troubleshooting</h2>
                <div className="space-y-6">
                  <div className="animate-fadeInLeft">
                    <h3 className="text-lg font-semibold text-white mb-2">Login Issues</h3>
                    <p className="text-white/70 mb-4">If you're having trouble logging in, try clearing your browser cache and cookies. If the problem persists, reset your password using the "Forgot Password" link.</p>
                  </div>

                  <div className="animate-fadeInLeft animate-delay-100">
                    <h3 className="text-lg font-semibold text-white mb-2">Sync Problems</h3>
                    <p className="text-white/70 mb-4">If your tasks aren't syncing across devices, check your internet connection and ensure you're logged into the same account on all devices.</p>
                  </div>

                  <div className="animate-fadeInLeft animate-delay-200">
                    <h3 className="text-lg font-semibold text-white mb-2">Performance Issues</h3>
                    <p className="text-white/70 mb-4">For slow performance, try using a different browser or updating your current browser to the latest version. Also, ensure you have sufficient storage space on your device.</p>
                  </div>

                  <div className="animate-fadeInLeft animate-delay-300">
                    <h3 className="text-lg font-semibold text-white mb-2">Feature Requests</h3>
                    <p className="text-white/70 mb-4">We welcome feature requests! Submit your ideas through our feedback form or vote on existing suggestions in our community forum.</p>
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'submit-ticket' && (
              <div>
                <h2 className="text-xl font-bold text-white mb-6">Submit a Support Ticket</h2>

                {ticketSubmitted ? (
                  <div className="bg-green-500/20 border border-green-500/50 rounded-xl p-6 mb-6">
                    <div className="flex items-center">
                      <svg className="w-6 h-6 text-green-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                      </svg>
                      <h3 className="text-lg font-semibold text-green-500">Ticket Submitted Successfully!</h3>
                    </div>
                    <p className="text-white/70 mt-2">We've received your ticket and will respond within 24 hours.</p>
                  </div>
                ) : (
                  <form onSubmit={handleTicketSubmit} className="space-y-6">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      <div>
                        <label className="block text-white/80 mb-2">Full Name</label>
                        <input
                          type="text"
                          name="name"
                          value={ticketForm.name}
                          onChange={handleTicketChange}
                          required
                          className="w-full px-4 py-2 rounded-lg bg-brand-card-bg/50 border border-brand-card-border text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-brand-button"
                          placeholder="Enter your full name"
                        />
                      </div>
                      <div>
                        <label className="block text-white/80 mb-2">Email Address</label>
                        <input
                          type="email"
                          name="email"
                          value={ticketForm.email}
                          onChange={handleTicketChange}
                          required
                          className="w-full px-4 py-2 rounded-lg bg-brand-card-bg/50 border border-brand-card-border text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-brand-button"
                          placeholder="Enter your email"
                        />
                      </div>
                    </div>

                    <div>
                      <label className="block text-white/80 mb-2">Subject</label>
                      <input
                        type="text"
                        name="subject"
                        value={ticketForm.subject}
                        onChange={handleTicketChange}
                        required
                        className="w-full px-4 py-2 rounded-lg bg-brand-card-bg/50 border border-brand-card-border text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-brand-button"
                        placeholder="Briefly describe your issue"
                      />
                    </div>

                    <div>
                      <label className="block text-white/80 mb-2">Issue Type</label>
                      <select
                        name="issueType"
                        value={ticketForm.issueType}
                        onChange={handleTicketChange}
                        className="w-full px-4 py-2 rounded-lg bg-brand-card-bg/50 border border-brand-card-border text-white focus:outline-none focus:ring-2 focus:ring-brand-button"
                      >
                        <option value="technical">Technical Issue</option>
                        <option value="billing">Billing Question</option>
                        <option value="feature">Feature Request</option>
                        <option value="account">Account Issue</option>
                        <option value="other">Other</option>
                      </select>
                    </div>

                    <div>
                      <label className="block text-white/80 mb-2">Description</label>
                      <textarea
                        name="description"
                        value={ticketForm.description}
                        onChange={handleTicketChange}
                        required
                        rows="5"
                        className="w-full px-4 py-2 rounded-lg bg-brand-card-bg/50 border border-brand-card-border text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-brand-button"
                        placeholder="Please provide detailed information about your issue"
                      />
                    </div>

                    <button
                      type="submit"
                      className="px-6 py-3 bg-brand-button hover:bg-brand-button-hover text-white rounded-lg font-semibold transition-colors"
                    >
                      Submit Ticket
                    </button>
                  </form>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </>
  )
}