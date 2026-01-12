from fastapi.testclient import TestClient
from app.main import app
from app.models import connect_db


def run():
    connect_db()
    client = TestClient(app)

    # Register user
    from fastapi.testclient import TestClient
    from app.main import app
    from app.models import connect_db


    def run():
        connect_db()
        client = TestClient(app)

        # Register user
        r = client.post('/api/register', json={
            "name": "Test",
            "height_cm": 170,
            "body_type": "average",
            "style": "casual",
            "favorite_colors": ["blue"]
        })
        print('register', r.status_code, r.json())
        user_id = r.json().get('user_id')

        # Add wardrobe items
        items = [
            {"category": "shirt", "color": "blue", "occasion": "casual", "comfort": 8, "tags": "cotton casual"},
            {"category": "jeans", "color": "black", "occasion": "casual", "comfort": 7, "tags": "denim"},
            {"category": "coat", "color": "red", "occasion": "formal", "comfort": 6, "tags": "wool"}
        ]

        for it in items:
            r = client.post(f'/api/add-wardrobe?user_id={user_id}', json=it)
            print('add', r.status_code, r.json())

        # Recommend
        r = client.post('/api/recommend-outfit', json={"user_id": user_id, "occasion": "casual"})
        print('recommend', r.status_code, r.json())

        # Chat (fallback)
        recs = r.json().get('recommendations')
        if recs:
            outfit = recs[0]
            r2 = client.post('/api/chat-styleup', json={"user_id": user_id, "outfit": outfit})
            print('chat', r2.status_code, r2.json())


    if __name__ == '__main__':
        run()
    r = client.post('/api/register', json={
