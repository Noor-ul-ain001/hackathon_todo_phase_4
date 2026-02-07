# UI Specification: Voice Interface

**Component**: Voice Interface
**Version**: 1.0.0
**Created**: 2025-12-27
**Status**: Active Specification

## Purpose

The voice interface enables hands-free task management through speech input and audio output. It is a thin presentation layer with zero business logic, emitting transcribed speech as structured intents to backend agents.

**Constitutional Requirement**: Per constitution.md section 13.2, "Frontend contains NO business logic. All intelligence resides in backend agents."

## Responsibilities

1. Capture audio input from microphone
2. Transcribe speech to text (STT - Speech-to-Text)
3. Emit transcribed text to POST /api/{user_id}/chat
4. Receive agent response
5. Convert response to speech (TTS - Text-to-Speech)
6. Play audio output
7. Provide visual feedback (listening, processing, speaking states)

## Architecture

### Component Hierarchy

```
VoicePage
├── VoiceButton (microphone icon)
├── StatusIndicator (listening | processing | speaking)
├── TranscriptDisplay (optional visual feedback)
└── ErrorBoundary
```

### State Management

**Local State Only**:
- `isListening`: Boolean (microphone active)
- `isProcessing`: Boolean (API request in flight)
- `isSpeaking`: Boolean (TTS audio playing)
- `transcript`: String (current transcription)
- `error`: Error object or null
- `conversationId`: Number or null

**No Redux/Global State**: Voice is stateless - all state derived from API responses.

## User Flow

```
1. User taps microphone button
2. UI starts audio capture
3. UI shows "Listening..." indicator
4. User speaks: "Add meeting tomorrow at 3pm"
5. User stops speaking (silence detected) OR taps button again
6. UI sends audio to STT service (Web Speech API or external)
7. STT returns transcript: "Add meeting tomorrow at 3pm"
8. UI emits intent to backend:
   POST /api/{user_id}/chat
   {
     "conversation_id": <current_conversation_id>,
     "message": "Add meeting tomorrow at 3pm",
     "modality": "voice"
   }
9. UI shows "Processing..." indicator
10. Backend processes request via agents
11. UI receives response:
    {
      "conversation_id": 123,
      "response": "I've added meeting with client to your task list for tomorrow at 3:00 PM.",
      "tool_calls": [...],
      "tasks_affected": [42]
    }
12. UI sends response text to TTS service
13. TTS returns audio
14. UI plays audio
15. UI shows "Speaking..." indicator
16. Audio finishes playing
17. UI returns to idle state
```

## Intent Emission

### Input Examples

**User speaks**: "Show me my tasks for this week"

**STT Output**: "Show me my tasks for this week"

**UI emits**:
```json
{
  "conversation_id": 123,
  "message": "Show me my tasks for this week",
  "modality": "voice",
  "metadata": {
    "voice_confidence": 0.92,
    "client_type": "web"
  }
}
```

### No Client-Side Interpretation

**WRONG** (violates constitution):
```typescript
// ❌ NEVER DO THIS - business logic in frontend
if (transcript.includes("add")) {
  const task = parseTask(transcript);
  createTask(task);
}
```

**CORRECT**:
```typescript
// ✅ Emit raw transcript to backend
const response = await fetch(`/api/${userId}/chat`, {
  method: 'POST',
  body: JSON.stringify({
    message: transcript,
    modality: 'voice',
    metadata: {
      voice_confidence: recognitionConfidence
    }
  })
});
```

## API Integration

### Request Format

```typescript
interface VoiceChatRequest {
  conversation_id: number | null;
  message: string; // Transcribed text
  modality: 'voice';
  metadata?: {
    voice_confidence?: number; // 0.0-1.0
    client_type?: 'web' | 'mobile';
  };
}
```

### Response Format

```typescript
interface ChatResponse {
  conversation_id: number;
  response: string; // Text to be spoken
  tool_calls: ToolCall[];
  tasks_affected: number[];
  metadata: {
    agents_invoked: string[];
    execution_time_ms: number;
  };
}
```

## Speech-to-Text (STT) Integration

### Option 1: Web Speech API (Browser Native)

**Supported Browsers**: Chrome, Edge, Safari (limited)

**Implementation**:
```typescript
function startListening() {
  const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();

  recognition.lang = 'en-US';
  recognition.continuous = false;
  recognition.interimResults = false;

  recognition.onstart = () => {
    setIsListening(true);
  };

  recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript;
    const confidence = event.results[0][0].confidence;

    handleTranscript(transcript, confidence);
  };

  recognition.onerror = (event) => {
    setError(`Speech recognition error: ${event.error}`);
    setIsListening(false);
  };

  recognition.onend = () => {
    setIsListening(false);
  };

  recognition.start();
}
```

