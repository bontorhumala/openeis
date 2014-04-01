import posixpath

from rest_framework import serializers
from rest_framework.reverse import reverse

from . import models


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Project
        exclude = ('owner',)


# Split file creation from other file operations because the file should
# be unchangeable once it is uploaded and assigned to the user's # project.

class CreateFileSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        self.project = kwargs.pop('project', None)
        super().__init__(*args, **kwargs)

    def restore_object(self, attrs, instance=None):
        if self.project is not None:
            attrs['project'] = self.project
        return super().restore_object(attrs, instance)

    class Meta:
        model = models.DataFile
        read_only_fields = ('project',)


class FileSerializer(serializers.ModelSerializer):
    download_url = serializers.CharField(source='pk', read_only=True)

    class Meta:
        model = models.DataFile
        read_only_fields = ('project', 'file')

    def transform_file(self, obj, value):
        return posixpath.basename(value)

    def transform_download_url(self, obj, value):
        return reverse('datafile-download', kwargs={'pk': value},
                       request=getattr(self, 'request', None))
