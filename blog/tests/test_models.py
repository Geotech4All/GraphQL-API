from io import BytesIO
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.core.management import call_command
from django.test import TestCase
from blog.models import PostImage
from PIL import Image
import shutil
from django.test import override_settings

from users.models import CustomUser

TEST_DIR = "test_data"
DEMO_IMAGE = "https://res.cloudinary.com/geotechmedia/image/upload/v1/images/posts/test_img_hztzla"

User = get_user_model()

class PostImageTestCase(TestCase):
    def __init__(self, methodName: str = ...) -> None:
        self.img_description = "Test PostImage"
        self.post_name = "Test post"
        super().__init__(methodName)

    def _get_temp_img(self) -> ContentFile:
        img_io = BytesIO()
        size = (200, 200)
        color = (255, 0, 0)
        image = Image.new("RGB", size, color)
        image.save(img_io, format="JPEG")
        image_content = ContentFile(img_io.getvalue(), "test_img.jpg")
        return image_content

    def _get_created_post_image(self) -> PostImage:
        return PostImage.objects.get(description=self.img_description)

    def _create_test_author(self) -> CustomUser:
        return User.objects.create(email="test@email.com", password="testing_password")

    def _delete_created_post_image(self):
        self._get_created_post_image().delete()

    @override_settings(MEDIA_ROOT=(TEST_DIR + "/media"))
    def setUp(self) -> None:
        # image = self._get_temp_img()
        image = DEMO_IMAGE
        PostImage.objects.create(image=image, description=self.img_description)

    def tearDown(self) -> None:
        print("\n Deleting teporary directory \n")
        try:
            print("\n deleting created podcast \n")
            self._delete_created_post_image()
            call_command("deleteorphanedmedia --noinput")
            print("\n created podcast deleted \n")
        except:
            pass
        try:
            shutil.rmtree(TEST_DIR)
            print(f"\n Deleted {TEST_DIR}")
        except OSError:
            pass
        return super().tearDown()
