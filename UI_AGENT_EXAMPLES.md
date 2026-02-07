# UI Agent - Example Interactions

This document shows example interactions with the UI Agent for image-to-UI conversion.

---

## Example 1: Modern Chat Interface

### Input: Text Description (When No Image Available)

```
Create a modern chat interface with:
- Light blue gradient header (#3B82F6 to #6366F1)
- White message bubbles for assistant (left-aligned)
- Blue message bubbles for user (right-aligned, #3B82F6)
- Rounded corners (16px)
- Subtle shadows on bubbles
- Clean, minimal input field with rounded corners
- Send button with paper plane icon
- Inter font family
- Responsive design
```

### UI Agent Process:

1. **image_analyzer** (text mode):
   - Parse text description
   - Extract color values
   - Identify layout structure
   - Note component styles

2. **style_extractor**:
   - Generate CSS variables
   ```css
   :root {
     --color-header-start: #3B82F6;
     --color-header-end: #6366F1;
     --color-user-message: #3B82F6;
     --color-assistant-message: #FFFFFF;
     --border-radius-bubble: 16px;
     --font-family: Inter, sans-serif;
   }
   ```

3. **chatkit_generator**:
   - Create ChatKit config
   - Set up Next.js project
   - Configure theme

4. **component_builder**:
   - Create custom header with gradient
   - Build message bubble components
   - Create input area component

### Output Structure:
```
frontend/
├── pages/
│   ├── _app.tsx
│   └── index.tsx
├── components/
│   ├── GradientHeader.tsx
│   ├── MessageBubble.tsx
│   └── InputArea.tsx
├── styles/
│   ├── variables.css
│   ├── theme.css
│   └── components.css
└── lib/
    └── api.ts
```

---

## Example 2: Dark Theme Chat Interface

### Input: Image Description

```
[Imagine an attached screenshot showing:]
- Dark background (#1A1A2E)
- Cyan accent color (#00D4FF)
- Dark gray chat bubbles for assistant (#2D2D44)
- Cyan chat bubbles for user (#00D4FF)
- Minimal header with user avatar
- Floating input at bottom
- Smooth fade-in animations
- Glassmorphism effect on input
```

### UI Agent Analysis:

**Color Palette Detected:**
- Background: #1A1A2E (dark navy)
- Surface: #2D2D44 (dark gray)
- Accent: #00D4FF (cyan)
- Text: #FFFFFF (white)
- Text Secondary: #A0AEC0 (light gray)

**Layout Structure:**
```
┌─────────────────────────┐
│  Header (Dark)          │
├─────────────────────────┤
│                         │
│  [Assistant] ◄─────     │
│     ────► [User]        │
│                         │
│  [Assistant] ◄─────     │
│                         │
├─────────────────────────┤
│ [Floating Input]        │
└─────────────────────────┘
```

**Components Identified:**
1. Header with avatar (minimal design)
2. Message list with dark bubbles
3. Floating input with glassmorphism
4. Fade-in animations

### Generated Code Examples:

**Custom Theme:**
```typescript
// frontend/lib/theme.ts
export const darkTheme = {
  colors: {
    background: '#1A1A2E',
    surface: '#2D2D44',
    primary: '#00D4FF',
    text: '#FFFFFF',
    textSecondary: '#A0AEC0'
  },
  effects: {
    glassmorphism: {
      background: 'rgba(45, 45, 68, 0.7)',
      backdropFilter: 'blur(10px)',
      border: '1px solid rgba(0, 212, 255, 0.2)'
    }
  },
  animations: {
    fadeIn: {
      keyframes: {
        from: { opacity: 0, transform: 'translateY(10px)' },
        to: { opacity: 1, transform: 'translateY(0)' }
      },
      duration: '0.3s',
      easing: 'ease-out'
    }
  }
};
```

