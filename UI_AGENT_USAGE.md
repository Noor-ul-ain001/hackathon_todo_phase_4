# UI Agent - Complete Usage Guide

This guide shows you how to use the UI Agent to analyze UI mockups and generate complete frontend code.

---

## What is the UI Agent?

The UI Agent is a specialized AI agent that:
- Analyzes UI mockup images using vision capabilities
- Extracts design elements (colors, layouts, typography, components)
- Generates production-ready ChatKit-based frontend code
- Creates responsive, accessible, and performant UIs

---

## How to Use the UI Agent with Claude Code

### Method 1: With an Image Mockup

#### Step 1: Prepare Your Mockup

Save your UI mockup in one of these formats:
- PNG, JPG, or PDF
- Screenshot from design tool (Figma, Sketch, Adobe XD)
- Hand-drawn sketch (photographed)
- Reference UI from existing website

#### Step 2: Start Claude Code

```bash
cd your-project-directory
claude-code
```

#### Step 3: Provide the Mockup to UI Agent

```
Please act as the UI Agent.

I'm attaching a mockup of my desired chat interface [attach: ui-mockup.png].

Analyze this image and generate a complete ChatKit-based frontend:

1. Use vision capabilities to identify:
   - Color scheme and palette
   - Layout structure (header, message area, input)
   - Component styles (chat bubbles, buttons, inputs)
   - Typography (fonts, sizes, weights)
   - Spacing and padding
   - Any animations or special effects

2. Generate:
   - Next.js project with ChatKit
   - Custom theme matching the mockup
   - CSS for all visual elements
   - React components for custom features
   - API integration code
   - Responsive design (mobile/tablet/desktop)

3. Backend API URL: http://localhost:8000

Create frontend/ directory with the complete implementation.
```

#### Step 4: Review Generated Code

The UI Agent will create:
```
frontend/
├── package.json
├── pages/
│   ├── _app.tsx
│   ├── _document.tsx
│   └── index.tsx
├── components/
│   ├── CustomHeader.tsx
│   ├── MessageBubble.tsx
│   ├── InputArea.tsx
│   └── ... (other custom components)
├── styles/
│   ├── variables.css
│   ├── theme.css
│   ├── components.css
│   └── responsive.css
├── lib/
│   ├── api.ts
│   └── types.ts
├── .env.local.example
└── README.md
```

---

### Method 2: With a Text Description (No Image)

If you don't have an image, you can describe your desired UI:

```
Please act as the UI Agent.

Create a ChatKit-based frontend with this design:

Visual Design:
- Light theme with clean, modern aesthetic
- Primary color: Deep blue (#1E40AF)
- Secondary color: Cyan (#06B6D4)
- Background: Light gray (#F9FAFB)
- User messages: Right-aligned, blue background (#3B82F6)
- Assistant messages: Left-aligned, white background with border

Layout:
- Fixed header (70px height) with gradient background
- Main chat area with auto-scroll
- Fixed input area at bottom (80px height)
- Max content width: 1200px, centered

Components:
- Header: Logo on left, user info on right
- Chat bubbles: Rounded corners (12px), subtle shadow
- Input: Rounded border (8px), send button with icon
- Avatars: Circular (40px) next to each message

Typography:
- Font family: Inter
- Message text: 14px
- Header text: 18px, bold
- Input text: 14px

Interactions:
- Smooth scroll behavior
- Fade-in animation for new messages (300ms)
- Hover effects on buttons
- Loading indicator for API calls

Responsive:
- Mobile: Single column, full width
- Tablet: 90% width
- Desktop: Max 1200px width

Backend API: http://localhost:8000

Generate the complete frontend implementation.
```

---

### Method 3: Reference an Existing UI

```
Please act as the UI Agent.

Create a ChatKit frontend inspired by Slack's chat interface:
- Similar layout structure
- Clean, professional design
- Sidebar for conversations (optional for this project)
- Modern message styling
- Professional color scheme

Adapt the design for a single-conversation todo chatbot.
Backend API: http://localhost:8000
```

---

## What the UI Agent Generates

