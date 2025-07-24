from agents import Agent, Runner, OpenAIChatCompletionsModel, set_tracing_disabled, function_tool
from dotenv import load_dotenv
import os
from openai import AsyncOpenAI
from whatsapp_message import send_whatsapp_message
import asyncio
import chainlit as cl
from typing import List, Dict
from pydantic import BaseModel

load_dotenv()
set_tracing_disabled(True)

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise EnvironmentError("GEMINI_API_KEY not found in environment variables.")

external_client = AsyncOpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=external_client
)

class LawyerProfile(BaseModel):
    name: str
    specialization: str
    experience: str
    location: str
    contact: str
    rating: str
    consultation_fee: str

@function_tool
def get_marriage_counseling_tips(issue_type: str = "general") -> Dict[str, List[str]]:
    tips = {
        "communication": [
            "🗣️ Listen to each other without judgment",
            "💭 Express your feelings calmly",
            "📵 Talk face-to-face without distractions",
            "🤝 Use 'I' statements instead of blame",
            "⏰ Dedicate 15-20 minutes daily for open conversation"
        ],
        "trust": [
            "🤲 Pray for your relationship",
            "💎 Maintain complete transparency",
            "🔒 Forgive past mistakes",
            "📱 Be open about online interactions",
            "🤝 Build trust with small consistent actions"
        ],
        "financial": [
            "💰 Create a monthly budget together",
            "📊 Set financial goals as a couple",
            "🛍️ Discuss big purchases beforehand",
            "💳 Build an emergency fund jointly",
            "📈 Involve your spouse in financial decisions"
        ],
        "family": [
            "👥 Set clear boundaries with in-laws",
            "🏠 Maintain personal space as a couple",
            "🤱 Align on parenting approach",
            "👨‍👩‍👧‍👦 Respect extended family with healthy limits",
            "🎯 Keep your partner the priority"
        ],
        "religious": [
            "🕌 Pray together regularly",
            "📖 Read and discuss Quran together",
            "🤲 Pray for one another",
            "📚 Study Islamic marriage guidance",
            "💫 Support each other in earning spiritual rewards"
        ]
    }
    if issue_type in tips:
        return {issue_type: tips[issue_type]}
    return {"general": tips["communication"] + tips["trust"][:3]}

@function_tool
def get_divorce_consequences() -> Dict[str, List[str]]:
    return {
        "islamic_perspective": [
            "📜 Divorce is the most disliked permissible act in the eyes of Allah",
            "⚖️ It should be a last resort after all reconciliation attempts fail",
            "🤲 Iddah period is mandatory for reflection and possible reconciliation",
            "👥 Try family mediation before final decision",
            "💫 Patience and prayer bring peace"
        ],
        "practical_consequences": [
            "👶 Children may face emotional and psychological impact",
            "💰 Financial stress and legal expenses",
            "🏠 Complications in property division",
            "👨‍👩‍👧‍👦 Tensions in family dynamics",
            "😔 Risk of emotional trauma and depression",
            "🔄 Trust issues in future relationships"
        ],
        "alternatives": [
            "🏥 Seek professional marriage counseling",
            "👨‍🏫 Consult a religious scholar",
            "⏸️ Consider temporary separation",
            "📚 Learn from marriage improvement books/courses",
            "🤝 Involve elders for mediation"
        ]
    }

@function_tool
def get_lawyers_data(specialization: str = "family", city: str = "all") -> List[LawyerProfile]:
    lawyers = [
        {"name": "Advocate Sana Ahmad", "specialization": "Family Law & Divorce Cases", "experience": "12 years", "location": "Lahore", "contact": "+92300-1122334", "rating": "4.8/5", "consultation_fee": "Rs. 5,000"},
        {"name": "Barrister Muhammad Tariq", "specialization": "Islamic Family Law", "experience": "15 years", "location": "Karachi", "contact": "+92301-2233445", "rating": "4.9/5", "consultation_fee": "Rs. 7,000"},
        {"name": "Advocate Farah Khan", "specialization": "Women Rights & Family Disputes", "experience": "10 years", "location": "Islamabad", "contact": "+92302-3344556", "rating": "4.7/5", "consultation_fee": "Rs. 4,500"},
        {"name": "Advocate Ali Hassan", "specialization": "Divorce & Child Custody", "experience": "8 years", "location": "Faisalabad", "contact": "+92303-4455667", "rating": "4.6/5", "consultation_fee": "Rs. 4,000"},
        {"name": "Advocate Ayesha Malik", "specialization": "Family Mediation & Divorce", "experience": "11 years", "location": "Multan", "contact": "+92304-5566778", "rating": "4.8/5", "consultation_fee": "Rs. 4,500"}
    ]
    return [LawyerProfile(**l) for l in lawyers if city.lower() == "all" or city.lower() in l["location"].lower()]

