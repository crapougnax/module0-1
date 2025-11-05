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

tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
chatModel = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")


class Texte(BaseModel):
    texte: str


logger.add("logs/api.log", rotation="500 MB", level="INFO")

app = FastAPI()

chat_history_ids = {}
new_user_input_ids = {}

@app.post("/chat/")
async def anasent(payload: Texte):
    logger.info(f"Received text: {payload.texte}")

    # Translate
    result = translationClient.translation(
        payload.texte,
        model="Helsinki-NLP/opus-mt-fr-en",
    )

    try:
        # encode the new user input, add the eos_token and return a tensor in Pytorch
        new_user_input_ids = tokenizer.encode(tokenizer.eos_token, return_tensors="pt")

        # append the new user input tokens to the chat history
        bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1)

        # generated a response while limiting the total chat history to 1000 tokens,
        chat_history_ids = chatModel.generate(
            bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id
        )

        # pretty print last ouput tokens from bot
        return {
            "message": payload.texte,
            "translation": result,
            "reply": format(
                tokenizer.decode(
                    chat_history_ids[:, bot_input_ids.shape[-1] :][0],
                    skip_special_tokens=True,
                )
            ),
        }
    except Exception as e:
        print(e)
        logger.error(f"Erreur lors de l'analyse: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("api:app", host="0.0.0.0", port=9000, reload=True)
