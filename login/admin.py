# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from . import models

# Register your models here.

# 创建超级管理员
# username: admin
# password: 123456asdf
# email: admin@admin.com
admin.site.register(models.User)