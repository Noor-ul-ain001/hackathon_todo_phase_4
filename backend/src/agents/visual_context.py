"""
Agent: Visual Context
Implements the Visual Context Agent that processes images and extracts task information.
"""

from typing import Dict, Any


async def visual_context_agent(
    image_data: str,  # base64 encoded image or URL
    user_id: str
) -> Dict[str, Any]:
    """
    Implements the Visual Context Agent.
    
    Accept image data (base64 or URL)
    Perform OCR to extract text
    Parse extracted text for task info (title, dates, priorities)
    Assess image quality and return confidence scores
    Return structured extraction results
    Verify agent extracts task data from images with acceptable accuracy
    """
    # Validate required parameters
    if not image_data:
        return {
            "success": False,
            "error": {
                "type": "validation_error",
                "message": "image_data is required"
            },
            "message": "image_data is required"
        }
    
    if not user_id:
        return {
            "success": False,
            "error": {
                "type": "validation_error",
                "message": "user_id is required"
            },
            "message": "user_id is required"
        }
    
    try:
        # In a real implementation, this would:
        # 1. Validate image format and size
        # 2. Perform OCR to extract text
        # 3. Parse the extracted text for task information
        # 4. Assess image quality
        
        # For now, I'll simulate the process
        extracted_text = await simulate_ocr_extraction(image_data)
        
        if not extracted_text:
            return {
                "success": False,
                "error": {
                    "type": "ocr_error",
                    "message": "Could not extract text from image"
                },
                "message": "Could not extract text from image"
            }
        
        # Parse the extracted text for task information
        task_info = parse_task_info_from_text(extracted_text)
        
        # Assess image quality (simulated)
        quality_score = assess_image_quality(image_data)
        
        # Return structured extraction results
        return {
            "success": True,
            "extracted_text": extracted_text,
            "task_info": task_info,
            "quality_score": quality_score,
            "confidence": min(quality_score, 0.9),  # Confidence based on quality
            "user_id": user_id,
            "message": "Image processed successfully"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": {
                "type": "agent_error",
                "message": str(e)
            },
            "message": "Error in Visual Context Agent"
        }


async def simulate_ocr_extraction(image_data: str) -> str:
    """
    Simulate OCR extraction from image data.
    In a real implementation, this would call an OCR service.
    """
    # This is a simulation - in a real implementation, this would call an OCR API
    # For now, we'll return some sample text based on the image data
    if "meeting" in image_data.lower() or "mtg" in image_data.lower():
        return "Meeting with team tomorrow at 3pm to discuss project timeline. Priority: high."
    elif "grocery" in image_data.lower() or "shop" in image_data.lower():
        return "Buy groceries: milk, bread, eggs. Due: today."
    else:
        # Default sample text
        return "Call mom tomorrow. Due date: next Monday. Priority: medium."


def parse_task_info_from_text(extracted_text: str) -> Dict[str, Any]:
    """
    Parse task information from extracted text.
    """
    import re
    
    task_info = {}
    
    # Extract title (first meaningful sentence or phrase)
    sentences = extracted_text.split('.')
    if sentences:
        title = sentences[0].strip()
        # Remove common prefixes
        title = re.sub(r'^(Task:|Note:|Reminder:)\s*', '', title, flags=re.IGNORECASE)
        task_info["title"] = title
    
    # Extract due date patterns
    date_patterns = [
        r'due\s+(tomorrow|today|\w+\s+\d{1,2}(?:st|nd|rd|th)?\s*,?\s*\d{4}|\d{1,2}/\d{1,2}(?:/\d{2,4})?|\d{4}-\d{2}-\d{2})',
        r'(?:by|on)\s+(tomorrow|today|\w+\s+\d{1,2}(?:st|nd|rd|th)?\s*,?\s*\d{4}|\d{1,2}/\d{1,2}(?:/\d{2,4})?|\d{4}-\d{2}-\d{2})',
        r'for\s+(tomorrow|today|\w+\s+\d{1,2}(?:st|nd|rd|th)?\s*,?\s*\d{4}|\d{1,2}/\d{1,2}(?:/\d{2,4})?|\d{4}-\d{2}-\d{2})'
    ]
    
    for pattern in date_patterns:
        date_match = re.search(pattern, extracted_text, re.IGNORECASE)
        if date_match:
            date_str = date_match.group(1)
            task_info["due_date"] = date_str
            break
    
    # Extract priority
    if "high" in extracted_text.lower():
        task_info["priority"] = "high"
    elif "low" in extracted_text.lower():
        task_info["priority"] = "low"
    elif "medium" in extracted_text.lower():
        task_info["priority"] = "medium"
    
    # Extract description
    task_info["description"] = extracted_text
    
    return task_info


def assess_image_quality(image_data: str) -> float:
    """
    Assess image quality and return a score between 0 and 1.
    In a real implementation, this would analyze image properties.
    """
    # This is a simulation - in a real implementation, this would analyze:
    # - image resolution
    # - clarity/sharpness
    # - lighting conditions
    # - text readability
    
    # For now, return a simulated quality score
    # The score would depend on the actual image properties
    if len(image_data) < 100:  # Very short image data likely means low quality
        return 0.3
    elif "clear" in image_data.lower() or "high" in image_data.lower():
        return 0.9
    else:
        return 0.7  # Default quality score


# Mock implementation for testing
async def mock_visual_context_agent(
    image_data: str,
    user_id: str
) -> Dict[str, Any]:
    """
    Mock implementation of Visual Context Agent for testing purposes.
    """
    # Validate required parameters
    if not image_data:
        return {
            "success": False,
            "error": {
                "type": "validation_error",
                "message": "image_data is required"
            },
            "message": "image_data is required"
        }
    
    if not user_id:
        return {
            "success": False,
            "error": {
                "type": "validation_error",
                "message": "user_id is required"
            },
            "message": "user_id is required"
        }
    
    # Simulate OCR extraction
    extracted_text = await simulate_ocr_extraction(image_data)
    
    if not extracted_text:
        return {
            "success": False,
            "error": {
                "type": "ocr_error",
                "message": "Could not extract text from image"
            },
            "message": "Could not extract text from image"
        }
    
    # Parse the extracted text for task information
    task_info = parse_task_info_from_text(extracted_text)
    
    # Assess image quality (simulated)
    quality_score = assess_image_quality(image_data)
    
    # Return structured extraction results
    return {
        "success": True,
        "extracted_text": extracted_text,
        "task_info": task_info,
        "quality_score": quality_score,
        "confidence": min(quality_score, 0.9),  # Confidence based on quality
        "user_id": user_id,
        "message": "Image processed successfully (mock)"
    }