from django.db import models
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
from io import BytesIO
import sys
from users.models import CustomUser


from django.db import models
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
from io import BytesIO
import sys
from users.models import CustomUser


class Good(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='goods_images/', max_length=255)
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.image:
            self._process_image()  # Process image before saving
        super().save(*args, **kwargs)

    def _process_image(self):
        """Crop and resize the uploaded image to a 300x300 square."""
        im = Image.open(self.image)
        im = im.convert("RGB")

        # Store EXIF data if available
        exif = im.info.get('exif', None)

        output = BytesIO()
        target_size = 300  # Target square size

        # Get dimensions
        width, height = im.size

        # Crop to square
        if width > height:
            offset = (width - height) // 2
            box = (offset, 0, offset + height, height)
        else:
            offset = (height - width) // 2
            box = (0, offset, width, offset + width)
        im = im.crop(box)

        # Resize to target size
        im = im.resize((target_size, target_size), Image.Resampling.LANCZOS)

        # Save image to BytesIO
        if exif:
            im.save(output, format='JPEG', exif=exif, quality=85)
        else:
            im.save(output, format='JPEG', quality=85)
        output.seek(0)

        # Replace the image field with the processed image
        self.image = InMemoryUploadedFile(
            output,
            'ImageField',
            f"{self.image.name.split('.')[0]}.jpg",
            'image/jpeg',
            sys.getsizeof(output),
            None
        )