### 1. ChatKit Configuration

```typescript
// frontend/lib/chatkit-config.ts
export const chatConfig = {
  theme: {
    colors: {
      primary: '#3B82F6',      // Extracted from mockup
      secondary: '#8B5CF6',    // Extracted from mockup
      background: '#F9FAFB',   // Extracted from mockup
      userMessage: '#3B82F6',
      assistantMessage: '#FFFFFF'
    },
    fonts: {
      base: 'Inter, system-ui, sans-serif',
      sizes: {
        message: '14px',
        header: '18px',
        input: '14px'
      }
    },
    borderRadius: {
      message: '12px',
      input: '8px'
    }
  }
};
```

### 2. Custom React Components

```tsx
// frontend/components/CustomHeader.tsx
export default function CustomHeader() {
  return (
    <header className="chat-header">
      <div className="header-logo">
        <h1>Todo Assistant</h1>
      </div>
      <div className="header-user">
        <span>Welcome, User</span>
        <Avatar src="/user.png" />
      </div>
    </header>
  );
}
```

### 3. Styled Components

```css
/* frontend/styles/components.css */
.message-bubble {
  max-width: 70%;
  padding: 12px 16px;
  border-radius: 12px;
  margin-bottom: 8px;
  animation: fadeIn 0.3s ease-out;
}

.message-user {
  background-color: #3B82F6;
  color: white;
  margin-left: auto;
  text-align: right;
}

.message-assistant {
  background-color: white;
  color: #111827;
  margin-right: auto;
  border: 1px solid #E5E7EB;
}
```

### 4. API Integration

```typescript
// frontend/lib/api.ts
export async function sendMessage(
  userId: string,
  message: string,
  conversationId?: number
) {
  const response = await fetch(
    `${process.env.NEXT_PUBLIC_API_URL}/api/${userId}/chat`,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message,
        conversation_id: conversationId
      })
    }
  );

  if (!response.ok) {
    throw new Error('Failed to send message');
  }

  return response.json();
}
```

### 5. Responsive Design

```css
/* frontend/styles/responsive.css */
/* Mobile */
@media (max-width: 767px) {
  .chat-container {
    width: 100%;
    padding: 0;
  }

  .message-bubble {
    max-width: 85%;
    font-size: 13px;
  }
}

/* Tablet */
@media (min-width: 768px) and (max-width: 1023px) {
  .chat-container {
    width: 90%;
    max-width: 800px;
  }

  .message-bubble {
    max-width: 75%;
  }
}

/* Desktop */
@media (min-width: 1024px) {
  .chat-container {
    max-width: 1200px;
  }

  .message-bubble {
    max-width: 60%;
  }
}
```

---

## Advanced UI Agent Features

### Feature 1: Dark Mode Support

If your mockup shows both light and dark modes:

```
UI Agent will generate:
- theme-light.css
- theme-dark.css
- ThemeToggle component
- useTheme hook
- localStorage persistence
```

### Feature 2: Animations

If mockup indicates animations:

```
UI Agent will generate:
- CSS keyframe animations
- Framer Motion code (if complex)
- Smooth transitions
- Loading states
```

### Feature 3: Accessibility

Automatically included in all generated code:
- ARIA labels
- Keyboard navigation
- Focus states
- Color contrast validation (WCAG AA)
- Screen reader support

---

## Testing Generated UI

### Step 1: Install Dependencies

```bash
cd frontend
npm install
```

### Step 2: Configure Environment

```bash
# Create .env.local
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
echo "NEXT_PUBLIC_OPENAI_DOMAIN_KEY=your-key" >> .env.local
```

### Step 3: Run Development Server

```bash
npm run dev
```

### Step 4: Open in Browser

```bash
open http://localhost:3000
```

---

## Customizing Generated UI

### Change Colors

Edit `frontend/styles/variables.css`:

```css
:root {
  --color-primary: #YOUR_COLOR;
  --color-secondary: #YOUR_COLOR;
  /* ... */
}
```

### Modify Layout

Edit `frontend/pages/index.tsx` and component files.

### Add Components

