import os
from openai import OpenAI

# Note: In a real environment, the user would provide their API key
# client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

class SalesExpert:
    def __init__(self, api_key=None):
        self.api_key = api_key
        # For this demo, we will use a mock response if no key is provided
        if api_key:
            self.client = OpenAI(api_key=api_key)
        else:
            self.client = None

    def generate_pitch(self, lead_data, audit_report):
        business_name = lead_data.get('business_name', 'Business Owner')
        lead_score = audit_report.get('lead_score', 'Gold')
        status = audit_report.get('website_status', 'No Website')

        prompt = f"""
        Business: {business_name}
        Status: {status}
        Score: {lead_score}
        Gaps: Mobile Responsive: {audit_report.get('mobile_responsive')}, WhatsApp: {audit_report.get('has_whatsapp')}, Booking: {audit_report.get('has_booking')}

        Generate a professional sales pitch in Hinglish for this Indian business owner.
        Keep it under 100 words. Highlight one gap and offer a solution.
        """

        if self.client:
            try:
                response = self.client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "system", "content": "You are a Sales Expert for Indian SMEs."},
                              {"role": "user", "content": prompt}]
                )
                return response.choices[0].message.content
            except Exception as e:
                return f"Error generating pitch: {e}"
        else:
            # High-quality fallback templates (Mocking AI)
            if lead_score == "Gold":
                return f"Namaste {business_name}, I saw your great reviews on Google Maps! Lekin aapki koi website nahi mili. Aaj kal patient pehle online check karte hain. Hum aapke liye ek professional site bana sakte hain appointment system ke saath. Kya aap demo dekhna chahenge?"
            elif lead_score == "Silver":
                return f"Hello {business_name}, aapki website mobile pe thik se nahi chalti aur WhatsApp button bhi missing hai. 90% log phone se search karte hain. Hum isse fix karke aapki leads 2x kar sakte hain. Contact karein!"
            else:
                return f"Hi {business_name}, your site is good but missing an automated booking system. We can automate your demo/appointment scheduling. Let's discuss?"

    def handle_objection(self, objection_text):
        # Mock logic for objection handling
        objections = {
            "expensive": "Sir, yeh kharcha nahi investment hai. Ek naya client hi iski cost recover kar dega. Baaki 24/7 marketing free hogi.",
            "developer": "Great! Par kya aapka developer SEO aur conversion optimization (WhatsApp/Booking) pe dhyan de raha hai? Humara focus sirf leads laane pe hai.",
            "not_needed": "Aapka business achha hai, par online presence na hone se naye generation ke clients competitors ke paas ja rahe hain. Safe rehne ke liye digital presence zaroori hai."
        }

        for key in objections:
            if key in objection_text.lower():
                return objections[key]

        return "I understand your concern. Let's hop on a 2-minute call so I can show you how exactly this will increase your revenue."

if __name__ == "__main__":
    expert = SalesExpert()
    print("Test Pitch (Gold Lead):")
    print(expert.generate_pitch({"business_name": "Clinic ABC"}, {"lead_score": "Gold"}))
    print("\nTest Objection (Price):")
    print(expert.handle_objection("It is too expensive for me right now."))
