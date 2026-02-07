# UI Specification: Web Chat Interface

**Component**: Web Chat Interface
**Version**: 1.0.0
**Created**: 2025-12-27
**Status**: Active Specification

## Purpose

The web chat interface provides a text-based conversational UI for task management. It is a thin presentation layer with zero business logic, emitting structured intents to backend agents.

**Constitutional Requirement**: Per constitution.md section 13.2, "Frontend contains NO business logic. All intelligence resides in backend agents."

## Responsibilities

1. Render conversation history
2. Accept user text input
3. Emit structured intent to POST /api/{user_id}/chat
4. Display agent responses
5. Show typing indicators and loading states
6. Handle errors gracefully

## Architecture

### Component Hierarchy

```
ChatPage
├── ConversationHeader
│   └── UserInfo
├── MessageList
│   ├── UserMessage (multiple)
│   └── AssistantMessage (multiple)
├── InputArea
│   ├── TextInput
│   ├── SendButton
│   └── TypingIndicator
└── ErrorBoundary
```

### State Management

**Local State Only**:
- `messages`: Array of conversation messages
- `inputText`: Current user input
- `isLoading`: Boolean for API request state
- `error`: Error object or null
- `conversationId`: Number or null

**No Redux/Global State**: Chat is stateless - all state derived from API responses.

## User Flow

```
1. User enters text in input field
2. User presses Enter or clicks Send button
3. UI emits intent to backend:
   POST /api/{user_id}/chat
   {
     "conversation_id": <current_conversation_id>,
     "message": "<user_input>",
     "modality": "text"
   }
4. UI shows typing indicator
5. Backend processes request via agents
6. UI receives response:
   {
     "conversation_id": 123,
     "response": "Task created successfully",
     "tool_calls": [...],
     "tasks_affected": [42]
   }
7. UI appends user message and assistant response to messages array
8. UI clears input field
9. UI hides typing indicator
```

## Intent Emission

### Input Examples

**User types**: "Add meeting tomorrow at 3pm"

**UI emits**:
```json
{
  "conversation_id": null,
  "message": "Add meeting tomorrow at 3pm",
  "modality": "text",
  "metadata": {
    "client_type": "web"
  }
}
```

**User types**: "Show my tasks"

**UI emits**:
```json
{
  "conversation_id": 123,
  "message": "Show my tasks",
  "modality": "text"
}
```

### No Client-Side Parsing

**WRONG** (violates constitution):
```typescript
// ❌ NEVER DO THIS - business logic in frontend
if (message.includes("add")) {
  const title = extractTitle(message);
  createTask(title);
}
```

**CORRECT**:
```typescript
// ✅ Emit raw input to backend
const response = await fetch(`/api/${userId}/chat`, {
  method: 'POST',
  body: JSON.stringify({
    message: userInput,
    modality: 'text'
  })
});
```

## API Integration

### Request Format

```typescript
interface ChatRequest {
  conversation_id: number | null;
  message: string;
  modality: 'text';
  metadata?: {
    client_type?: 'web';
  };
}
```

### Response Format

```typescript
interface ChatResponse {
  conversation_id: number;
  response: string;
  tool_calls: ToolCall[];
  tasks_affected: number[];
  metadata: {
    agents_invoked: string[];
    execution_time_ms: number;
  };
}

interface ToolCall {
  tool: string;
  arguments: Record<string, any>;
  result: Record<string, any>;
}
```

### Error Format

```typescript
interface ErrorResponse {
  error: {
    code: string;
    message: string;
    details?: Record<string, any>;
    timestamp: string;
  };
}
```

## UI Components

### 1. ChatPage

**Props**: None (gets userId from auth context)

**Responsibilities**:
- Manage conversation state
- Handle API requests
- Render child components

**Example**:
```typescript
function ChatPage() {
  const { userId } = useAuth();
  const [messages, setMessages] = useState<Message[]>([]);
  const [conversationId, setConversationId] = useState<number | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSend = async (text: string) => {
    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch(`/api/${userId}/chat`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          conversation_id: conversationId,
          message: text,
          modality: 'text'
        })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error.message);
      }

      const data = await response.json();

      setMessages(prev => [
        ...prev,
        { role: 'user', content: text },
        { role: 'assistant', content: data.response }
      ]);
      setConversationId(data.conversation_id);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="chat-page">
      <ConversationHeader userId={userId} />
      <MessageList messages={messages} />
      <InputArea
        onSend={handleSend}
        isLoading={isLoading}
        error={error}
      />
    </div>
  );
}
```

### 2. MessageList

**Props**:
- `messages`: Message[]

**Responsibilities**:
- Render scrollable message history
- Auto-scroll to bottom on new message
- Display user and assistant messages with distinct styling

**Example**:
```typescript
interface Message {
  role: 'user' | 'assistant';
  content: string;
}

function MessageList({ messages }: { messages: Message[] }) {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <div className="message-list">
      {messages.map((msg, idx) => (
        msg.role === 'user'
          ? <UserMessage key={idx} content={msg.content} />
          : <AssistantMessage key={idx} content={msg.content} />
      ))}
      <div ref={messagesEndRef} />
    </div>
  );
}
```

