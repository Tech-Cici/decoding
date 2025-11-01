import cv2
import numpy as np
from pyzbar.pyzbar import decode
from decoder_utils import load_image, preprocess_image

def decode_barcode(image_path):
    """
    Decode standard barcode (1D barcode) from an image.
    
    Args:
        image_path (str): Path to the image containing barcode
        
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
        
        # Try to decode the barcode
        decoded_objects = decode(gray)
        
        if not decoded_objects:
            # If no barcode found, try with preprocessed image
            processed = preprocess_image(image)
            decoded_objects = decode(processed)
        
        if decoded_objects:
            results = []
            for obj in decoded_objects:
                if obj.type in ['EAN13', 'EAN8', 'UPC', 'CODE128', 'CODE39', 'ITF']:
                    results.append({
                        'type': obj.type,
                        'data': obj.data.decode('utf-8'),
                        'points': obj.polygon
                    })
            return results if results else "No standard barcode found"
        else:
            return "No barcodes found in the image"
            
    except Exception as e:
        return f"Error decoding barcode: {str(e)}"

if __name__ == "__main__":
    # Test the decoder with the provided image
    image_path = "Barcode.jpg"
    result = decode_barcode(image_path)
    print("Barcode Decoding Results:")
    print(result)