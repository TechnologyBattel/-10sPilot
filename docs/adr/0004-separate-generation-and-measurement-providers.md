# 0004: Separate LLM generation providers from AI-visibility measurement providers

Status: Proposed — pending inspection of router.py/config.py

Context: The AEO router defaults to "openai" but internal routing
sends requests to Groq. Groq/Gemini are appropriate for content
generation and analysis but must not be presented as a measurement
of ChatGPT/Perplexity visibility.

Decision: Introduce two distinct concepts — AIProvider (generation:
Groq, Gemini) and AnswerEngine (measurement: OpenAI, Perplexity,
Gemini, Google AI). Exact wiring TBD pending code inspection.
