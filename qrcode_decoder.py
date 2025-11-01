import cv2
import numpy as np
from pyzbar.pyzbar import decode
from decoder_utils import load_image, preprocess_image

def decode_qrcode(image_path):
    """
    Decode QR Code from an image.
    
    Args:
        image_path (str): Path to the image containing QR Code
        
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
        
        # Try to decode the QR code
        decoded_objects = decode(gray)
        
        if not decoded_objects:
            # If no QR code found, try with preprocessed image
            processed = preprocess_image(image)
            decoded_objects = decode(processed)
        
        if decoded_objects:
            results = []
            for obj in decoded_objects:
                if obj.type == 'QRCODE':
                    results.append({
                        'type': obj.type,
                        'data': obj.data.decode('utf-8'),
                        'points': obj.polygon
                    })
            return results if results else "No QR Code found"
        else:
            return "No QR Codes found in the image"
            
    except Exception as e:
        return f"Error decoding QR Code: {str(e)}"

if __name__ == "__main__":
    # Test the decoder with the provided image
    image_path = "QR Code.jpg"
    result = decode_qrcode(image_path)
    print("QR Code Decoding Results:")
    print(result)