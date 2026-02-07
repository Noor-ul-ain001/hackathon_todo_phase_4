# Todo Intelligence Platform - Frontend

This is the frontend for the Todo Intelligence Platform, built with Next.js and OpenAI ChatKit.

## Features

- Modern chat interface for task management
- Natural language processing for task commands
- Responsive design for all devices
- Real-time conversation with AI assistant

## Getting Started

### Prerequisites

- Node.js 18+
- npm or yarn

### Installation

1. Install dependencies:

```bash
npm install
```

2. Create a `.env.local` file with your environment variables:

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Running the Development Server

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

### Building for Production

```bash
npm run build
```

## Environment Variables

- `NEXT_PUBLIC_API_URL` - The URL of your backend API server

## API Integration

The frontend communicates with the backend API at `/api/{user_id}/chat` to send and receive messages from the AI assistant.

## Example Commands

- "Add buy groceries to my list"
- "What tasks do I have?"
- "Mark task 1 as complete"
- "Delete the groceries task"
- "Update task 1 to 'Call mom tomorrow'"