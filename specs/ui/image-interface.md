# UI Specification: Image Interface

**Component**: Image Interface
**Version**: 1.0.0
**Created**: 2025-12-27
**Status**: Active Specification

## Purpose

The image interface enables task creation from photos of sticky notes, whiteboards, calendar screenshots, or handwritten notes. It is a thin presentation layer with zero business logic, emitting captured images to backend agents for processing.

**Constitutional Requirement**: Per constitution.md section 13.2, "Frontend contains NO business logic. All intelligence resides in backend agents."

## Responsibilities

1. Capture image via camera or file upload
2. Display image preview
3. Emit base64-encoded image to POST /api/{user_id}/chat
4. Receive extracted task details from Visual Context Agent
5. Display confirmation with editable fields
6. Allow user to confirm or reject task creation

## Architecture

### Component Hierarchy

```
ImagePage
├── CaptureArea
│   ├── CameraButton
│   ├── UploadButton
│   └── ImagePreview
├── ProcessingIndicator
├── ExtractedDataDisplay
│   ├── TaskFields (title, due_date, priority, etc.)
│   └── ConfirmationButtons (Confirm | Retry | Cancel)
└── ErrorBoundary
```

### State Management

**Local State Only**:
- `imageData`: Base64 string or null
- `isProcessing`: Boolean (API request in flight)
- `extractedData`: Object with task fields or null
- `error`: Error object or null
- `conversationId`: Number or null

**No Redux/Global State**: Image processing is stateless.

## User Flow

```
1. User taps "Camera" or "Upload" button
2. User captures photo or selects file
3. UI displays image preview
4. User taps "Process" button
5. UI emits image to backend:
   POST /api/{user_id}/chat
   {
     "conversation_id": null,
     "message": "",
     "modality": "image",
     "metadata": {
       "image_data": "data:image/png;base64,iVBORw0KGgo..."
     }
   }
6. UI shows "Processing..." indicator
7. Backend invokes Visual Context Agent
8. Visual Context Agent:
   - Extracts text via OCR
   - Parses task details (title, due date, priority)
   - Invokes Task Reasoning Agent
9. Backend returns structured task data:
   {
     "conversation_id": 125,
     "response": "I found a task in your image",
     "tool_calls": [],
     "tasks_affected": [],
     "metadata": {
       "extracted_task": {
         "title": "Quarterly Review Meeting",
         "due_date": "2025-12-30",
         "due_time": "14:00",
         "priority": "high",
         "confidence": 0.75
       }
     }
   }
10. UI displays extracted data in editable form
11. User reviews and optionally edits fields
12. User taps "Confirm" button
13. UI emits confirmation:
    POST /api/{user_id}/chat
    {
      "conversation_id": 125,
      "message": "create task",
      "modality": "text",
      "metadata": {
        "confirmed_task": { ... }
      }
    }
14. Backend creates task via Task Reasoning Agent
15. UI displays success: "Task created"
16. Image discarded (privacy)
```

## Intent Emission

### Phase 1: Image Submission

**User action**: Capture/upload image

**UI emits**:
```json
{
  "conversation_id": null,
  "message": "",
  "modality": "image",
  "metadata": {
    "image_data": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...",
    "client_type": "mobile"
  }
}
```

### Phase 2: Confirmation

**User action**: Confirm extracted task data

**UI emits**:
```json
{
  "conversation_id": 125,
  "message": "create task with confirmed details",
  "modality": "text",
  "metadata": {
    "confirmed_task": {
      "title": "Quarterly Review Meeting",
      "due_date": "2025-12-30",
      "due_time": "14:00",
      "priority": "high"
    }
  }
}
```

### No Client-Side OCR

**WRONG** (violates constitution):
```typescript
// ❌ NEVER DO THIS - business logic in frontend
const text = await performOCR(image);
const task = parseTaskFromText(text);
createTask(task);
```

**CORRECT**:
```typescript
// ✅ Emit raw image to backend
const base64 = await imageToBase64(imageFile);

const response = await fetch(`/api/${userId}/chat`, {
  method: 'POST',
  body: JSON.stringify({
    message: "",
    modality: 'image',
    metadata: {
      image_data: base64
    }
  })
});
```

