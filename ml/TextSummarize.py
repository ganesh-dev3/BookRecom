from transformers import GPT2Tokenizer

from ollama import Client

class TextSummary():
    def __init__(self):
        self.client = Client(host='http://localhost:11434')
        self.connect_to_server()
        self.tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

    def connect_to_server(self):
            # Check if the required model is available. If not, pull it.
        model_name = "llama3:8b"
        try:
            self.client.show(model_name)
        except:
            self.client.pull(model_name)

    def chunk_text(self, text, max_length=2000):
        tokens = self.tokenizer.encode(text)
        chunks = []

        start = 0
        while start < len(tokens):
            end = min(start + max_length, len(tokens))
            chunk = self.tokenizer.decode(tokens[start:end])
            chunks.append(chunk)
            start = end

        return chunks

    def generate_response_from_text(self, text):
        try:
            chunks = self.chunk_text(text, max_length=2000)
            chunk_prompts = [f"\n\n{chunk}" for chunk in chunks]

            response = self.client.chat(
                model="llama3:8b",
                messages=[{"role": "user", "content": "\n\n".join(chunk_prompts)}]
            )
            generated_text = response.get('message', {}).get('content', '').strip()

            return generated_text
        except Exception as e:
            raise RuntimeError(f"Error generating response: {str(e)}") from e