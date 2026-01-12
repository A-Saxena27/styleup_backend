"""Simple, explainable content-based recommender for outfits.

Design goals:
- Keep logic transparent for judges: rule-based filtering + simple TF-IDF scoring.
- Return small list (top 3) with per-item score and short reasoning.
"""

from typing import List, Dict, Any
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def _safe_get_user_field(user: Dict[str, Any], key: str, default=""):
    v = user.get(key)
    if v is None:
        return default
    return v


def get_recommendations(user_prefs: Dict[str, Any], wardrobe_items: List[Dict[str, Any]], occasion_filter: str) -> List[Dict[str, Any]]:
    if not wardrobe_items:
        return []

    df = pd.DataFrame(wardrobe_items)

    # Rule-based filtering: occasion must match
    filtered_df = df[df.get('occasion', '') == occasion_filter].copy()
    if filtered_df.empty:
        return []

    # Normalize and fill missing columns
    for col in ['color', 'category', 'tags', 'comfort']:
        if col not in filtered_df.columns:
            filtered_df[col] = '' if col != 'comfort' else 5
        filtered_df[col] = filtered_df[col].fillna('')

    # Build feature string for vectorization
    filtered_df['features'] = (filtered_df['color'].astype(str) + ' ' +
                               filtered_df['category'].astype(str) + ' ' +
                               filtered_df['tags'].astype(str))

    # Build user profile text from explicit preferences
    fav_colors = _safe_get_user_field(user_prefs, 'favorite_colors', [])
    if isinstance(fav_colors, list):
        fav_colors_str = ' '.join(fav_colors)
    else:
        fav_colors_str = str(fav_colors)

    user_profile_components = [fav_colors_str, _safe_get_user_field(user_prefs, 'style', ''), _safe_get_user_field(user_prefs, 'body_type', '')]
    user_profile_str = ' '.join([c for c in user_profile_components if c])

    # TF-IDF similarity between each item's features and user profile
    vectorizer = TfidfVectorizer()
    feature_matrix = vectorizer.fit_transform(filtered_df['features'].tolist() + [user_profile_str])
    cosine_sim = cosine_similarity(feature_matrix[:-1], feature_matrix[-1:]).flatten()

    # Compose final score: base from cosine similarity plus small comfort boost
    comfort_vals = pd.to_numeric(filtered_df.get('comfort', 5), errors='coerce').fillna(5).astype(float)

    # Normalize comfort (1-10) to 0-0.2 weight
    comfort_score = (comfort_vals - 1) / 9.0 * 0.2

    final_score = 0.8 * cosine_sim + comfort_score

    filtered_df['score'] = final_score

    # Build simple explanation components
    explanations = []
    for i, row in filtered_df.iterrows():
        reasons = []
        # color reason
        user_colors = [c.lower() for c in (fav_colors if isinstance(fav_colors, list) else [fav_colors])]
        if any(c.lower() in row['color'].lower() for c in user_colors if c):
            """Simple, explainable content-based recommender for outfits.

            Design goals:
            - Keep logic transparent for judges: rule-based filtering + simple TF-IDF scoring.
            - Return small list (top 3) with per-item score and short reasoning.
            """

            from typing import List, Dict, Any
            import pandas as pd
            from sklearn.feature_extraction.text import TfidfVectorizer
            from sklearn.metrics.pairwise import cosine_similarity


            def _safe_get_user_field(user: Dict[str, Any], key: str, default=""):
                v = user.get(key)
                if v is None:
                    return default
                return v


            def get_recommendations(user_prefs: Dict[str, Any], wardrobe_items: List[Dict[str, Any]], occasion_filter: str) -> List[Dict[str, Any]]:
                if not wardrobe_items:
                    return []

                df = pd.DataFrame(wardrobe_items)

                # Rule-based filtering: occasion must match
                filtered_df = df[df.get('occasion', '') == occasion_filter].copy()
                if filtered_df.empty:
                    return []

                # Normalize and fill missing columns
                for col in ['color', 'category', 'tags', 'comfort']:
                    if col not in filtered_df.columns:
                        filtered_df[col] = '' if col != 'comfort' else 5
                    filtered_df[col] = filtered_df[col].fillna('')

                # Build feature string for vectorization
                filtered_df['features'] = (filtered_df['color'].astype(str) + ' ' +
                                           filtered_df['category'].astype(str) + ' ' +
                                           filtered_df['tags'].astype(str))

                # Build user profile text from explicit preferences
                fav_colors = _safe_get_user_field(user_prefs, 'favorite_colors', [])
                if isinstance(fav_colors, list):
                    fav_colors_str = ' '.join(fav_colors)
                else:
                    fav_colors_str = str(fav_colors)

                user_profile_components = [fav_colors_str, _safe_get_user_field(user_prefs, 'style', ''), _safe_get_user_field(user_prefs, 'body_type', '')]
                user_profile_str = ' '.join([c for c in user_profile_components if c])

                # TF-IDF similarity between each item's features and user profile
                vectorizer = TfidfVectorizer()
                feature_matrix = vectorizer.fit_transform(filtered_df['features'].tolist() + [user_profile_str])
                cosine_sim = cosine_similarity(feature_matrix[:-1], feature_matrix[-1:]).flatten()

                # Compose final score: base from cosine similarity plus small comfort boost
                comfort_vals = pd.to_numeric(filtered_df.get('comfort', 5), errors='coerce').fillna(5).astype(float)

                # Normalize comfort (1-10) to 0-0.2 weight
                comfort_score = (comfort_vals - 1) / 9.0 * 0.2

                final_score = 0.8 * cosine_sim + comfort_score

                filtered_df['score'] = final_score

                # Build simple explanation components
                explanations = []
                for i, row in filtered_df.iterrows():
                    reasons = []
                    # color reason
                    user_colors = [c.lower() for c in (fav_colors if isinstance(fav_colors, list) else [fav_colors])]
                    if any(c.lower() in row['color'].lower() for c in user_colors if c):
                        reasons.append('matches favorite color')
                    # category/style reason
                    if _safe_get_user_field(user_prefs, 'style', '').lower() in str(row['tags']).lower():
                        reasons.append('matches preferred style')
                    # comfort reason
                    if float(row.get('comfort', 5)) >= 7:
                        reasons.append('high comfort')

                    explanations.append('; '.join(reasons) or 'good match')

                filtered_df['explanation'] = explanations

                # Select top 3
                recommendations = filtered_df.sort_values(by='score', ascending=False).head(3)

                # Keep output JSON-serializable and tidy
                out = []
                for _, r in recommendations.iterrows():
                    out.append({
                        '_id': str(r.get('_id', '')),
                        'category': r.get('category', ''),
                        'color': r.get('color', ''),
                        'occasion': r.get('occasion', ''),
                        'comfort': float(r.get('comfort', 5)),
                        'score': float(r.get('score', 0.0)),
                        'explanation': r.get('explanation', '')
                    })

                return out