### Option 2: External STT Service (Whisper, Google Cloud Speech)

**Use Case**: Mobile apps, non-Chrome browsers, higher accuracy

**Implementation**:
```typescript
async function transcribeAudio(audioBlob: Blob) {
  const formData = new FormData();
  formData.append('audio', audioBlob);

  const response = await fetch('/api/stt/transcribe', {
    method: 'POST',
    body: formData
  });

  const { transcript, confidence } = await response.json();
  return { transcript, confidence };
}
```

### STT Error Handling

| Error | Cause | UI Response |
|-------|-------|-------------|
| no-speech | User didn't speak | "No speech detected. Please try again." |
| aborted | User canceled | Return to idle state |
| audio-capture | Mic permission denied | "Microphone access required. Please enable in settings." |
| network | STT service unavailable | "Speech recognition unavailable. Try typing instead." |

## Text-to-Speech (TTS) Integration

### Option 1: Web Speech API (Browser Native)

**Supported Browsers**: All modern browsers

**Implementation**:
```typescript
function speak(text: string) {
  const utterance = new SpeechSynthesisUtterance(text);

  utterance.lang = 'en-US';
  utterance.rate = 1.0;
  utterance.pitch = 1.0;
  utterance.volume = 1.0;

  utterance.onstart = () => {
    setIsSpeaking(true);
  };

  utterance.onend = () => {
    setIsSpeaking(false);
  };

  utterance.onerror = (event) => {
    console.error('TTS error:', event);
    setIsSpeaking(false);
  };

  window.speechSynthesis.speak(utterance);
}
```

### Option 2: External TTS Service (ElevenLabs, Google Cloud TTS)

**Use Case**: Higher quality voices, custom voice cloning

**Implementation**:
```typescript
async function synthesizeSpeech(text: string) {
  const response = await fetch('/api/tts/synthesize', {
    method: 'POST',
    body: JSON.stringify({ text, voice: 'en-US-Neural' })
  });

  const audioBlob = await response.blob();
  const audioUrl = URL.createObjectURL(audioBlob);

  const audio = new Audio(audioUrl);
  audio.play();

  audio.onplay = () => setIsSpeaking(true);
  audio.onended = () => setIsSpeaking(false);
}
```

## UI Components

### 1. VoicePage

**Props**: None (gets userId from auth context)

**Responsibilities**:
- Manage voice interaction state
- Coordinate STT, API, TTS
- Render child components

**Example**:
```typescript
function VoicePage() {
  const { userId, token } = useAuth();
  const [isListening, setIsListening] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [conversationId, setConversationId] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleTranscript = async (text: string, confidence: number) => {
    setTranscript(text);
    setIsProcessing(true);
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
          modality: 'voice',
          metadata: {
            voice_confidence: confidence
          }
        })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error.message);
      }

      const data = await response.json();
      setConversationId(data.conversation_id);

      // Speak the response
      speak(data.response);
    } catch (err) {
      setError(err.message);
      speak(`Sorry, ${err.message}`);
    } finally {
      setIsProcessing(false);
    }
  };

  const toggleListening = () => {
    if (isListening) {
      stopListening();
    } else {
      startListening();
    }
  };

  return (
    <div className="voice-page">
      <VoiceButton
        isListening={isListening}
        isProcessing={isProcessing}
        isSpeaking={isSpeaking}
        onClick={toggleListening}
      />
      <StatusIndicator
        isListening={isListening}
        isProcessing={isProcessing}
        isSpeaking={isSpeaking}
      />
      <TranscriptDisplay transcript={transcript} />
      {error && <ErrorBanner message={error} />}
    </div>
  );
}
```

### 2. VoiceButton

**Props**:
- `isListening`: boolean
- `isProcessing`: boolean
- `isSpeaking`: boolean
- `onClick`: () => void

**Responsibilities**:
- Display microphone icon
- Animate based on state
- Handle tap to start/stop

**States**:
- **Idle**: Gray microphone icon
- **Listening**: Pulsing red microphone icon
- **Processing**: Spinner
- **Speaking**: Animated sound waves

### 3. StatusIndicator

**Props**:
- `isListening`: boolean
- `isProcessing`: boolean
- `isSpeaking`: boolean

**Responsibilities**:
- Display current state text
- Provide visual feedback

**States**:
- "Tap to speak"
- "Listening..."
- "Processing..."
- "Speaking..."

### 4. TranscriptDisplay

**Props**:
- `transcript`: string

**Responsibilities**:
- Display transcribed text (optional)
- Show what the system heard
- Aid in error correction

