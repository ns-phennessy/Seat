from django.contrib import admin

import dashboard.models

admin.site.register(dashboard.models.User)
admin.site.register(dashboard.models.Question)
admin.site.register(dashboard.models.Submission)
admin.site.register(dashboard.models.Exam)
admin.site.register(dashboard.models.Course)
admin.site.register(dashboard.models.Teacher)