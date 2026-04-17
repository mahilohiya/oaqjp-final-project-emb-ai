import requests

def _offline_emotion_fallback(text):
    text_lower = text.lower()

    scores = {
        "anger": 0.05,
        "disgust": 0.03,
        "fear": 0.06,
        "joy": 0.76,
        "sadness": 0.10
    }

    keyword_boosts = {
        "joy": ["happy", "excited", "great", "awesome", "love", "wonderful"],
        "sadness": ["sad", "down", "depressed", "cry", "upset", "lonely"],
        "anger": ["angry", "mad", "furious", "annoyed", "hate"],
        "fear": ["afraid", "scared", "anxious", "worried", "terrified"],
        "disgust": ["disgust", "gross", "nasty", "revolting"]
    }

    for emotion, words in keyword_boosts.items():
        if any(word in text_lower for word in words):
            scores[emotion] += 0.20

    total = sum(scores.values())
    normalized = {emotion: round(value / total, 2) for emotion, value in scores.items()}
    dominant_emotion = max(normalized, key=normalized.get)

    return {
        "anger": normalized["anger"],
        "disgust": normalized["disgust"],
        "fear": normalized["fear"],
        "joy": normalized["joy"],
        "sadness": normalized["sadness"],
        "dominant_emotion": dominant_emotion
    }

def emotion_detector(text_to_analyze):
    empty_result = {
        "anger": None,
        "disgust": None,
        "fear": None,
        "joy": None,
        "sadness": None,
        "dominant_emotion": None
    }

    if not text_to_analyze.strip():
        return empty_result

    url = "https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
    headers = {
        "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"
    }
    payload = {
        "raw_document": {
            "text": text_to_analyze
        }
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=2)
    except requests.RequestException:
        return _offline_emotion_fallback(text_to_analyze)

    if response.status_code == 200:
        emotions = response.json()["emotionPredictions"][0]["emotion"]
        dominant_emotion = max(emotions, key=emotions.get)

        return {
            "anger": emotions["anger"],
            "disgust": emotions["disgust"],
            "fear": emotions["fear"],
            "joy": emotions["joy"],
            "sadness": emotions["sadness"],
            "dominant_emotion": dominant_emotion
        }

    if response.status_code == 400:
        return empty_result

    return _offline_emotion_fallback(text_to_analyze)
    