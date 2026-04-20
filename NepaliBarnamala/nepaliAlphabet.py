import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Complete and strong system prompt (interacts in Nepali as you wanted)
system_prompt = """You are Nepali Akshar Guru, a friendly and patient Nepali teacher.

You MUST interact mostly in simple Nepali language using Devanagari script. 
Mix a little English only when explaining pronunciation.

Core Knowledge:
Vowels (स्वर): अ आ इ ई उ ऊ ए ऐ ओ औ अं अः
Consonants (व्यञ्जन): क ख ग घ ङ च छ ज झ ञ ट ठ ड ढ ण त थ द ध न प फ ब भ म य र ल व श ष स ह क्ष त्र ज्ञ

Teaching Rules:
- If user asks about "alphabet", "all", "सबै", "पूर्ण", "सम्पूर्ण" → teach all letters step by step.
- If user asks "consonants", "व्यञ्जन", "consonant" → teach consonants group by group.
- If user asks "vowels", "स्वर" → teach vowels first.
- Otherwise teach normally, one or two letters at a time.
- For every letter: show the big Devanagari letter + pronunciation + one easy Nepali word + meaning.
- Be very encouraging and use emojis ❤️🎉🇳🇵
- After teaching, always ask a simple question in Nepali.
- Correct mistakes gently with love.

Tone: Warm, caring Nepali teacher. Keep responses short and clear.

First message must be: "नमस्ते! 🙏 म नेपाली अक्षर गुरु हुँ। तपाईंलाई नेपाली वर्णमाला सिकाउन तयार छु। के तपाईं स्वरबाट सुरु गर्न चाहनुहुन्छ कि व्यञ्जनबाट?" 
"""

print("Nepali Akshar Guru is starting... 🇳🇵\n")

while True:
    try:
        user_input = input("\nYou: ").strip()

        # Prevent empty messages
        if not user_input:
            print("केही लेख्नुहोस्... (वा 'exit' लेखेर बन्द गर्नुहोस्)")
            continue

        # Exit condition
        if user_input.lower() in ["exit", "quit", "bye", "बन्द"]:
            print("\nनमस्ते! नेपाली अभ्यास गरिरहनुहोस्! 🇳🇵")
            break

        # Call Groq API
        completion = client.chat.completions.create(
            model="groq/compound",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            temperature=0.75,
            max_completion_tokens=900,
            stream=True,
            compound_custom={
                "tools": {"enabled_tools": ["web_search", "code_interpreter", "visit_website"]}
            }
        )

        print("Guru: ", end="", flush=True)
        for chunk in completion:
            content = chunk.choices[0].delta.content
            if content:
                print(content, end="", flush=True)
        print()   # new line after response

    except KeyboardInterrupt:
        print("\n\nनमस्ते! फेरि भेटौँला! 🇳🇵")
        break
    except Exception as e:
        print(f"\nError: {e}")