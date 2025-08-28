from google import genai
from google.genai import types
import base64



def generate(text,img_url):
  client = genai.Client(
      vertexai=True,
      project="project-1-XXXXX",
      location="global",
  )

  msg1_image1 = types.Part.from_uri(
      file_uri=img_url
      mime_type="image/jpeg",
  )

  model = "gemini-2.0-flash-preview-image-generation"
  contents = [
    types.Content(
      role="user",
      parts=[
        msg1_image1,
        types.Part.from_text(text=text)
      ]
    ),
  ]

  generate_content_config = types.GenerateContentConfig(
    temperature = 1,
    top_p = 0.95,
    max_output_tokens = 8192,
    response_modalities = ["TEXT", "IMAGE"],
    safety_settings = [types.SafetySetting(
      category="HARM_CATEGORY_HATE_SPEECH",
      threshold="OFF"
    ),types.SafetySetting(
      category="HARM_CATEGORY_DANGEROUS_CONTENT",
      threshold="OFF"
    ),types.SafetySetting(
      category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
      threshold="OFF"
    ),types.SafetySetting(
      category="HARM_CATEGORY_HARASSMENT",
      threshold="OFF"
    ),types.SafetySetting(
      category="HARM_CATEGORY_IMAGE_HATE",
      threshold="OFF"
    ),types.SafetySetting(
      category="HARM_CATEGORY_IMAGE_DANGEROUS_CONTENT",
      threshold="OFF"
    ),types.SafetySetting(
      category="HARM_CATEGORY_IMAGE_HARASSMENT",
      threshold="OFF"
    ),types.SafetySetting(
      category="HARM_CATEGORY_IMAGE_SEXUALLY_EXPLICIT",
      threshold="OFF"
    )],
  )

  img_binary = b''

  for chunk in client.models.generate_content_stream(
      model=model,
      contents=contents,
      config=generate_content_config,
  ):
      try:
          parts = chunk.dict()['candidates'][0]['content']['parts']
          inline_data = parts[0].get('inline_data')
          if inline_data and isinstance(inline_data, dict):
              data_bytes = inline_data.get('data')
              if data_bytes:
                  img_binary += data_bytes
      except Exception as e:
          print(f"Skipped chunk due to: {e}")

  if img_binary:
    with open('static/generated_image.png', 'wb') as f:
        f.write(img_binary)
    print("Image saved as generated_image.png")
  else:
      print("No image data received.")

  return img_binary

