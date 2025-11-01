import cv2
import numpy as np
from pyzbar.pyzbar import decode
from decoder_utils import load_image, preprocess_image

def decode_aztec(image_path):
    """
    Decode Aztec Code from an image.
    
    Args:
        image_path (str): Path to the image containing Aztec Code
        
    Returns:
        str: Decoded data or error message
    """
    try:
        # Load the image
        image = load_image(image_path)
        if image is None:
            return "Failed to load image"
            
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Try to decode the Aztec code
        decoded_objects = decode(gray)
        
        if not decoded_objects:
            # If no code found, try with preprocessed image
            processed = preprocess_image(image)
            decoded_objects = decode(processed)
        
        if decoded_objects:
            results = []
            for obj in decoded_objects:
                if obj.type == 'AZTEC':
                    results.append({
                        'type': obj.type,
                        'data': obj.data.decode('utf-8'),
                        'points': obj.polygon
                    })
            return results if results else "No Aztec Code found"
        else:
            return "No Aztec Codes found in the image"
            
    except Exception as e:
        return f"Error decoding Aztec Code: {str(e)}"

if __name__ == "__main__":
    # Test the decoder with the provided image
    image_path = "Aztec Code.jpg"
    result = decode_aztec(image_path)
    print("Aztec Code Decoding Results:")
    print(result)