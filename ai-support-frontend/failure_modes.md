# ⚠️ Failure Modes & Handling

This document outlines potential failure scenarios in the AI Support Agent system and how each is handled to ensure robustness and reliability.

---

##  1. Missing or Invalid Order ID

###  Scenario

User enters:

```
refund for ORD-9999
```

But the order does not exist in uploaded JSON.

---

###  Problem

* Tool cannot find order
* AI might hallucinate response

---

###  Handling

* `check_refund_eligibility` returns:

```json
{
  "status": "not eligible",
  "reason": "Order not found"
}
```

* Agent generates safe response:

> "I couldn’t find this order. Please check the order ID and try again."

---

###  Why this works

* Prevents hallucination
* Ensures data integrity
* Keeps system trustworthy

---

##  2. No JSON Uploaded (Missing External Data)

###  Scenario

User directly asks:

```
refund for ORD-777
```

without uploading any data.

---

###  Problem

* No `external_data` available
* Tools cannot operate

---

###  Handling

* Tool returns:

```json
{
  "error": "No data available"
}
```

* Agent responds:

> "Please upload your order data first so I can assist you."

---

###  Why this works

* Prevents incorrect assumptions
* Guides user clearly

---

##  3. Invalid JSON Structure

###  Scenario

User uploads malformed JSON:

```json
{
  "wrong_key": []
}
```

---

###  Problem

* `orders` or `products` missing
* Tool lookup fails

---

###  Handling

* Tool safely defaults:

```python
orders = external_data.get("orders", [])
```

* If not found:

```json
{
  "status": "not eligible",
  "reason": "Order not found"
}
```

---

###  Why this works

* No crash
* Graceful degradation

---

##  4. LLM Returns Invalid JSON

###  Scenario

LLM responds with:

```
"Sure, I can help..."
```

instead of structured JSON.

---

###  Problem

* `json.loads()` fails
* Agent pipeline breaks

---

###  Handling

```python
return {
  "error": "Invalid LLM response",
  "raw": text
}
```

* System avoids crash
* Logs raw output for debugging

---

###  Why this works

* Keeps system stable
* Enables debugging

---

##  5. Refund Not Eligible (Business Logic Failure)

###  Scenario

* Product not returnable
* Return window expired
* Order not delivered

---

###  Problem

User expects refund but policy denies

---

###  Handling

Tool returns structured reason:

```json
{
  "status": "not eligible",
  "reason": "Return window has expired"
}
```

Agent responds clearly:

> "Your order is not eligible for a refund because the return window has expired."

---

###  Why this works

* Transparent reasoning
* Matches real-world policies

---

##  6. Backend / API Failure

###  Scenario

* API key invalid
* LLM quota exceeded
* Server error

---

###  Problem

Frontend shows generic failure

---

###  Handling

Backend returns:

```json
{
  "error": "Backend error"
}
```

Frontend shows:

> "Something went wrong. Please try again."

---

###  Why this works

* User-friendly fallback
* Prevents crash UI

---

#  Summary

| Failure            | Handling              |
| ------------------ | --------------------- |
| Missing order      | Safe response         |
| No JSON data       | Prompt user           |
| Invalid JSON       | Graceful fallback     |
| LLM failure        | Error handling        |
| Business rule fail | Clear explanation     |
| API failure        | User-friendly message |

---

# Design Philosophy

*  No crashes
*  No hallucinations
*  Clear user guidance
*  Safe fallbacks
*  Real-world robustness

---
