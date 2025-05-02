# 📘 📘 ENGLABS

## 📝 Prompt Instructions

### 📌 Topic Prompt

Please perform the following tasks:

1. Translate the sentence in the "r" field from English to Vietnamese and write the translation in the "t" field.
2. For each object in the "rd" array:
   - Translate the English phrase in the "l1" field to Vietnamese.
   - The translation in the "l2" field must closely match the meaning of the same phrase as it appears in the translated sentence from the "t" field. It should reflect contextual meaning rather than a word-for-word translation.
3. Ensure that all translations are suitable for educational use, sound natural in Vietnamese, and preserve cultural and linguistic accuracy.
4. Do not alter the structure of the JSON or rename any fields. Only fill in the "t" and "l2" fields.
5. Do not include any JSON formatting or structure in your response. Just provide the translated text.

Here is the input JSON:

```json

```

Please return only the updated JSON with the "t" and "l2" fields completed. Do not include any explanations or extra comments.

## 🏷️ Phrase Type Abbreviations

| Code  | Type      | Description                 |
| ----- | --------- | --------------------------- |
| `n`   | Noun      | Person, place, or thing.    |
| `v`   | Verb      | Action word.                |
| `adj` | Adjective | Describes a noun.           |
| `adv` | Adverb    | Describes a verb/adjective. |

## Json

### Topics

#### 🔍 Top-Level Fields

| Field | Type     | Description                                         |
| ----- | -------- | --------------------------------------------------- |
| `id`  | `string` | Unique identifier for the topic (e.g., `"food"`).   |
| `ti`  | `string` | Human-readable title of the topic (e.g., `"Food"`). |
| `w`   | `array`  | List of vocabulary entries related to the topic.    |

---

#### 📚 Inside the `w` Array (Vocabulary Items)

Each object in the `w` array contains:

| Field | Type     | Description                                    |
| ----- | -------- | ---------------------------------------------- |
| `w`   | `string` | A vocabulary word in English, e.g., `"apple"`. |
| `m`   | `array`  | Meanings or usage examples for that word.      |

---

#### 🧠 Inside the `m` Array (Meaning and Example Usage)

Each object in the `m` array includes:

| Field | Type     | Description                                              |
| ----- | -------- | -------------------------------------------------------- |
| `mn`  | `string` | The meaning of the word in the **second language**.      |
| `e`   | `object` | Contains an example sentence and contextual information. |

---

#### ✏️ Inside the `e` Object (Example Sentence)

| Field | Type     | Description                                                                   |
| ----- | -------- | ----------------------------------------------------------------------------- |
| `r`   | `string` | Example sentence in the **first language**.                                   |
| `t`   | `string` | Translation of the sentence in the **second language**.                       |
| `rd`  | `array`  | Detailed breakdown of specific words or phrases with contextual translations. |

---

#### 🧩 Inside the `rd` Array (Reference Details)

Each object in the `rd` array includes:

| Field | Type     | Description                                                        |
| ----- | -------- | ------------------------------------------------------------------ |
| `L1`  | `string` | A word or phrase from the **first language** sentence.             |
| `L2`  | `string` | Its meaning or contextual equivalent in the **second language**.   |
| `t`   | `string` | Type of the word or phrase (e.g., `"n"` for noun, `"v"` for verb). |

---

#### Topics index.json

| Field | Type     | Description                                                             |
| ----- | -------- | ----------------------------------------------------------------------- |
| `id`  | `string` | Unique identifier for the resource (includes a slug and random suffix). |
| `lu`  | `string` | ISO 8601 timestamp indicating when the resource was last updated.       |

---

### 📖 Passages

Passages are structured as educational texts (e.g., paragraphs or full sentences) meant to provide more context than single vocabulary words. These are stored in the `c` array.

---

#### 🏗️ Top-Level Fields (Passages)

| Field | Type     | Description                                                           |
| ----- | -------- | --------------------------------------------------------------------- |
| `id`  | `string` | Unique identifier for the passage (e.g., a slug or hash).             |
| `ti`  | `string` | Human-readable title of the passage.                                  |
| `c`   | `array`  | Content array that holds individual sentences and their translations. |

---

#### 🧾 Inside the `c` Array (Content Items)

Each object in the `c` array represents a sentence with contextual translations.

| Field | Type     | Description                                                                      |
| ----- | -------- | -------------------------------------------------------------------------------- |
| `r`   | `string` | Sentence in the **first language**.                                              |
| `t`   | `string` | Translated sentence in the **second language**.                                  |
| `rd`  | `array`  | Array of breakdowns explaining how phrases or words are translated contextually. |

---

#### 🔍 Inside the `rd` Array (Reference Details for Passages)

Each object inside `rd` serves to explain key phrases or words in a sentence.

| Field | Type     | Description                                                                        |
| ----- | -------- | ---------------------------------------------------------------------------------- |
| `L1`  | `string` | Word or phrase from the sentence in the **first language**.                        |
| `L2`  | `string` | Its corresponding translation or contextual equivalent in the **second language**. |
| `t`   | `string` | Type of the item: `"n"` (noun), `"v"` (verb), `"adj"`, `"adv"`.                    |

---

#### Passages index.json

| Field | Type     | Description                                                             |
| ----- | -------- | ----------------------------------------------------------------------- |
| `id`  | `string` | Unique identifier for the resource (includes a slug and random suffix). |
| `lu`  | `string` | ISO 8601 timestamp indicating when the resource was last updated.       |
