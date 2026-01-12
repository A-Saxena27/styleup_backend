import os
import openai
from dotenv import load_dotenv

load_dotenv()

# Azure OpenAI configuration via environment
API_BASE = os.environ.get('AZURE_OPENAI_API_BASE')
API_KEY = os.environ.get('AZURE_OPENAI_KEY')
DEPLOYMENT = os.environ.get('AZURE_OPENAI_DEPLOYMENT')
API_VERSION = os.environ.get('AZURE_OPENAI_API_VERSION', '2023-05-15')

if API_KEY and API_BASE:
	openai.api_type = "azure"
	openai.api_version = API_VERSION
	openai.api_base = API_BASE
	openai.api_key = API_KEY
import os
import openai
from dotenv import load_dotenv

load_dotenv()

# Azure OpenAI configuration via environment
API_BASE = os.environ.get('AZURE_OPENAI_API_BASE')
API_KEY = os.environ.get('AZURE_OPENAI_KEY')
DEPLOYMENT = os.environ.get('AZURE_OPENAI_DEPLOYMENT')
API_VERSION = os.environ.get('AZURE_OPENAI_API_VERSION', '2023-05-15')

if API_KEY and API_BASE:
	openai.api_type = "azure"
	openai.api_version = API_VERSION
	openai.api_base = API_BASE
	openai.api_key = API_KEY


def explain_outfit(outfit: dict, user: dict) -> str:
	"""Call Azure OpenAI to produce an explainable, judge-friendly justification.

	The function keeps the prompt simple and constrained for predictable outputs.
	"""
	if not DEPLOYMENT:
		# graceful fallback: return handcrafted explanation
		parts = [f"This {outfit.get('category')} in {outfit.get('color')} is recommended because {outfit.get('explanation', 'it suits your preferences')}."]
		return ' '.join(parts)

	prompt = (
		f"You are StyleUp, a helpful fashion assistant.\n"
		f"User profile: name={user.get('name')}, height={user.get('height_cm')}, body_type={user.get('body_type')}, style={user.get('style')}, favorite_colors={user.get('favorite_colors')}.\n"
		f"Outfit: category={outfit.get('category')}, color={outfit.get('color')}, occasion={outfit.get('occasion')}, comfort={outfit.get('comfort')}.\n"
		"Explain in 2-3 short sentences why this outfit is a good match for the user, focusing on style, color, and comfort. Keep language simple and non-technical."
	)

	try:
		resp = openai.ChatCompletion.create(
			engine=DEPLOYMENT,
			messages=[{"role": "system", "content": "You are a concise fashion assistant."},
					  {"role": "user", "content": prompt}],
			max_tokens=150,
			temperature=0.3,
		)
		text = resp['choices'][0]['message']['content'].strip()
		return text
	except Exception:
		parts = [f"This {outfit.get('category')} in {outfit.get('color')} is recommended because {outfit.get('explanation', 'it suits your preferences')}."]
		return ' '.join(parts)