### 3. InputArea

**Props**:
- `onSend`: (text: string) => void
- `isLoading`: boolean
- `error`: string | null

**Responsibilities**:
- Capture user text input
- Emit intent on Enter or Send click
- Disable input during loading
- Display errors

**Example**:
```typescript
function InputArea({ onSend, isLoading, error }: InputAreaProps) {
  const [text, setText] = useState('');

  const handleSubmit = () => {
    if (text.trim() && !isLoading) {
      onSend(text);
      setText('');
    }
  };

  const handleKeyPress = (e: KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <div className="input-area">
      {error && <ErrorBanner message={error} />}
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        onKeyPress={handleKeyPress}
        placeholder="Type your message..."
        disabled={isLoading}
      />
      <button onClick={handleSubmit} disabled={isLoading || !text.trim()}>
        {isLoading ? <Spinner /> : 'Send'}
      </button>
      {isLoading && <TypingIndicator />}
    </div>
  );
}
```

## Styling Requirements

### Layout

- Full-height viewport (100vh)
- Fixed header (user info)
- Scrollable message area (flex-grow)
- Fixed input area (bottom)

### Responsive Breakpoints

- Mobile: < 768px (single column, full width)
- Tablet: 768px - 1024px (max-width 800px, centered)
- Desktop: > 1024px (max-width 1000px, centered)

### Accessibility

- ARIA labels on all interactive elements
- Keyboard navigation support (Tab, Enter, Escape)
- Focus indicators visible
- Screen reader announcements for new messages

## Error Handling

### Network Errors

**Error**: Fetch fails (network down)

**UI Response**:
1. Display error banner: "Unable to send message. Check your connection."
2. Retry button
3. Keep user's unsent message in input field

### Authentication Errors

**Error**: 401 Unauthorized

**UI Response**:
1. Redirect to login page
2. Save draft message to localStorage
3. Restore draft after successful login

### Validation Errors

**Error**: 400 Validation Error

**UI Response**:
1. Display error message from backend
2. Highlight problematic field (if applicable)
3. Do not clear user input

### Agent Errors

**Error**: 500 Agent Error

**UI Response**:
1. Display friendly message: "Something went wrong. Please try again."
2. Retry button
3. Log error to monitoring service

## Performance Considerations

### Message Pagination

- Load last 50 messages initially
- Lazy load older messages on scroll up
- Virtualize message list for >100 messages

### Optimistic Updates

**Optional Enhancement** (Phase 6+):
- Immediately append user message to UI
- Show "sending..." indicator
- On success: Replace with confirmed message
- On error: Mark as failed, show retry button

### Debouncing

- No typing indicators (stateless architecture)
- No "user is typing" broadcasts

## Security Measures

1. **JWT Validation**: Include Bearer token in Authorization header
2. **Input Sanitization**: Sanitize HTML in message display (XSS prevention)
3. **HTTPS Only**: Enforce secure connection
4. **CSRF Protection**: Include CSRF token in requests
5. **Rate Limiting**: Client-side throttle (max 1 request/second)

## Testing Requirements

### Unit Tests

1. InputArea emits correct intent on Send click
2. InputArea emits correct intent on Enter press
3. MessageList renders messages correctly
4. Error banner displays on API failure
5. Loading state disables input

### Integration Tests

1. Send message → API called with correct payload
2. Receive response → Messages updated correctly
3. conversation_id persists across messages
4. Error response → Error banner displayed
5. Retry → API called again

### E2E Tests

1. User sends "Add task" → Task created, confirmation displayed
2. User sends "Show tasks" → Task list displayed
3. Network failure → Error message, retry works
4. JWT expires → Redirect to login

## Acceptance Criteria

1. ✅ Zero business logic in frontend (all intelligence in backend)
2. ✅ Emits raw user input to /api/{user_id}/chat
3. ✅ Displays agent responses verbatim
4. ✅ Handles all error types gracefully
5. ✅ Accessible (WCAG 2.1 AA)
6. ✅ Responsive (mobile, tablet, desktop)
7. ✅ Conversation persists across page refreshes
8. ✅ JWT authentication enforced

---

## Example Conversation Flow

**User Input**: "Add meeting with client tomorrow at 3pm"

**UI Action**:
```json
POST /api/user_123/chat
{
  "conversation_id": null,
  "message": "Add meeting with client tomorrow at 3pm",
  "modality": "text"
}
```

**Backend Response**:
```json
{
  "conversation_id": 124,
  "response": "I've added 'Meeting with client' to your task list for tomorrow at 3:00 PM.",
  "tool_calls": [{
    "tool": "add_task",
    "arguments": {
      "user_id": "user_123",
      "title": "Meeting with client",
      "due_date": "2025-12-28",
      "due_time": "15:00"
    },
    "result": {
      "task_id": 42,
      "status": "created"
    }
  }],
  "tasks_affected": [42]
}
```

**UI Display**:
```
User: Add meeting with client tomorrow at 3pm