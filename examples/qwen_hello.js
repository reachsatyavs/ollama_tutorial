import ollama from 'ollama'

const response = await ollama.chat({
  model: 'qwen3.5:0.8b',
  messages: [{role: 'user', content: 'Hello!'}],
})
console.log(response.message.content)