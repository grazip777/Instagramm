"""
permissions
"""
from rest_framework import permissions
from transformers import pipeline

# Загружаем модель для анализа токсичности текста
classifier = pipeline("text-classification", model="unitary/toxic-bert")

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only the author of the post to edit or delete it.
    All users can read, but the post must be checked for toxicity before allowing edits or deletions.
    """

    def has_object_permission(self, request, view, obj):
        # Разрешить чтение всем пользователям (для безопасных методов)
        if request.method in permissions.SAFE_METHODS:
            return True

        # Проверка на токсичность текста перед редактированием или удалением
        if self.is_toxic(obj.content):
            return False  # Если текст токсичен, запрещаем редактирование/удаление

        # Разрешить редактирование или удаление только автору поста
        return obj.author == request.user

    def is_toxic(self, text):
        """
        Проверяет токсичность текста с помощью модели.
        Возвращает True, если текст токсичен, иначе False.
        """
        try:
            result = classifier(text)
            # Если результат пустой или не содержит ожидаемой метки, возвращаем False
            if not result or 'label' not in result[0]:
                return False

            # Проверка на метку токсичности
            toxic_labels = ['LABEL_1', 'toxic']  # В зависимости от модели может быть другая метка
            return result[0]['label'] in toxic_labels
        except Exception as e:
            # Логируем ошибку (если потребуется) и возвращаем False
            print(f"Error during toxicity check: {e}")
