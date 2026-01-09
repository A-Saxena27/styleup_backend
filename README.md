(The file is empty)
**StyleUp Backend — MVP**

- **Tech stack:** FastAPI (Python), Azure Cosmos DB (MongoDB API), Scikit-learn, Azure OpenAI, Azure App Service
- **Project goal:** provide quick, explainable outfit recommendations and a short AI justification for judges.

**Architecture**
- **API layer:** `app/main.py` + `app/routes.py` (FastAPI)
- **Data layer:** Azure Cosmos DB (MongoDB API) via `pymongo` in `app/models.py`
- **ML & logic:** `app/recommender.py` (rule-based filters + TF-IDF scoring)
- **Chatbot:** `app/chatbot.py` (Azure OpenAI wrapper)

**Database Schemas**
- `users` collection (example fields):
	- `_id` (ObjectId)
	- `name` (string)
	- `height_cm` (int)
	- `body_type` (string)
	- `style` (string)
	- `favorite_colors` (array of strings)
- `wardrobe` collection (example fields):
	- `_id` (ObjectId)
	- `user_id` (ObjectId ref to users)
	- `category` (string)
	- `color` (string)
	- `occasion` (string)
	- `comfort` (int 1-10)
	- `tags` (string)

**ML Logic (plain English)**
- Filter wardrobe items by requested `occasion` (hard rule).
- Build a simple text profile for the user (favorite colors, style, body type).
- Vectorize item `color + category + tags` and the user profile using TF-IDF.
- Compute cosine similarity between each item and user profile (content-based).
- Adjust scores with a small comfort-based boost (transparent weighting).
- Return top 3 items with a short `explanation` and numeric `score`.

**Endpoints**
- `POST /api/register` — body: user object. Returns `user_id`.
- `POST /api/add-wardrobe?user_id={user_id}` — body: wardrobe item. Returns `item_id`.
- `POST /api/recommend-outfit` — body: `{ "user_id": "...", "occasion": "casual" }`. Returns `recommendations` array (top 3).
- `POST /api/chat-styleup` — body: `{ "user_id": "...", "outfit": { ... } }`. Returns `explanation` text from Azure OpenAI.

**Example request / response**
- Register user (curl):

```bash
curl -X POST "http://localhost:8000/api/register" -H "Content-Type: application/json" -d '{"name":"Alex","height_cm":175,"body_type":"athletic","style":"casual","favorite_colors":["blue","white"]}'
```

- Recommend outfit:

```bash
curl -X POST "http://localhost:8000/api/recommend-outfit" -H "Content-Type: application/json" -d '{"user_id":"<USER_ID>", "occasion":"casual"}'
```

- Sample response:

```json
{
	"recommendations": [
		{"_id":"w1","category":"shirt","color":"blue","occasion":"casual","comfort":8,"score":0.92,"explanation":"matches favorite color; high comfort"}
	]
}
```

**Environment variables**
- `COSMOS_MONGO_URI` — Cosmos DB connection string (Mongo API)
- `COSMOS_DB_NAME` — database name (default: `styleup`)
- `AZURE_OPENAI_API_BASE` — Azure OpenAI endpoint (https://your-resource.openai.azure.com)
- `AZURE_OPENAI_KEY` — API key
- `AZURE_OPENAI_DEPLOYMENT` — model deployment name

**Run locally**

1. Create a `.env` file with the variables above.
2. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

3. Run the server:

```bash
uvicorn app.main:app --reload --port 8000
```

**Azure App Service deployment (high level)**
1. Push repo to GitHub.
2. Create an Azure App Service for Linux (Python 3.10+).
3. In App Service settings, configure App Settings with the environment variables above.
4. Configure deployment from GitHub; App Service will install requirements and run `uvicorn app.main:app`.

**Automated GitHub deployment (optional)**

This repo includes a sample GitHub Actions workflow at `.github/workflows/azure-deploy.yml` that will:

- Run on pushes to `main`.
- Set up Python, install dependencies, run tests, and deploy the repository to Azure App Service using a publish profile.

To enable it:

1. Obtain the App Service **Publish Profile** from the Azure portal (Overview -> Get publish profile).
2. Add repository secrets in GitHub:
	- `AZURE_WEBAPP_NAME` — the App Service name
	- `AZURE_WEBAPP_PUBLISH_PROFILE` — contents of the publish profile XML
3. Push to `main` to trigger the workflow.


Questions or want me to run quick local tests? I can start the server and show sample requests.