## Styling Requirements

### Layout

- Centered microphone button (large, 120px diameter)
- Status text below button
- Optional transcript display at bottom
- Minimal chrome (focus on voice interaction)

### Responsive

- Mobile: Full-screen, portrait-optimized
- Tablet: Centered, max-width 600px
- Desktop: Centered, max-width 800px

### Accessibility

- ARIA labels: "Start voice input" / "Stop voice input"
- Keyboard shortcut: Spacebar to start/stop
- Visual indicators for deaf/hard-of-hearing users (transcript display)
- Screen reader announcements for state changes

## Error Handling

### Microphone Permission Denied

**Error**: User blocks microphone access

**UI Response**:
1. Display message: "Microphone access required"
2. Show instructions to enable in browser settings
3. Provide "Try Again" button

### STT Service Unavailable

**Error**: Speech recognition fails

**UI Response**:
1. Display message: "Speech recognition unavailable"
2. Offer fallback: "Try typing instead" (link to text chat)
3. Log error to monitoring service

### Low Confidence Transcription

**Scenario**: STT confidence < 0.5

**UI Response**:
1. Display transcript to user
2. Ask for confirmation: "Did you say: [transcript]?"
3. Options: "Yes" / "No, let me try again"

### Network Errors

**Error**: API request fails

**UI Response**:
1. Speak error message: "Unable to process request. Please try again."
2. Display error banner
3. Provide retry button

## Performance Considerations

### Audio Latency

- **STT Latency**: <500ms (Web Speech API) or <1s (external)
- **API Latency**: <2s (p95)
- **TTS Latency**: <300ms (Web Speech API) or <1s (external)
- **Total End-to-End**: <3s from speech end to audio response start

### Audio Quality

- **Microphone**: 16 kHz sample rate minimum
- **TTS Output**: 22 kHz sample rate (natural quality)
- **Noise Cancellation**: Browser native or server-side

### Battery Optimization

- Stop audio capture when inactive
- No continuous listening (push-to-talk only)
- Debounce microphone button (prevent accidental taps)

## Security Measures

1. **JWT Validation**: Include Bearer token in Authorization header
2. **HTTPS Only**: Required for microphone access
3. **Audio Privacy**: Audio data discarded after transcription
4. **No Recording**: Do not store audio files
5. **Rate Limiting**: Max 30 requests/minute per user

## Testing Requirements

### Unit Tests

1. VoiceButton toggles isListening state
2. STT success → Transcript emitted to API
3. API response → TTS invoked
4. Error states display correctly

### Integration Tests

1. User speaks → STT → API → TTS → Audio plays
2. Microphone permission denied → Error message displayed
3. STT fails → Fallback to text chat offered
4. API error → Error spoken and displayed

### E2E Tests

1. User says "Add task" → Task created, confirmation spoken
2. User says "Show tasks" → Task list spoken
3. Network failure → Error message spoken
4. Low confidence → Confirmation requested

### Browser Compatibility

- Chrome: Full support (Web Speech API)
- Firefox: Limited STT, full TTS
- Safari: Limited STT, full TTS
- Edge: Full support (Web Speech API)
- Mobile browsers: Native speech APIs preferred

## Acceptance Criteria

1. ✅ Zero business logic in frontend (all intelligence in backend)
2. ✅ Emits raw transcript to /api/{user_id}/chat
3. ✅ Plays agent responses as audio
4. ✅ Handles microphone permission gracefully
5. ✅ Low-latency interaction (<3s end-to-end)
6. ✅ Accessible (keyboard shortcuts, visual indicators)
7. ✅ Works offline fallback to text chat
8. ✅ No audio recording stored

---

## Example Voice Interaction

**User**: [Taps microphone button]

**UI**: "Listening..."

**User**: [Speaks] "Add meeting with client tomorrow at 3pm"

**UI**: [Transcribes] "Add meeting with client tomorrow at 3pm"

**UI**: [Emits to API]
```json
POST /api/user_123/chat
{
  "conversation_id": null,
  "message": "Add meeting with client tomorrow at 3pm",
  "modality": "voice",
  "metadata": {
    "voice_confidence": 0.92
  }
}
```

**Backend Response**:
```json
{
  "conversation_id": 124,
  "response": "I've added meeting with client to your task list for tomorrow at 3:00 PM.",
  "tool_calls": [{
    "tool": "add_task",
    "result": { "task_id": 42 }
  }],
  "tasks_affected": [42]
}
```

**UI**: [TTS speaks] "I've added meeting with client to your task list for tomorrow at 3:00 PM."

**UI**: [Returns to idle state] "Tap to speak"
