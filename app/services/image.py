import base64
import google.generativeai as genai

class ImageService:
    def __init__(self, genai_module):
        self.genai = genai_module

    async def analyze_image(self, image_path: str):
        try:
            # Read and encode image
            with open(image_path, "rb") as image_file:
                image_data = image_file.read()
            
            # Use Gemini Vision to analyze image
            model = self.genai.GenerativeModel('gemini-1.5-flash')
            
            # Create the image part
            image_part = {
                "mime_type": "image/jpeg",
                "data": image_data
            }
            
            response = model.generate_content([
                "Analyze this image in detail. Describe what you see, including objects, people, colors, composition, and any notable features or context.",
                image_part
            ])
            
            return {
                "description": response.text
            }
            
        except Exception as e:
            return {
                "description": f"Error analyzing image: {str(e)}"
            }
