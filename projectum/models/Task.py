from django.db import models
from .Project import Project

class BoardColumn(models.Model):
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='columns')
    name = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.project.name} - {self.name}"


class Task(models.Model):
    class Status(models.TextChoices):
        NOT_STARTED = "NS", "Não iniciada"
        IN_PROGRESS = "IP", "Em desenvolvimento"
        COMPLETED = "CO", "Concluída"

    class Tag(models.TextChoices):
        FEATURE = "FE", "Feature"
        BUG = "BG", "Bug"
        STYLE = "ST", "Estilo/UI"
        DOCUMENTATION = "DC", "Documentação"
        REFACTOR = "RF", "Refatoração"
        TEST = "TS", "Teste"
        PERFORMANCE = "PF", "Performance"

    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=2, choices=Status.choices, default=Status.NOT_STARTED
    )
    tag = models.CharField(
        max_length=2, choices=Tag.choices, default=Tag.FEATURE, blank=True, null=True
    )
    column = models.ForeignKey(BoardColumn, on_delete=models.CASCADE, related_name='tasks')
    position = models.PositiveIntegerField(default=0)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["position", "created_at"]
        verbose_name = "Tarefa"
        verbose_name_plural = "Tarefas"

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"