@function_tool
def format_lawyer_message(lawyers: List[LawyerProfile]) -> str:
    if not lawyers:
        return "❌ No lawyers found matching your criteria."

    msg = "⚖️ *FAMILY LAWYERS LIST* ⚖️\n\n"
    msg += "🚨 *Note: These are suggested only after extensive counseling. Please prioritize reconciliation first.*\n\n"
    for i, l in enumerate(lawyers, 1):
        msg += f"*{i}. {l.name}*\n📋 Specialization: {l.specialization}\n⏳ Experience: {l.experience}\n📍 Location: {l.location}\n📞 Contact: {l.contact}\n⭐ Rating: {l.rating}\n💰 Fee: {l.consultation_fee}\n{'─'*35}\n\n"
    msg += "💡 *Shared by RishtaSaver Agent*\n🤲 May Allah guide you with wisdom\n📞 Reach out if you need further support."
    return msg

@function_tool
def get_emergency_support() -> Dict[str, str]:
    return {
        "crisis_helpline": "Rozan Helpline: 0800-22444 (24/7 free)",
        "women_helpline": "Madadgaar National Helpline: 1099",
        "mental_health": "Mental Health Association: +92-21-111-647-725",
        "legal_aid": "Legal Aid Society: 0800-55555",
        "domestic_violence": "Women Crisis Center: 111-911-911"
    }

rishta_saver_agent = Agent(
    name="RishtaSaver Counseling Agent",
    instructions="""
    You are a compassionate marriage counseling AI dedicated to helping users through emotional and relationship crises.

    YOUR MISSION:
    - Prevent divorces whenever possible through practical & spiritual advice
    - Encourage thoughtful decision-making through empathy
    - Provide Islamic guidance aligned with real-life issues
    - Share legal help only after all other options are exhausted

    STYLE:
    - English-only communication
    - Respectful, warm, empathetic tone
    - Offer practical + spiritual solutions together
    - Support without judgment or pressure

    TOOLS:
    - get_marriage_counseling_tips()
    - get_divorce_consequences()
    - get_lawyers_data()
    - format_lawyer_message()
    - send_whatsapp_message()
    - get_emergency_support()

    RESPONSE FLOW:
    - Ask the user for issues in detail
    - Suggest counseling tips first
    - Show divorce impact
    - Ask again if they want to proceed
    - Only then offer lawyer contacts
    """,
    model=model,
    tools=[
        get_marriage_counseling_tips,
        get_divorce_consequences,
        get_lawyers_data,
        format_lawyer_message,
        send_whatsapp_message,
        get_emergency_support
    ]
)

@cl.on_chat_start
async def start():
    cl.user_session.set("history", [])
    cl.user_session.set("counseling_sessions", 0)

    welcome_msg = """
🌟 *Welcome to RishtaSaver Agent* 🌟

💕 I am here to support your marriage and emotional well-being.

🎯 *I can help you with:*
✅ Improving communication and understanding
✅ Resolving trust and financial issues
✅ Providing Islamic and practical guidance
✅ Exploring alternatives to divorce
✅ Recommending lawyers only if needed (as last resort)

🙏 Remember: *Divorce is the most disliked permissible act in Islam.*

💬 Please share your concern, and let’s explore a better path together. 💪
    """
    await cl.Message(welcome_msg).send()

@cl.on_message
async def main(message: cl.Message):
    thinking_msg = await cl.Message("🤔 Thinking...").send()

    history = cl.user_session.get("history") or []
    sessions = cl.user_session.get("counseling_sessions", 0)

    history.append({"role": "user", "content": message.content})
    sessions += 1
    cl.user_session.set("counseling_sessions", sessions)

    try:
        result = Runner.run_sync(
            starting_agent=rishta_saver_agent,
            input=f"Counseling Session #{sessions}\n\nUser Message: {message.content}\n\nPrevious Context: {history[-3:] if len(history) > 1 else 'First session'}"
        )

        history.append({"role": "assistant", "content": result.final_output})
        cl.user_session.set("history", history)

        await cl.Message(content=result.final_output, author="assistant").send()

    except Exception as e:
        error_msg = f"❌ Sorry, there was a technical issue: {str(e)}\n\n"
        error_msg += "🙏 Please try again later or use the emergency helplines:\n"
        error_msg += "📞 Rozan Helpline: 0800-22444 (24/7 free)"

        await cl.Message(content=error_msg, author="assistant").send()
