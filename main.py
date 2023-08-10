from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from rembg import remove
from PIL import Image
from io import BytesIO


app = FastAPI()

origins = [
    # Add the list of origins you'd like to allow requests from (if your frontend is hosted elsewhere)
    # For example: "http://localhost:3000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/remove-bg/")
async def remove_bg(file: UploadFile = UploadFile(...)):
    try:
        # Read image from the request
        image_data = await file.read()
        image = Image.open(BytesIO(image_data))
        
        # Remove background
        output = remove(image)
        img_byte_array = BytesIO()
        output.save(img_byte_array, format="PNG")
        
        # Return the modified image
        return {"image": img_byte_array.getvalue().decode("latin1")}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing image: {e}")