**Glassmorphism Input:**
```tsx
// frontend/components/GlassmorphicInput.tsx
import { useState } from 'react';
import styles from '../styles/Input.module.css';

export default function GlassmorphicInput({ onSend }: { onSend: (msg: string) => void }) {
  const [message, setMessage] = useState('');

  const handleSend = () => {
    if (message.trim()) {
      onSend(message);
      setMessage('');
    }
  };

  return (
    <div className={styles.glassInput}>
      <input
        type="text"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        onKeyPress={(e) => e.key === 'Enter' && handleSend()}
        placeholder="Type your message..."
        className={styles.input}
      />
      <button onClick={handleSend} className={styles.sendButton}>
        <SendIcon />
      </button>
    </div>
  );
}
```

**CSS for Glassmorphism:**
```css
/* frontend/styles/Input.module.css */
.glassInput {
  position: fixed;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  width: calc(100% - 40px);
  max-width: 600px;

  background: rgba(45, 45, 68, 0.7);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(0, 212, 255, 0.2);
  border-radius: 16px;

  padding: 12px;
  display: flex;
  gap: 12px;

  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.input {
  flex: 1;
  background: transparent;
  border: none;
  color: #FFFFFF;
  font-size: 14px;
  outline: none;
}

.input::placeholder {
  color: #A0AEC0;
}

.sendButton {
  background: #00D4FF;
  border: none;
  border-radius: 8px;
  padding: 8px 16px;
  color: #1A1A2E;
  cursor: pointer;
  transition: all 0.2s;
}

.sendButton:hover {
  background: #00BFEA;
  transform: scale(1.05);
}
```

---

## Example 3: Minimalist Corporate Chat

### Input: Figma Export Description

```
[Screenshot of Figma design showing:]
- Clean white background
- Corporate blue (#0066CC)
- Simple header with company logo
- Rectangular message bubbles (minimal border-radius: 4px)
- Professional sans-serif font (Roboto)
- Subtle dividers between messages
- Timestamp on each message
- Read receipt indicators
```

### UI Agent Analysis:

**Design System Extracted:**
- **Brand Colors:**
  - Primary: #0066CC (corporate blue)
  - Background: #FFFFFF (white)
  - Text: #333333 (dark gray)
  - Borders: #E0E0E0 (light gray)

- **Typography:**
  - Font: Roboto
  - Sizes: 14px (body), 12px (timestamps), 16px (header)

- **Spacing System:**
  - Base unit: 8px
  - Message padding: 16px
  - Message gap: 8px

- **Components:**
  - Header with logo
  - Rectangular bubbles (minimal radius)
  - Timestamps
  - Read receipts
  - Dividers

### Generated Components:

**Message with Timestamp:**
```tsx
// frontend/components/CorporateMessage.tsx
import { formatTimestamp } from '../lib/utils';

interface MessageProps {
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  read?: boolean;
}

export default function CorporateMessage({ role, content, timestamp, read }: MessageProps) {
  return (
    <div className={`message message-${role}`}>
      <div className="message-content">
        {content}
      </div>
      <div className="message-meta">
        <span className="timestamp">{formatTimestamp(timestamp)}</span>
        {role === 'user' && read && <span className="read-receipt">✓✓</span>}
      </div>
    </div>
  );
}
```

**Corporate Styles:**
```css
/* frontend/styles/Corporate.module.css */
.message {
  max-width: 70%;
  padding: 16px;
  margin-bottom: 8px;
  border-radius: 4px;
  font-family: Roboto, sans-serif;
  font-size: 14px;
  line-height: 1.5;
}

.message-user {
  margin-left: auto;
  background-color: #0066CC;
  color: #FFFFFF;
  text-align: right;
}

.message-assistant {
  margin-right: auto;
  background-color: #F5F5F5;
  color: #333333;
  border: 1px solid #E0E0E0;
}

.message-meta {
  margin-top: 8px;
  font-size: 12px;
  color: #999999;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.read-receipt {
  color: #0066CC;
}
```

---

## Example 4: Mobile-First Chat

### Input: Mobile Screenshot

```
[Mobile UI screenshot showing:]
- Full-screen chat interface
- Sticky header with back button
- Large tap targets (44px minimum)
- Bottom navigation
- Swipe gestures for actions
- Pull-to-refresh at top
```

