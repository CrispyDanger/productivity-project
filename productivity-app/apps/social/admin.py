from django.contrib import admin
import social.models as models

admin.site.register(models.SocialProfile)
admin.site.register(models.Post)
admin.site.register(models.Comment)
admin.site.register(models.Topic)
admin.site.register(models.AITopicScore)
admin.site.register(models.AIPostScore)
