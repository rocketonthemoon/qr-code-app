from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import qrcode
import boto3
from botocore.config import Config
import os
from io import BytesIO
import hashlib

# Loading Environment variable (AWS Access Key and Secret Key)
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

# Allowing CORS for local testing
origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

# AWS S3 Configuration
aws_region = os.getenv("AWS_REGION", "eu-north-1")
aws_access_key = os.getenv("AWS_ACCESS_KEY")
aws_secret_key = os.getenv("AWS_SECRET_KEY")

s3_kwargs = {
    "region_name": aws_region,
    "config": Config(
        signature_version="s3v4",
        s3={"addressing_style": "virtual"}
    )
}
if aws_access_key and aws_secret_key:
    s3_kwargs["aws_access_key_id"] = aws_access_key
    s3_kwargs["aws_secret_access_key"] = aws_secret_key

s3 = boto3.client('s3', **s3_kwargs)

bucket_name = os.getenv('BUCKET_NAME')

@app.get("/api/health", status_code=status.HTTP_200_OK, tags=["Health"])
async def health_check():
    return {"status": "ok"}

@app.post("/api/generate-qr/")
async def generate_qr(url: str):
    # Generate QR Code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    
    # Save QR Code to BytesIO object
    img_byte_arr = BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)

    # Generate file name for S3
    url_hash = hashlib.md5(url.encode()).hexdigest()
    file_name = f"qr_codes/{url_hash}.png"

    try:
        # Upload to S3
        s3.put_object(Bucket=bucket_name, Key=file_name, Body=img_byte_arr, ContentType='image/png')
        
        # Generate presigned S3 URL (valid for 15 minutes)
        s3_url = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': file_name},
            ExpiresIn=900
        )
        return {"qr_code_url": s3_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    