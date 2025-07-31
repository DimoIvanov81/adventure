import os
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class FileExtensionValidator:
    valid_extensions = ['gpx', 'kml', 'tcx']

    def __init__(self, allowed_extensions=None, message=None):
        self.allowed_extensions = allowed_extensions or self.valid_extensions
        self.message = message

    @property
    def message(self):
        return self.__message

    @message.setter
    def message(self, value):
        if not value:
            self.__message = f'The file must be in the correct format: {", ".join(self.allowed_extensions)}'
        else:
            self.__message = value

    def __call__(self, value):
        ext = os.path.splitext(value.name)[1][1:].lower()
        if ext not in self.allowed_extensions:
            raise ValidationError(self.message)


@deconstructible
class FileSizeValidator:

    def __init__(self, file_size: int = 10, message=None):
        self.file_size = file_size
        self.message = message

    @property
    def message(self):
        return self.__message

    @message.setter
    def message(self, value):
        if value is None:
            self.__message = f"The file size must be equal or below {self.file_size} MB"
        else:
            self.__message = value

    def __call__(self, value):
        if value.size > self.file_size * 1024 * 1024:
            raise ValidationError(self.message)