## API Integration

### Request Format (Image Submission)

```typescript
interface ImageChatRequest {
  conversation_id: number | null;
  message: string; // Empty for image submission
  modality: 'image';
  metadata: {
    image_data: string; // Base64 encoded image (data URL format)
    client_type?: 'web' | 'mobile';
  };
}
```

### Response Format (Extracted Data)

```typescript
interface ImageChatResponse {
  conversation_id: number;
  response: string; // "I found a task in your image"
  tool_calls: ToolCall[];
  tasks_affected: number[];
  metadata: {
    extracted_task?: {
      title: string;
      description?: string;
      due_date?: string;
      due_time?: string;
      priority?: string;
      confidence: number; // 0.0-1.0
    };
    agents_invoked: string[]; // ["InterfaceOrchestrator", "VisualContext", ...]
    execution_time_ms: number;
  };
}
```

### Error Format

```typescript
interface ImageErrorResponse {
  error: {
    code: 'NO_TEXT_FOUND' | 'LOW_CONFIDENCE' | 'INVALID_IMAGE' | 'AGENT_ERROR';
    message: string;
    details?: {
      confidence?: number;
      extracted_text?: string;
    };
    timestamp: string;
  };
}
```

## Image Capture

### Option 1: Camera (Mobile)

**Implementation**:
```typescript
function captureFromCamera() {
  const input = document.createElement('input');
  input.type = 'file';
  input.accept = 'image/*';
  input.capture = 'environment'; // Use back camera

  input.onchange = async (e) => {
    const file = (e.target as HTMLInputElement).files?.[0];
    if (file) {
      const base64 = await fileToBase64(file);
      setImageData(base64);
    }
  };

  input.click();
}
```

### Option 2: File Upload (Desktop/Mobile)

**Implementation**:
```typescript
function uploadFromGallery() {
  const input = document.createElement('input');
  input.type = 'file';
  input.accept = 'image/png, image/jpeg, image/jpg';

  input.onchange = async (e) => {
    const file = (e.target as HTMLInputElement).files?.[0];
    if (file) {
      // Validate file size (max 5MB)
      if (file.size > 5 * 1024 * 1024) {
        setError('Image too large. Max size: 5MB');
        return;
      }

      const base64 = await fileToBase64(file);
      setImageData(base64);
    }
  };

  input.click();
}
```

### Image Preprocessing

**Client-side optimization** (optional):
```typescript
async function optimizeImage(file: File): Promise<string> {
  // Resize to max 1920x1920
  // Compress to JPEG quality 85%
  // Convert to base64
  const canvas = document.createElement('canvas');
  const ctx = canvas.getContext('2d');
  const img = await loadImage(file);

  const maxSize = 1920;
  let width = img.width;
  let height = img.height;

  if (width > maxSize || height > maxSize) {
    if (width > height) {
      height = (height / width) * maxSize;
      width = maxSize;
    } else {
      width = (width / height) * maxSize;
      height = maxSize;
    }
  }

  canvas.width = width;
  canvas.height = height;
  ctx.drawImage(img, 0, 0, width, height);

  return canvas.toDataURL('image/jpeg', 0.85);
}
```

## UI Components

### 1. ImagePage

**Props**: None (gets userId from auth context)

**Responsibilities**:
- Manage image capture/upload
- Submit image to API
- Display extracted data
- Handle confirmation

**Example**:
```typescript
function ImagePage() {
  const { userId, token } = useAuth();
  const [imageData, setImageData] = useState<string | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [extractedData, setExtractedData] = useState<ExtractedTask | null>(null);
  const [conversationId, setConversationId] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleImageCapture = async (base64: string) => {
    setImageData(base64);
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
          message: "",
          modality: 'image',
          metadata: {
            image_data: base64
          }
        })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error.message);
      }

      const data = await response.json();
      setConversationId(data.conversation_id);
      setExtractedData(data.metadata.extracted_task);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleConfirm = async (taskData: ExtractedTask) => {
    // Emit confirmation to create task
    // (implementation similar to handleImageCapture)
  };

  return (
    <div className="image-page">
      <CaptureArea
        onCapture={handleImageCapture}
        imageData={imageData}
      />
      {isProcessing && <ProcessingIndicator />}
      {extractedData && (
        <ExtractedDataDisplay
          data={extractedData}
          onConfirm={handleConfirm}
          onRetry={() => setImageData(null)}
          onCancel={() => setImageData(null)}
        />
      )}
      {error && <ErrorBanner message={error} />}
    </div>
  );
}
```

