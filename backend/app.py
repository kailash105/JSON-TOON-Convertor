from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from converter import json_to_toon
from tokenizer import count_tokens, calculate_cost

app = FastAPI(title="LLM Prompt Optimizer")

class JSONInput(BaseModel):
    data: dict

@app.post("/optimize")
async def optimize(input_data: JSONInput):
    try:
        data = input_data.data

        if not data:
            raise HTTPException(status_code=400, detail="Request body cannot be empty")

        json_str = str(data)
        toon_str = json_to_toon(data)

        json_tokens = count_tokens(json_str)
        toon_tokens = count_tokens(toon_str)

        if json_tokens == 0:
            raise HTTPException(status_code=400, detail="Unable to calculate tokens — check input format")

        json_cost = calculate_cost(json_tokens)
        toon_cost = calculate_cost(toon_tokens)

        return {
            "json_tokens": json_tokens,
            "toon_tokens": toon_tokens,
            "savings_percent": round((1 - toon_tokens / json_tokens) * 100, 2),
            "cost_json": json_cost,
            "cost_toon": toon_cost,
            "toon_output": toon_str
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
