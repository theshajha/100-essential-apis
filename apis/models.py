# from django.db import models
# from django.contrib.postgres.fields import ArrayField
#
#
# class ApiCategory(models.Model):
#     name = models.CharField('Category Name', max_length=120, unique=False, null=False, blank=False)
#     description = models.CharField('Category Description', max_length=1024, unique=False, null=True, blank=True)
#     slug = models.CharField('Category Slug', max_length=120, unique=False, null=True, blank=True)
#     updated_at = models.DateTimeField('Updated At', auto_now=True)
#     created_at = models.DateTimeField('Created At', auto_now_add=True)
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         verbose_name = 'API Category'
#         verbose_name_plural = 'API Categories'
#
#
# class ApiList(models.Model):
#     """
#     Model for storing various API types.
#     """
#
#     STATUS_CHOICES = (
#         ('DRAFT', 'Draft'),  # API is not yet ready for publishing only seen by the publisher
#         ('PENDING', 'Pending'),  # API is ready for publishing but not yet approved by the admin
#         ('LIVE', 'Live'),  # API is approved by the admin and is live
#         ('COMING_SOON', 'Coming Soon'),  # API is accepting early access requests
#         ('BETA', 'Beta'),  # API is in beta and may have bugs
#         ('REJECTED', 'Rejected'),  # API is rejected by the admin
#         ('DEPRECATED', 'Deprecated'),  # API is deprecated and will be removed soon
#     )
#
#     name = models.CharField('API Name', max_length=120, unique=False, null=False, blank=False)
#
#     icon = models.CharField('API Icon', max_length=120, unique=False, null=True, blank=True)
#
#     description = models.CharField('API Description', max_length=1024, unique=False, null=True, blank=True)
#
#     long_info = models.TextField('API Long Info', null=True, blank=True)
#
#     banners = ArrayField(models.CharField(max_length=200), null=True, blank=True)
#
#     category = models.ForeignKey(ApiCategory, on_delete=models.SET_NULL, related_name='api_category', null=True,
#                                  blank=True)
#
#     slug = models.SlugField('API Slug', max_length=120, unique=True, null=True, blank=True)
#
#     doc_link = models.CharField('API Doc URL', max_length=120, unique=False, null=True, blank=True)
#
#     demo_link = models.CharField('API Demo URL', max_length=120, unique=False, null=True, blank=True)
#
#     status = models.CharField('API Status', max_length=120, choices=STATUS_CHOICES, default='DRAFT')
#
#     is_active = models.BooleanField(default=True)
#
#     featured = models.BooleanField(default=False)
#
#     updated_at = models.DateTimeField('Updated At', auto_now=True)
#
#     created_at = models.DateTimeField('Created At', auto_now_add=True)
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         verbose_name = 'API'
#         verbose_name_plural = 'APIs'
