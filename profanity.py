from transformers import pipeline

profanity_pipe = pipeline("text-classification",
                          model="parsawar/profanity_model_3.1")


def predict_profanity(content: str):
    return profanity_pipe.predict(content)[
        0]['label'] == '1'
