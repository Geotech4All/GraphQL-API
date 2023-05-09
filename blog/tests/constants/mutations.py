create_update_post_image = """
    mutation CreateUpdatePostImage($image: Upload, $description: String) {
        image: createUpdatePostImage (image: $image, description: $description) {
            image
            description
            imageId
        }
    }
"""
