# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.shortcuts import redirect
import hashlib
from . import models
from . import forms


# Create your views here.


# 首页处理业务
def index(request):
    pass
    return render(request, 'login/index.html')


# 登录处理业务
def login(request):
    if request.session.get('is_login', None):
        return redirect(request, '/index/')
    if 'POST' == request.method:
        # 获取表单
        login_form = forms.UserForm(request.POST)
        message = "所用的信息都需要填写正确！"
        # 校验表单是否为空
        if login_form.is_valid():
            # 获取表单数据
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                # 从数据库中查讯用户密码
                user = models.User.objects.get(name=username)
                # 验证数据库用户密码是否正确
                if user.password == hash_code(password):
                    # 保持session用户数据
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    # 登录成功，重定向到首页
                    return redirect('/index/')
                else:
                    message = "密码错误！"
            except:
                # 查询失败，跳转到重新登录
                message = "用户名不存在！"
        return render(request, 'login/login.html', {"message": message, "login_form": login_form})
    login_form = forms.UserForm()
    return render(request, 'login/login.html', {"login_form": login_form})


# 注册处理业务
def register(request):
    # 检查是否已登录
    if request.session.get('is_login', None):
        return redirect(request, '/index/')
    if request.method == 'POST':
        # 获取表单
        register_form = forms.RegisterForm(request.POST)
        message = "请输入全部的注册内容"
        # 校验表单
        if register_form.is_valid():
            # 获取表单数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            sex = register_form.cleaned_data['sex']
            email = register_form.cleaned_data['email']
            if password2 != password1:
                message = "两次输入的密码不一致！"
                return render(request, 'login/register.html', {"message": message, "register_form": register_form})
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:
                    message = "用户名已存在！请重新选择！"
                    return render(request, 'login/register.html', {"message": message, "register_form": register_form})
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:
                    message = "邮箱已被注册，请选择新的邮箱！"
                    return render(request, 'login/register.html', {"message": message, "register_form": register_form})
                # 创建新用户对象
                new_user = models.User()
                new_user.name = username
                new_user.password = hash_code(password1)
                new_user.gender = sex
                new_user.email = email
                new_user.save()
                return redirect('/login/')
        else:
            return render(request, 'login/register.html', {"register_form": register_form})
    register_form = forms.RegisterForm()
    return render(request, 'login/register.html', {"register_form": register_form})


# 退出处理业务
def logout(request):
    if not request.session.get('is_login', None):
        # 未登录，不必重复登出
        return redirect(request, '/index/')
    request.session.flush()
    return redirect("/index/")


def hash_code(s, salt='mysite'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()
