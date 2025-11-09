import uuid
from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from .Tag import Tag


class Project(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DR", "Rascunho"
        ACTIVE = "AT", "Ativo"
        COMPLETED = "CO", "Completo"
        ARCHIVED = "AR", "Arquivado"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200,default="Projeto sem título")
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=2, choices=Status.choices, default=Status.DRAFT
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name="projects")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="authored_projects",
    )
    collaborators = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name="collaborations"
    )
    thumbnail = models.ImageField(
        upload_to="projects/thumbnails/", null=True, blank=True
    )

    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Project"
        verbose_name_plural = "Projects"

    def __str__(self):
        return f"{self.title}"

    def _generate_slug_base(self):
        base = slugify(self.title) if self.title else str(self.id)
        return base[:200] 

    def save(self, *args, **kwargs):
        if not self.slug:
            base = self._generate_slug_base()
            slug = base
            counter = 0
            from django.db.models import Q

            while Project.objects.filter(Q(slug=slug)).exclude(pk=self.pk).exists():
                counter += 1
                slug = f"{base}-{counter}"
            self.slug = slug
        super().save(*args, **kwargs)