### 2. CaptureArea

**Props**:
- `onCapture`: (base64: string) => void
- `imageData`: string | null

**Responsibilities**:
- Display capture/upload buttons
- Show image preview
- Emit captured image

**Example**:
```typescript
function CaptureArea({ onCapture, imageData }: CaptureAreaProps) {
  return (
    <div className="capture-area">
      {!imageData ? (
        <>
          <button onClick={captureFromCamera}>
            📷 Take Photo
          </button>
          <button onClick={uploadFromGallery}>
            🖼️ Upload Image
          </button>
        </>
      ) : (
        <>
          <img src={imageData} alt="Captured task" />
          <button onClick={() => onCapture(imageData)}>
            Process Image
          </button>
          <button onClick={() => setImageData(null)}>
            Retake
          </button>
        </>
      )}
    </div>
  );
}
```

### 3. ExtractedDataDisplay

**Props**:
- `data`: ExtractedTask
- `onConfirm`: (data: ExtractedTask) => void
- `onRetry`: () => void
- `onCancel`: () => void

**Responsibilities**:
- Display extracted task fields
- Allow inline editing
- Confirm or reject

**Example**:
```typescript
function ExtractedDataDisplay({ data, onConfirm, onRetry, onCancel }: ExtractedDataDisplayProps) {
  const [editedData, setEditedData] = useState(data);

  return (
    <div className="extracted-data">
      <h3>Found Task (Confidence: {(data.confidence * 100).toFixed(0)}%)</h3>

      <label>
        Title:
        <input
          value={editedData.title}
          onChange={(e) => setEditedData({ ...editedData, title: e.target.value })}
        />
      </label>

      <label>
        Due Date:
        <input
          type="date"
          value={editedData.due_date || ''}
          onChange={(e) => setEditedData({ ...editedData, due_date: e.target.value })}
        />
      </label>

      <label>
        Due Time:
        <input
          type="time"
          value={editedData.due_time || ''}
          onChange={(e) => setEditedData({ ...editedData, due_time: e.target.value })}
        />
      </label>

      <label>
        Priority:
        <select
          value={editedData.priority || 'medium'}
          onChange={(e) => setEditedData({ ...editedData, priority: e.target.value })}
        >
          <option value="low">Low</option>
          <option value="medium">Medium</option>
          <option value="high">High</option>
        </select>
      </label>

      <div className="actions">
        <button onClick={() => onConfirm(editedData)} className="primary">
          ✓ Create Task
        </button>
        <button onClick={onRetry}>
          ↻ Try Another Image
        </button>
        <button onClick={onCancel}>
          ✗ Cancel
        </button>
      </div>
    </div>
  );
}
```

## Styling Requirements

### Layout

- Mobile-first design (primary use case)
- Capture buttons: Full-width, large tap targets (min 60px height)
- Image preview: Full viewport width, maintain aspect ratio
- Extracted data form: Card layout with clear labels

### Responsive

- Mobile: Full-screen, portrait
- Tablet: Centered, max-width 800px
- Desktop: Centered, max-width 1000px

### Accessibility

- ARIA labels on all buttons
- High contrast for text fields
- Clear focus indicators
- Error messages with ARIA live regions

## Error Handling

### No Text Found

**Error**: Visual Context Agent finds no extractable text

**UI Response**:
1. Display message: "No task found in image. Please try a clearer photo."
2. Show extracted text (if any) for debugging
3. Offer "Try Again" button

### Low Confidence Extraction

**Scenario**: Confidence < 0.5

**UI Response**:
1. Display warning: "Low confidence extraction. Please review carefully."
2. Show extracted data with editable fields
3. Highlight low-confidence fields in yellow
4. User must confirm or correct before proceeding

### Invalid Image Format

**Error**: Unsupported file type

