<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}个人博客{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/main.css') }}">
</head>
<body>
    <nav class="nav-bar">
        <div class="nav-container">
            <div class="nav-logo">
                <a href="/">张二毛</a>
            </div>
            <div class="nav-links">
                <a href="/" class="active">首页</a>
                <a href="/about">关于</a>
                <a href="/friends">友链</a>
                {% if session.get('logged_in') %}
                    <a href="{{ url_for('logout') }}">注销</a>
                {% else %}
                    <a href="{{ url_for('login') }}">登录</a>
                {% endif %}
            </div>
            <div class="nav-search">
                <input type="text" placeholder="请输入关键字...">
            </div>
        </div>
    </nav>
    <div class="container">
        <main>
            {% block content %}{% endblock %}
        </main>
    </div>
</body>
</html>