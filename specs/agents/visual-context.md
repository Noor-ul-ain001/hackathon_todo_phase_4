# Agent Specification: Visual Context

**Agent Name**: Visual Context Agent
**Version**: 1.0.0
**Created**: 2025-12-27
**Status**: Active Specification (Phase 5)

## Purpose

The Visual Context Agent extracts task-relevant information from images submitted by users. It identifies text, dates, priorities, and other structured data from screenshots, photos of notes, whiteboards, or documents, enabling task creation from visual inputs.

## Responsibilities

### Primary Responsibilities

1. **Text Extraction**: Perform OCR (Optical Character Recognition) on images
2. **Date Recognition**: Identify dates and times in extracted text
3. **Priority Detection**: Recognize visual cues indicating urgency or priority
4. **Content Structuring**: Organize extracted data into task-relevant fields
5. **Confidence Scoring**: Rate extraction quality and reliability

### Secondary Responsibilities

1. **Image Quality Assessment**: Determine if image is suitable for processing
2. **Orientation Detection**: Identify if image needs rotation
3. **Handwriting Recognition**: Extract text from handwritten notes
4. **Multi-Language Support**: Handle text in various languages
5. **Visual Metadata**: Capture image properties (timestamp, location if embedded)

## Allowed Actions

### Image Processing
- Perform OCR on uploaded images
- Detect text regions within images
- Extract and recognize handwritten text
- Identify visual markers (checkboxes, bullet points, highlights)
- Assess image quality (blur, contrast, resolution)

### Content Analysis
- Parse extracted text for task-relevant information
- Identify dates, times, deadlines in text
- Recognize priority keywords (urgent, ASAP, important)
- Detect structure (lists, tables, headings)
- Extract contact info, locations, names (for task context)

### Data Structuring
- Map extracted text to task fields (title, description, due_date)
- Assign confidence scores to each extracted field
- Identify multiple potential tasks in one image
- Handle ambiguous or incomplete extractions

## Skills Used

**None directly**. The Visual Context Agent uses computer vision and OCR libraries/APIs, not business logic skills.

However, results are passed to `ui_intent_normalization` skill (via Interface Orchestrator) to convert extracted data into structured task intent.

## Disallowed Behavior

### Absolutely Prohibited

1. **Task Creation**: NO direct task operations (delegate to Task Reasoning Agent)
2. **Validation**: NO input validation (delegate to Validation Agent)
3. **MCP Tool Calls**: NO database access
4. **Response Formatting**: NO user-facing messages
5. **Image Storage**: NO long-term image retention (privacy/security)

### Specific Restrictions

- **NO image storage**: Process and discard immediately after extraction
- **NO facial recognition**: Don't identify people in images
- **NO sensitive data extraction**: Skip credit cards, SSNs, passwords
- **NO assumption of correctness**: Always provide confidence scores
- **NO state storage**: Process each image independently

## Input Specification

### Expected Input Format

```json
{
  "image_data": "base64_encoded_string",
  "image_metadata": {
    "format": "png|jpg|jpeg|webp",
    "size_bytes": 245678,
    "timestamp": "2025-12-27T10:30:00Z (from file metadata if available)"
  },
  "user_id": "string (required)",
  "context": {
    "source": "mobile_camera|screenshot|file_upload",
    "original_filename": "string (optional)"
  }
}
```

### Example Input

```json
{
  "image_data": "iVBORw0KGgoAAAANSUhEUgAAA...(base64)",
  "image_metadata": {
    "format": "png",
    "size_bytes": 187654,
    "timestamp": "2025-12-27T10:30:00Z"
  },
  "user_id": "user_123",
  "context": {
    "source": "mobile_camera",
    "original_filename": "meeting_notes.png"
  }
}
```

## Output Specification

### Expected Output Format

```json
{
  "success": "boolean",
  "extracted_data": {
    "full_text": "string (all extracted text)",
    "structured_fields": {
      "potential_title": "string (most prominent text)",
      "potential_description": "string (body text)",
      "detected_dates": [
        {
          "text": "string",
          "parsed_date": "ISO 8601",
          "confidence": 0.0-1.0
        }
      ],
      "detected_priorities": [
        {
          "keyword": "urgent|important|asap|etc.",
          "priority": "high|medium|low",
          "confidence": 0.0-1.0
        }
      ]
    },
    "visual_markers": {
      "checkboxes": ["checked", "unchecked"],
      "bullet_points": 3,
      "highlighted_text": ["important deadline", "urgent"]
    }
  },
  "quality_assessment": {
    "overall_quality": "good|fair|poor",
    "text_clarity": 0.0-1.0,
    "orientation_correct": "boolean",
    "issues": ["blur", "low_contrast", "partial_text"]
  },
  "errors": [
    {
      "code": "string",
      "message": "string"
    }
  ]
}
```

