from fastapi import FastAPI, HTTPException
from loguru import logger
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import os
from huggingface_hub import InferenceClient

translationClient = InferenceClient(
    provider="hf-inference",
    api_key=os.environ["HF_TOKEN"],
)

sentimentClient = InferenceClient(
    provider="hf-inference",
    api_key=os.environ["HF_TOKEN"],
)

tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
chatModel = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")


class Texte(BaseModel):
    texte: str


logger.add("logs/api.log", rotation="500 MB", level="INFO")

app = FastAPI()


@app.post("/chat/")
async def anasent(payload: Texte):
    logger.info(f"Received text: {payload.texte}")

    # Translate
    result = translationClient.translation(
        payload.texte,
        model="Helsinki-NLP/opus-mt-fr-en",
    )

    try:
        messages = [{"role": "user", "content": result.translation_text}]
        inputs = tokenizer.apply_chat_template(
            messages,
            add_generation_prompt=True,
            tokenize=True,
            return_dict=True,
            return_tensors="pt",
        ).to(chatModel.device)

        outputs = chatModel.generate(**inputs, max_new_tokens=40)

        return {
            "message": payload.texte,
            "translation": result.translation_text,
            "sentiment": sentimentClient.text_classification(
                result.translation_text,
                model="nlptown/bert-base-multilingual-uncased-sentiment",
                top_k=1,
            ),
            "reply": tokenizer.decode(outputs[0][inputs["input_ids"].shape[-1] :]),
        }
    except Exception as e:
        print(e)
        logger.error(f"Erreur lors de l'analyse: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("api:app", host="0.0.0.0", port=9000, reload=True)