### UI Agent Mobile Optimization:

**Responsive Breakpoints:**
```css
/* Mobile first approach */
:root {
  --header-height: 60px;
  --input-height: 80px;
  --message-max-width: 85%;
}

/* Tablet */
@media (min-width: 768px) {
  :root {
    --header-height: 70px;
    --message-max-width: 70%;
  }
}

/* Desktop */
@media (min-width: 1024px) {
  :root {
    --header-height: 80px;
    --message-max-width: 60%;
  }
}
```

**Touch-Optimized Components:**
```tsx
// frontend/components/TouchOptimizedInput.tsx
export default function TouchOptimizedInput() {
  return (
    <div className="mobile-input">
      {/* Minimum 44px tap target */}
      <button className="attach-button" style={{ minHeight: '44px', minWidth: '44px' }}>
        📎
      </button>
      <input type="text" className="message-input" />
      <button className="send-button" style={{ minHeight: '44px', minWidth: '44px' }}>
        ✉️
      </button>
    </div>
  );
}
```

---

## Testing UI Agent Output

### Validation Checklist:

1. **Visual Accuracy**
   - Colors match mockup (within 5% tolerance)
   - Layout structure matches design
   - Component styles are accurate
   - Spacing follows design system

2. **Responsiveness**
   - Mobile (320px - 767px): Single column, full width
   - Tablet (768px - 1023px): Moderate padding
   - Desktop (1024px+): Max width constraint

3. **Accessibility**
   - Color contrast ratio ≥ 4.5:1
   - Keyboard navigation works
   - Screen reader compatible
   - ARIA labels present

4. **Performance**
   - First Contentful Paint < 1.5s
   - Time to Interactive < 3s
   - Smooth animations (60fps)
   - Optimized images

---

## Advanced UI Agent Features

### Feature 1: Animation Extraction

If mockup shows animations:
```
Input: [Video or animated GIF showing fade-in effect on messages]

UI Agent generates:
```css
@keyframes messageFadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.message {
  animation: messageFadeIn 0.3s ease-out;
}
```

### Feature 2: Multi-Theme Support

If mockup shows light and dark modes:
```
UI Agent generates:
- theme-light.css
- theme-dark.css
- ThemeToggle component
- useTheme hook
- localStorage persistence
```

### Feature 3: Component Library

For complex UIs, UI Agent creates:
```
components/
├── atoms/
│   ├── Button.tsx
│   ├── Input.tsx
│   └── Avatar.tsx
├── molecules/
│   ├── MessageBubble.tsx
│   └── InputArea.tsx
└── organisms/
    ├── ChatWindow.tsx
    └── Header.tsx
```

---

## Tips for Best Results

1. **Provide High-Quality Images**
   - Resolution: At least 1920x1080
   - Clear, uncompressed formats (PNG preferred)
   - Multiple views if available (mobile + desktop)

2. **Include Design Specs**
   - Color hex codes if known
   - Font names
   - Specific measurements
   - Animation descriptions

3. **Describe Interactions**
   - Hover states
   - Active states
   - Loading states
   - Error states

4. **Specify Responsiveness**
   - Breakpoints
   - Mobile behavior
   - Tablet adjustments

---

## Common UI Agent Outputs

Every UI Agent run produces:

1. **Complete Next.js Project**
   - Configured and ready to run
   - All dependencies in package.json

2. **Custom Theme Files**
   - CSS variables
   - Theme configuration
   - Component styles

3. **React Components**
   - TypeScript types
   - Props interfaces
   - Event handlers

4. **API Integration**
   - Backend connection
   - Error handling
   - Loading states

5. **Documentation**
   - Component usage
   - Customization guide
   - Deployment instructions

---

## Conclusion

The UI Agent transforms visual designs into production-ready code, whether from:
- Image mockups
- Figma exports
- Text descriptions
- Reference screenshots

It ensures:
- Pixel-perfect accuracy
- Production-quality code
- Full responsiveness
- Accessibility compliance
- Performance optimization
