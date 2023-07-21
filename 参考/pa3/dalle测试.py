import openai
from io import BytesIO
from PIL import Image

# 请在此处输入您的 OpenAI API 密钥
openai.api_key = "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"


def create_image(prompt, n=1, size="1024x1024"):
    response = openai.Image.create(
        prompt=prompt,
        n=n,
        size=size
    )
    image_urls = [data['url'] for data in response['data']]
    return image_urls


# 示例
print(create_image("a white siamese cat"))
