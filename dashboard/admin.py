from django.contrib import admin

import seat.models

admin.site.register(seat.models.User)
admin.site.register(seat.models.Question)
admin.site.register(seat.models.Submission)
admin.site.register(seat.models.Exam)
admin.site.register(seat.models.Course)
admin.site.register(seat.models.Teacher)