Create new files in `frontend/components/` and import them.

### Update Styles

Modify CSS files in `frontend/styles/`.

---

## Common UI Agent Prompts

### Prompt 1: Minimal Design

```
Create a minimal, clean ChatKit interface with:
- White background
- Single accent color (blue)
- Simple rounded rectangles for messages
- No shadows or gradients
- Plenty of whitespace
```

### Prompt 2: Modern/Trendy

```
Create a modern ChatKit interface with:
- Gradients and shadows
- Smooth animations
- Glassmorphism effects
- Vibrant colors
- Playful design elements
```

### Prompt 3: Corporate/Professional

```
Create a professional ChatKit interface suitable for enterprise:
- Conservative color scheme
- Clear hierarchy
- Readable typography
- Minimal animations
- Accessibility-focused
```

### Prompt 4: Mobile-First

```
Create a mobile-optimized ChatKit interface:
- Large tap targets (44px minimum)
- Simplified navigation
- Bottom sheet for actions
- Swipe gestures
- Full-screen focus
```

---

## Troubleshooting

### Issue: Generated UI doesn't match mockup exactly

**Solution:**
- Provide higher resolution image
- Include design specifications in text
- Specify exact color hex codes
- Describe specific elements in detail

### Issue: ChatKit not loading

**Solution:**
```bash
# Check environment variable
echo $NEXT_PUBLIC_OPENAI_DOMAIN_KEY

# Verify domain allowlist
# Visit: https://platform.openai.com/settings/organization/security/domain-allowlist
```

### Issue: Styles not applying

**Solution:**
```bash
# Clear Next.js cache
rm -rf .next
npm run dev
```

### Issue: API integration fails

**Solution:**
```bash
# Check API URL
echo $NEXT_PUBLIC_API_URL

# Test backend
curl http://localhost:8000/health
```

---

## Best Practices

### 1. Provide Clear Mockups

- High resolution (1920x1080 or higher)
- Clear visibility of all elements
- Multiple views if possible (mobile + desktop)

### 2. Include Specifications

Even with images, add text:
- Color hex codes
- Font names
- Exact measurements
- Interaction descriptions

### 3. Describe States

Mention all UI states:
- Default state
- Hover state
- Active/selected state
- Loading state
- Error state

### 4. Specify Responsiveness

Describe behavior at different sizes:
- Mobile (< 768px)
- Tablet (768px - 1024px)
- Desktop (> 1024px)

---

## Example: Complete UI Agent Session

**User:**
```
Please act as the UI Agent.

[Attaches: modern-chat-ui.png]

This is my desired chat interface. Generate a complete ChatKit frontend that matches this design.

Additional specs:
- Primary color: #6366F1 (indigo)
- Font: Inter
- Animations: Fade-in for messages (300ms)
- Responsive: Mobile-first

Backend API: http://localhost:8000
```

**UI Agent Response:**
```
I'll analyze your mockup and generate a complete ChatKit frontend.

[Uses vision to analyze image]

Identified elements:
- Modern gradient header (#6366F1 to #8B5CF6)
- Rounded chat bubbles (16px radius)
- White assistant messages, indigo user messages
- Clean input with send button
- Inter font family
- Ample spacing between messages

Generating frontend...

✓ Created frontend/ directory
✓ Generated ChatKit configuration
✓ Built custom components:
  - GradientHeader.tsx
  - MessageBubble.tsx
  - ChatInput.tsx
✓ Created responsive CSS
✓ Added fade-in animations
✓ Configured API integration

Next steps:
1. cd frontend
2. npm install
3. Copy .env.local.example to .env.local
4. Add your OPENAI_DOMAIN_KEY
5. npm run dev
6. Open http://localhost:3000

Your frontend is ready!
```

---

## Summary

The UI Agent is a powerful tool that:

✅ Analyzes visual designs automatically
✅ Generates production-ready code
✅ Saves hours of frontend development
✅ Ensures consistency with designs
✅ Creates responsive, accessible UIs
✅ Includes best practices by default

Use it to rapidly prototype or build complete frontend applications from mockups!
