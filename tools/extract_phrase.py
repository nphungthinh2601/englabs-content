import os
import json
import spacy
import random
import string
from typing import List, Set, Dict, Tuple
from spacy.tokens import Span
from google import genai
from dotenv import load_dotenv

load_dotenv()
nlp = spacy.load("en_core_web_lg")

"""
# Phrase Extraction Prompt using spaCy (en_core_web_lg)

## Objective

Write a Python function named `def extract_phrase(text: str) -> str:` using the spaCy library with the `en_core_web_lg` model to analyze a given English sentence and extract its linguistic components, including:

- **Noun phrases** (noun_phrases)
- **Noun chunks** (noun_chunks)
- **Prepositional phrases**
- **Verb phrases**
- **Adjective phrases**
- **Adverb phrases**
- **Pronouns**
- **Verbs**
- **Adjectives**
- **Adverbs**
- **Determiners**

All variables within the function must have clearly defined types using type hints.

## Output Format

The output should be a JSON string with the following structure:

```json
{
    "r": "<raw_sentence>",
    "t": "",
    "rd": [
        {"l1": "<phrase_or_token>", "l2": "", "t": "<type>"}
    ]
}
```

- Use the `t` field to denote the type of the item:
  - `"n"` for noun phrases or noun chunks
  - `"v"` for verbs or verb phrases
  - `"prep"` for prepositional phrases
  - `"adj"` for adjectives or adjective phrases
  - `"adv"` for adverbs or adverb phrases
  - `"pron"` for pronouns
  - `"det"` for determiners

## Rules and Constraints

1. Prioritize **phrases and chunks** over individual tokens, and prioritize **smaller phrases or chunks** with lengths in the range of **2 to 7 tokens** over longer ones.

2. If a phrase (of any type listed above) exceeds **7 tokens**, attempt to **split** it into subphrases with lengths in the range of **2 to 7 tokens**, prioritizing **shorter subphrases first**.  
   - Example: A 12-token phrase can be split into [2, 2, 5, 3].

3. If a phrase is exactly 7 tokens long and can be split (e.g., [4, 3]), perform the split to prioritize smaller phrases.

4. **Eliminate any duplicated or overlapping tokens or subphrases** that are already **contained within** another phrase or chunk to ensure non-redundant output.

5. **Subphrases or chunks** split from larger phrases must remain meaningful and be classified according to the following prioritized types:
   - **Noun phrases** (noun_phrases)
   - **Noun chunks** (noun_chunks)
   - **Prepositional phrases**
   - **Verb phrases**
   - **Adjective phrases**
   - **Adverb phrases**
   - **Pronouns**
   - **Verbs**
   - **Adjectives**
   - **Adverbs**
   - **Determiners**

   The smaller phrases or chunks should be contextually meaningful and fit within the defined types in order of priority.

## Use Case

This prompt is designed for educational applications such as:
- Vocabulary acquisition
- Phrase-level grammar learning
- Interactive sentence breakdown

The final output should be clear, non-overlapping, and useful for linguistic or pedagogical purposes.
"""
def extract_phrase(text: str) -> str:
    # Load spaCy model
    nlp = spacy.load("en_core_web_lg")
    doc = nlp(text)

    # Initialize result structure
    result: Dict[str, any] = {
        "r": text,
        "t": "",
        "rd": []
    }
    
    # Track used tokens to avoid overlaps
    used_tokens: Set[int] = set()
    
    # Helper function to check if span overlaps with used tokens
    def is_span_available(span: Span) -> bool:
        return all(i not in used_tokens for i in range(span.start, span.end))
    
    # Helper function to mark tokens as used
    def mark_tokens_used(span: Span) -> None:
        for i in range(span.start, span.end):
            used_tokens.add(i)
    
    # Helper function to split long phrases
    def split_long_phrase(span: Span) -> List[Span]:
        if len(span) <= 7:
            return [span]
        
        subphrases: List[Span] = []
        remaining = span
        while len(remaining) > 7:
            # Try to find a natural split point (e.g., at a conjunction or comma)
            split_point = min(4, len(remaining) - 3)  # Prefer 4-token chunks
            for i in range(2, 6):
                if i < len(remaining) and remaining[i].pos_ in ("CCONJ", "PUNCT"):
                    split_point = i
                    break
            subphrases.append(remaining[:split_point])
            remaining = remaining[split_point:]
        if len(remaining) >= 2:
            subphrases.append(remaining)
        return subphrases

    # Collect phrases and tokens by priority
    candidates: List[Tuple[Span, str]] = []
    
    # 1. Noun phrases and noun chunks
    for chunk in doc.noun_chunks:
        if is_span_available(chunk):
            candidates.append((chunk, "n"))
    
    # 2. Prepositional phrases
    for token in doc:
        if token.pos_ == "ADP" and token.head:
            prep_phrase = [token]
            for child in token.children:
                if child.dep_ in ("pobj", "prep", "advmod"):
                    prep_phrase.extend([t for t in child.subtree])
            if prep_phrase:
                start = min(t.i for t in prep_phrase)
                end = max(t.i for t in prep_phrase) + 1
                span = doc[start:end]
                if is_span_available(span) and 2 <= len(span) <= 7:
                    candidates.append((span, "prep"))
    
    # 3. Verb phrases
    for token in doc:
        if token.pos_ == "VERB":
            verb_phrase = [token]
            for child in token.children:
                if child.dep_ in ("aux", "advmod", "neg"):
                    verb_phrase.append(child)
            if verb_phrase:
                start = min(t.i for t in verb_phrase)
                end = max(t.i for t in verb_phrase) + 1
                span = doc[start:end]
                if is_span_available(span) and 2 <= len(span) <= 7:
                    candidates.append((span, "v"))
    
    # 4. Adjective phrases
    for token in doc:
        if token.pos_ == "ADJ":
            adj_phrase = [token]
            for child in token.children:
                if child.dep_ == "advmod":
                    adj_phrase.append(child)
            if len(adj_phrase) > 1:
                start = min(t.i for t in adj_phrase)
                end = max(t.i for t in adj_phrase) + 1
                span = doc[start:end]
                if is_span_available(span):
                    candidates.append((span, "adj"))
    
    # 5. Adverb phrases
    for token in doc:
        if token.pos_ == "ADV":
            adv_phrase = [token]
            for child in token.children:
                if child.dep_ == "advmod":
                    adv_phrase.append(child)
            if len(adv_phrase) > 1:
                start = min(t.i for t in adv_phrase)
                end = max(t.i for t in adv_phrase) + 1
                span = doc[start:end]
                if is_span_available(span):
                    candidates.append((span, "adv"))
    
    # 6. Individual tokens (pronouns, verbs, adjectives, adverbs, determiners)
    for token in doc:
        if token.i not in used_tokens:
            if token.pos_ == "PRON":
                candidates.append((doc[token.i:token.i+1], "pron"))
            elif token.pos_ == "VERB":
                candidates.append((doc[token.i:token.i+1], "v"))
            elif token.pos_ == "ADJ":
                candidates.append((doc[token.i:token.i+1], "adj"))
            elif token.pos_ == "ADV":
                candidates.append((doc[token.i:token.i+1], "adv"))
            elif token.pos_ == "DET":
                candidates.append((doc[token.i:token.i+1], "det"))
    
    # Process candidates and split long phrases
    final_phrases: List[Tuple[Span, str]] = []
    for span, phrase_type in candidates:
        if len(span) > 7:
            subphrases = split_long_phrase(span)
            for sub in subphrases:
                if is_span_available(sub) and 2 <= len(sub) <= 7:
                    final_phrases.append((sub, phrase_type))
                    mark_tokens_used(sub)
        elif len(span) == 7:
            # Try to split into smaller meaningful phrases
            subphrases = split_long_phrase(span)
            for sub in subphrases:
                if is_span_available(sub):
                    final_phrases.append((sub, phrase_type))
                    mark_tokens_used(sub)
        else:
            if is_span_available(span):
                final_phrases.append((span, phrase_type))
                mark_tokens_used(span)
    
    # Build result
    for span, phrase_type in final_phrases:
        result["rd"].append({
            "l1": span.text,
            "l2": "",
            "t": phrase_type
        })
    
    return json.dumps(result, ensure_ascii=False)

