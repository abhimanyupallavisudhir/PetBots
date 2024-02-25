# Functional one -- AS IN: THIS IS NOT A DELETED NOTEBOOK, YOU ARE GOOD TO GO
# ^^^ DELETE THIS LINE IF YOU WANT TO DELETE THIS NOTEBOOK. 9 Feb 2024.

# consistent characters SD
# inpainting
# video: runway? sd video?
# whisper, tts etc.

import openai

cliento = openai.OpenAI()

def dalle(input,
          n = 1,
          model = "dall-e-3",
          size = "1024x1024",
          quality = "standard" # standard, hd
          ):
  response = cliento.images.generate(
    model = model,
    prompt = input,
    size = size,
    quality = quality,
    n = n,
  )
  return response

dalle("")