### Example Outputs

#### Successful Extraction (High Quality)
```json
{
  "success": true,
  "extracted_data": {
    "full_text": "Quarterly Review Meeting\n\nScheduled: Dec 30, 2025 at 2:00 PM\nLocation: Conference Room A\n\nAgenda:\n- Review Q4 results\n- Plan Q1 objectives\n- Budget allocation\n\nURGENT: Prepare presentation by Dec 28",
    "structured_fields": {
      "potential_title": "Quarterly Review Meeting",
      "potential_description": "Review Q4 results, Plan Q1 objectives, Budget allocation",
      "detected_dates": [
        {
          "text": "Dec 30, 2025 at 2:00 PM",
          "parsed_date": "2025-12-30T14:00:00Z",
          "confidence": 0.95
        },
        {
          "text": "Dec 28",
          "parsed_date": "2025-12-28",
          "confidence": 0.90
        }
      ],
      "detected_priorities": [
        {
          "keyword": "URGENT",
          "priority": "high",
          "confidence": 0.98
        }
      ]
    },
    "visual_markers": {
      "checkboxes": [],
      "bullet_points": 3,
      "highlighted_text": ["URGENT"]
    }
  },
  "quality_assessment": {
    "overall_quality": "good",
    "text_clarity": 0.92,
    "orientation_correct": true,
    "issues": []
  },
  "errors": []
}
```

#### Poor Quality Image
```json
{
  "success": false,
  "extracted_data": {
    "full_text": "Me...ng n...tes\nUn...ble to r...d",
    "structured_fields": {
      "potential_title": null,
      "potential_description": null,
      "detected_dates": [],
      "detected_priorities": []
    },
    "visual_markers": {}
  },
  "quality_assessment": {
    "overall_quality": "poor",
    "text_clarity": 0.25,
    "orientation_correct": true,
    "issues": ["severe_blur", "low_contrast", "text_too_small"]
  },
  "errors": [
    {
      "code": "LOW_QUALITY_IMAGE",
      "message": "Image quality too low for reliable text extraction. Please capture a clearer image."
    }
  ]
}
```

## Execution Flow

```
1. Receive image data + metadata
   ↓
2. Validate image format and size
   - Check supported formats (png, jpg, webp)
   - Check size < 10MB
   - Reject if invalid
   ↓
3. Assess image quality
   - Check resolution (min 640x480)
   - Detect blur, low contrast
   - Check orientation
   - If quality too low: return error
   ↓
4. Perform OCR
   - Extract all text from image
   - Identify text regions
   - Recognize handwriting if present
   - Generate confidence scores per region
   ↓
5. Analyze extracted text
   - Identify title (largest/topmost text)
   - Extract description (body paragraphs)
   - Parse dates and times
   - Detect priority keywords
   - Identify visual markers (bullets, checkboxes)
   ↓
6. Structure extracted data
   - Map to task fields
   - Assign confidence scores
   - Flag ambiguities
   ↓
7. Return extraction results
   - Structured fields
   - Quality assessment
   - Errors/warnings
   ↓
8. Discard image data (privacy)
```

## Text Extraction Logic

### Title Detection

```
1. Identify largest text region
2. If at top of image: likely title
3. If bold/highlighted: likely title
4. If followed by bullet points: likely title
5. Confidence based on position + formatting
```

### Date Parsing

| Extracted Text | Parsed Date | Confidence |
|----------------|-------------|------------|
| "Dec 30, 2025" | 2025-12-30 | 0.95 |
| "12/30/2025" | 2025-12-30 | 0.90 |
| "tomorrow" | (relative calculation) | 0.70 |
| "next week" | (relative calculation) | 0.60 |
| "30th" | (ambiguous month) | 0.40 |

### Priority Detection

| Visual Cue | Detected Priority | Confidence |
|------------|-------------------|------------|
| "URGENT" in caps | high | 0.98 |
| Red highlighting | high | 0.85 |
| "ASAP" or "!!!" | high | 0.90 |
| "Important" | high | 0.75 |
| "Low priority" | low | 0.95 |
| No markers | medium (default) | 0.50 |

## Error Handling

### Error Categories

1. **Image Quality Errors**: Too blurry, low resolution, poor contrast
2. **Format Errors**: Unsupported image format
3. **Size Errors**: Image too large (>10MB)
4. **OCR Failures**: No text detected, language not supported
5. **Processing Errors**: OCR service unavailable

### Error Response Strategy

```
If image quality too low:
  → Return error with guidance
  → Message: "Please capture a clearer image with better lighting"

If no text detected:
  → Return error
  → Message: "No text found in image. Please ensure image contains readable text."

If OCR service fails:
  → Return error
  → Message: "Unable to process image at this time. Please try again."

If format unsupported:
  → Return error
  → Message: "Supported formats: PNG, JPG, WebP"
```