def build_translation_prompt(json: str) -> str:
    return """Please perform the following tasks:

1. Translate the sentence in the "r" field from English to Vietnamese and write the translation in the "t" field.
2. For each object in the "rd" array:
   - Translate the English phrase in the "l1" field to Vietnamese.
   - The translation in the "l2" field must closely match the meaning of the same phrase as it appears in the translated sentence from the "t" field. It should reflect contextual meaning rather than a word-for-word translation.
3. Ensure that all translations are suitable for educational use, sound natural in Vietnamese, and preserve cultural and linguistic accuracy.
4. Do not alter the structure of the JSON or rename any fields. Only fill in the "t" and "l2" fields.
5. Do not include any JSON formatting or structure in your response. Just provide the translated text.

Here is the input JSON:

```json
%s
```

Please return only the updated JSON with the "t" and "l2" fields completed. Do not include any explanations or extra comments.""" % json

def translate_extract_phrase(raw: str) -> str:
    extract = extract_phrase(raw)
    prompt = build_translation_prompt(extract)
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=[prompt]
    )
    result = response.text.replace("```json\n", "").replace("```", "")
    return json.loads(result)

def split_into_sentences(paragraph: str) -> list[str]:
    doc = nlp(paragraph)
    return [sent.text.strip() for sent in doc.sents]

def generate_random_string(length: int = 10) -> str:
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def to_pascal_case(text: str) -> str:
    return ' '.join(word.capitalize() for word in text.split('_'))

def passage_to_json(file: str, lang: str):
    with open(file, "r", encoding="utf-8") as f:
        content = f.read()

    sentences = split_into_sentences(content)

    results = []
    for sentence in sentences:
        result = translate_extract_phrase(sentence)
        results.append(result)

    random_string = generate_random_string(10)
    base_filename = os.path.basename(file).replace(".txt", "")
    title = to_pascal_case(base_filename)
    json_filename = base_filename + ".json"
    output_path = os.path.join("..", lang, "passages", json_filename)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump({
                    "id": f"{base_filename}_{random_string}",
                    "ti": title,
                    "c": results
                }, f, ensure_ascii=False)