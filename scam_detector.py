import os
import google.generativeai as genai
import json
from taxonomy import classify_taxonomy_rule_based

class ScamDetector:
    def __init__(self, api_key=None):
        if api_key:
            genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash', generation_config={"response_mime_type": "application/json"})
        
    def analyze_message(self, message, recent_context, similar_past):
        taxonomy_class = classify_taxonomy_rule_based(message)
        
        context_text = "Recent Messages:\n"
        for ctx in recent_context:
            context_text += f"[{ctx['sender']}]: {ctx['text']}\n"
            
        similar_text = "Similar Past Messages in Memory:\n"
        for sim in similar_past:
             similar_text += f"- {sim['message']}\n"

        prompt = f"""You are an AI tasked with analyzing chat messages for manipulation, scams, and psychological pressure.
Analyze the following new message in the context of recent chat history and similar past messages.

New Message: "{message}"
Taxonomy Classification: {taxonomy_class}

{context_text}
{similar_text}

Provide your analysis in JSON format with exactly the following keys:
- "Risk Level": An integer between 0 and 100
- "Scam Type": String, corresponding to the scam type detected (e.g., normal, phishing, urgency manipulation, etc.)
- "Confidence Score": An integer between 0 and 100 representing how confident you are in this analysis
- "Explanation": A string explaining why you gave this risk level and classification. Include noting any multi-message manipulation patterns if evident from the context.
- "Advice": A string recommending what the user should do next.
"""

        try:
            response = self.model.generate_content(prompt)
            result = json.loads(response.text.strip(' `\njson'))
            
            # Combine rule-based score with LLM score
            llm_score = int(result.get("Risk Level", 0))
            base_score = 10 if taxonomy_class == "NORMAL" else 50
            
            # Use max so that taxonomy doesn't drag down a good LLM detection
            final_score = max(llm_score, base_score)
            
            if taxonomy_class != "NORMAL" and final_score < 40:
                final_score = 40
            
            result["Final Risk Score"] = final_score
            result["Taxonomy Classification"] = taxonomy_class
            return result
        except Exception as e:
            return {
                "Final Risk Score": 10 if taxonomy_class == "NORMAL" else 50,
                "Taxonomy Classification": taxonomy_class,
                "Risk Level": 0,
                "Scam Type": "Error/Rule-based Fallback",
                "Confidence Score": 0,
                "Explanation": f"LLM Analysis failed or API Key is invalid (Error: {str(e)}). Falling back to rule-based taxonomy.",
                "Advice": "Please ensure your Gemini API key is valid. The current score relies entirely on basic keyword rules."
            }