## Quality Assessment Criteria

### Good Quality (confidence 0.8-1.0)
- Resolution ≥ 1024x768
- Text clarity high (sharp, well-lit)
- Correct orientation
- High contrast
- No blur

### Fair Quality (confidence 0.5-0.79)
- Resolution 640x480 - 1024x768
- Some blur or low contrast
- Handwriting partially unclear
- Minor orientation issues
- Still usable

### Poor Quality (confidence < 0.5)
- Resolution < 640x480
- Severe blur
- Very low contrast
- Text too small to read
- Wrong orientation
- Not usable

## State Management

### Stateless Processing

```python
# Conceptual example
class VisualContextAgent:
    def extract_from_image(self, image_data):
        # 1. Validate image
        if not self.is_valid_image(image_data):
            return {"success": False, "errors": [{"code": "INVALID_IMAGE"}]}

        # 2. Perform OCR
        ocr_result = self.ocr_service.extract_text(image_data)

        # 3. Analyze text
        structured = self.analyze_extracted_text(ocr_result.text)

        # 4. Assess quality
        quality = self.assess_quality(ocr_result)

        # 5. Return results
        return {
            "success": True,
            "extracted_data": structured,
            "quality_assessment": quality
        }

        # Image data NOT stored
        # Next request starts fresh
```

### Prohibited State

- **NO image storage**: Immediately discard after processing
- **NO user preferences**: Don't remember preferred extraction settings
- **NO learning**: No ML model updates based on user corrections (for now)
- **NO caching**: Every image processed independently

## Privacy and Security

### Privacy Protections

1. **Immediate Discard**: Image data deleted after extraction completes
2. **No Logging of Images**: Only log metadata (size, format), not actual images
3. **Sensitive Data Detection**: Skip extraction of credit card numbers, SSNs
4. **No Facial Recognition**: Don't identify or tag people in images
5. **User Isolation**: Only user who submitted image can see results

### Security Measures

1. **Size Limits**: Reject images > 10MB (DoS prevention)
2. **Format Validation**: Only allow known safe formats
3. **Malware Scanning**: Check for embedded exploits (if using external OCR)
4. **Rate Limiting**: Limit image uploads per user per hour

## Testing Requirements

### Unit Tests

1. Text extraction from clean screenshots
2. Handwriting recognition from notes
3. Date parsing from various formats
4. Priority detection from keywords and visual cues
5. Quality assessment (blur, contrast, resolution)
6. Error handling for unsupported formats

### Integration Tests

1. End-to-end image → task creation flow
2. Multi-language text extraction
3. Image with multiple potential tasks
4. Poor quality image rejection

### Edge Cases

1. Blank image → error: "No text found"
2. Image with only numbers → extract as description
3. Upside-down image → detect and rotate
4. Image with multiple languages → extract all, note languages
5. Screenshot with UI elements → extract relevant text only

## Failure Modes

| Failure Scenario | Detection | Response | User Impact |
|------------------|-----------|----------|-------------|
| Image too large | Size check | Return error: "Max 10MB" | Request rejected, user must resize |
| No text detected | OCR returns empty | Return error with guidance | Request rejected, user retries with better image |
| Very low quality | Quality score < 0.3 | Return error with tips | Request rejected, user captures new image |
| Unsupported format | Format validation | Return error with supported formats | Request rejected |
| OCR service down | API error | Return error: "Service unavailable" | Request fails, retry later |

## Dependencies

### Required Components

- **OCR Service/Library**: Tesseract, Google Vision API, AWS Textract, or similar
- **Image Processing Library**: PIL/Pillow, OpenCV, or similar
- **Date Parser**: For converting text dates to ISO 8601

### Optional Components

- **Handwriting Recognition**: For cursive/handwritten notes
- **Object Detection**: For identifying visual markers (checkboxes, highlights)
- **Language Detection**: For multi-language support

## Versioning and Evolution

### Phase 5 (Initial)
- Basic OCR for printed text
- Simple date and priority detection
- Quality assessment
- English language only

### Future Enhancements
- Handwriting recognition
- Multi-language support
- Table/structure extraction
- Visual element detection (diagrams, charts)
- ML-based task suggestion from context

## Acceptance Criteria

A Visual Context Agent implementation is considered compliant if:

1. ✅ Extracts text from clear images with >85% accuracy
2. ✅ Detects dates and parses to ISO 8601 format
3. ✅ Identifies priority keywords and visual cues
4. ✅ Assesses image quality accurately
5. ✅ Returns structured extraction results
6. ✅ Handles poor quality images gracefully with clear errors
7. ✅ Discards image data immediately after processing
8. ✅ Passes all unit and integration tests
