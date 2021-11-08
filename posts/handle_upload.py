import cloudinary
import cloudinary.uploader
import cloudinary.api 

def configure():
    cloudinary.config( 
        cloud_name = "dvcjj1k7a", 
        api_key = "729825675423928", 
        api_secret = "2OFvASzEW_Vp37Hu0mwwSiLKXss" ,
        secure=True
    )

def upload_image(image,filename,folder):
    configure()
    uploadedImage=cloudinary.uploader.upload(image, 
        folder = folder, 
        public_id = filename,
        overwrite = False,
        resource_type = "image")
    result={
        "asset_id":uploadedImage.get('asset_id'),
        "secure_url":uploadedImage.get('secure_url'),
        "created_at":uploadedImage.get('created_at')
    }
    return result