**UI Response**:
1. Display message: "Unsupported image format. Please use JPG or PNG."
2. Clear image data
3. Return to capture state

### File Too Large

**Error**: Image > 5MB

**UI Response**:
1. Display message: "Image too large. Max size: 5MB"
2. Suggest: "Try taking a new photo or compressing the image."
3. Clear image data

### Network Error

**Error**: API request fails

**UI Response**:
1. Display message: "Unable to process image. Check your connection."
2. Preserve image data
3. Offer "Retry" button

## Performance Considerations

### Image Size Limits

- **Max File Size**: 5MB
- **Max Dimensions**: 1920x1920 (resize if larger)
- **Compression**: JPEG quality 85%

### Processing Latency

- **Image Upload**: <1s
- **OCR Processing**: 2-5s (backend)
- **Task Extraction**: 1-2s (backend)
- **Total End-to-End**: <8s (p95)

### Offline Behavior

- Capture image offline
- Queue for processing when connection restored
- Show "Queued for processing" indicator

## Security Measures

1. **JWT Validation**: Include Bearer token in Authorization header
2. **Image Privacy**: Image discarded after processing (not stored)
3. **File Type Validation**: Only PNG/JPG allowed
4. **File Size Validation**: Max 5MB enforced
5. **Rate Limiting**: Max 10 image uploads/minute per user
6. **No PII Logging**: Do not log image data or extracted text

## Testing Requirements

### Unit Tests

1. Camera capture → Base64 generated
2. File upload → Base64 generated
3. File too large → Error displayed
4. Invalid format → Error displayed
5. Extracted data displayed correctly

### Integration Tests

1. Upload image → API called with base64
2. Receive extracted data → Form populated
3. Confirm task → Task created
4. Low confidence → Warning displayed
5. Error response → Error message displayed

### E2E Tests

1. User captures sticky note → Task created with correct details
2. User uploads calendar screenshot → Task created with due date
3. No text found → Error message, retry works
4. Network failure → Error message, retry works
5. User edits extracted data → Edited data used for task creation

### Image Test Cases

1. **Sticky note** (handwritten text)
2. **Whiteboard photo** (printed text)
3. **Calendar screenshot** (digital text)
4. **Business card** (mixed layout)
5. **Low quality photo** (blurry, poor lighting)
6. **Non-task image** (random photo, no text)

## Acceptance Criteria

1. ✅ Zero business logic in frontend (all OCR in backend)
2. ✅ Emits raw image (base64) to /api/{user_id}/chat
3. ✅ Displays extracted task data for user review
4. ✅ Allows inline editing before confirmation
5. ✅ Handles all error types gracefully
6. ✅ Image discarded after processing (privacy)
7. ✅ Mobile-optimized (primary use case)
8. ✅ File size and format validation enforced

---

## Example Image Processing Flow

**User Action**: Upload photo of sticky note with text:
```
Quarterly Review Meeting
Dec 30, 2025 at 2:00 PM
URGENT
```

**UI Action**:
```json
POST /api/user_123/chat
{
  "conversation_id": null,
  "message": "",
  "modality": "image",
  "metadata": {
    "image_data": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA..."
  }
}
```

**Backend Processing**:
1. Visual Context Agent extracts text via OCR
2. Parses: title="Quarterly Review Meeting", due_date="2025-12-30", due_time="14:00", priority="high"
3. Confidence: 0.82

**Backend Response**:
```json
{
  "conversation_id": 125,
  "response": "I found a task in your image",
  "tool_calls": [],
  "tasks_affected": [],
  "metadata": {
    "extracted_task": {
      "title": "Quarterly Review Meeting",
      "due_date": "2025-12-30",
      "due_time": "14:00",
      "priority": "high",
      "confidence": 0.82
    },
    "agents_invoked": ["InterfaceOrchestrator", "VisualContext", "TaskReasoning"]
  }
}
```

**UI Display**:
- Form pre-populated with extracted data
- Confidence badge: "82%"
- User reviews, optionally edits
- User clicks "✓ Create Task"

**Task Created**:
- Task #42 created
- Confirmation message: "Quarterly Review Meeting added for Dec 30 at 2:00 PM"
- Image discarded (privacy)
