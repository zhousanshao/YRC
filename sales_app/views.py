from django.http import request
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import pandas as pd
import os
from datetime import datetime
from django.conf import settings
from matplotlib import pyplot as plt
import seaborn as sns
from io import BytesIO
import base64

from .forms import HonorForm
from .models import Honor

# 登录视图
def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "用户名或密码错误！")
    return render(request, "sales_app/login.html")

# 登出视图
def user_logout(request):
    logout(request)
    return redirect("login")

# 首页视图
@login_required
def home(request):
    return render(request, "sales_app/home.html")

# 个人业绩查询表单视图
@login_required
def view_individual_form(request):
    return render(request, "sales_app/individual_form.html")

@login_required
def view_individual_performance(request):
    date_str = request.GET.get("date")
    name = request.GET.get("name")
    if not date_str or not name:
        messages.error(request, "日期或姓名不能为空！")
        return redirect("individual_form")

    try:
        date = datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        messages.error(request, "日期格式错误，请输入正确的日期格式（YYYY-MM-DD）。")
        return redirect("individual_form")

    data = load_data_by_date(date, request)
    if data is None or data.empty:
        messages.error(request, "未找到指定日期的数据文件或数据为空！")
        return render(request, "sales_app/individual_performance.html", {
            "error_message": "未找到指定日期的数据文件或数据为空！",
            "date": date_str,
            "name": name,
            "no_performance": True  # 添加标志
        })

    filtered_data = data[data["姓名"] == name]
    if filtered_data.empty:
        # 传递特定的错误信息给模板
        return render(request, "sales_app/individual_performance.html", {
            "error_message": "对不起，该员工当天无业绩",
            "date": date_str,
            "name": name,
            "no_performance": True  # 添加标志
        })
    else:
        data = filtered_data.to_dict(orient="records")  # 转换为列表格式

    return render(request, "sales_app/individual_performance.html", {
        "data": data,
        "date": date_str,
        "name": name,
        "no_performance": False  # 添加标志
    })

# 查看团队业绩
@login_required
def view_team_performance(request):
    date_str = request.GET.get("date")
    if not date_str:
        messages.error(request, "日期不能为空！")
        return redirect("home")

    try:
        date = datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        messages.error(request, "日期格式错误，请输入正确的日期格式（YYYY-MM-DD）。")
        return redirect("home")

    data = load_data_by_date(date)
    if data is None:
        messages.error(request, "未找到指定日期的数据文件！")
        return redirect("home")

    return render(request, "sales_app/team_performance.html", {
        "data": data,
        "date": date_str
    })

#日排行表单查询
@login_required
def daily_ranking_form(request):
    return render(request, "sales_app/daily_ranking_form.html")

@login_required
def daily_ranking(request):
    date_str = request.GET.get("date")
    if not date_str:
        return redirect("daily_ranking_form")

    try:
        date = datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        messages.error(request, "日期格式错误，请输入正确的日期格式（YYYY-MM-DD）。")
        return redirect("daily_ranking_form")

    data = load_data_by_date(date,request)
    if data is None or data.empty:
        messages.error(request, "未找到指定日期的数据文件或数据为空！")
        return redirect("daily_ranking_form")

    # 设置 Matplotlib 支持中文
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定中文字体
    plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

    # 获取当天业绩排行榜
    filtered_data = data.sort_values(by="当天业绩", ascending=False)
    # 过滤掉数据为 0 的条目
    filtered_data= filtered_data[filtered_data["当天业绩"] > 0]

    # 为前三名添加小图标
    medals = ['🥇', '🥈', '🥉'] + [''] * (len(filtered_data) - 3)
    filtered_data["姓名"] = filtered_data["姓名"].apply(lambda x: medals.pop(0) + x)

    # 为条形图指定颜色
    colors = ['#FFD700', '#C0C0C0', '#CD7F32'] + ['#1E90FF'] * (len(filtered_data) - 3)

    # 绘制横向条形图并保存为图片
    plt.figure(figsize=(25, 20))  # 调整图表大小
    plt.barh(filtered_data["姓名"], filtered_data["当天业绩"], color=colors)  # 使用 plt.barh() 绘制横向条形图
    plt.xlabel("当天业绩", fontsize=12)
    plt.ylabel("姓名", fontsize=12)
    plt.title(f"日排行榜 - {date_str}", fontsize=16)
    plt.yticks(rotation=0, fontsize=10)  # 确保姓名标签水平显示
    plt.xticks(fontsize=10)


    # 添加网格线
    plt.grid(axis='x', linestyle='--', alpha=0.6)

    # 保存图表为图片
    chart_path = os.path.join(settings.MEDIA_ROOT, "daily_ranking_chart.png")
    os.makedirs(os.path.dirname(chart_path), exist_ok=True)  # 确保目录存在
    plt.savefig(chart_path, bbox_inches='tight')  # 保存时确保内容完整
    plt.close()

    # 将图片路径传递到模板
    chart_url = settings.MEDIA_URL + "daily_ranking_chart.png"

    return render(request, "sales_app/daily_ranking.html", {
        "data": filtered_data.to_dict(orient="records"),
        "date": date_str,
        "chart_url": chart_url  # 传递图表的 URL
    })

# 月排行榜
@login_required
def monthly_ranking_form(request):
    return render(request, "sales_app/monthly_ranking_form.html")

@login_required
def monthly_ranking(request):
    date_str = request.GET.get("date")
    if not date_str:
        messages.error(request, "日期不能为空！")
        return redirect("monthly_ranking_form")

    try:
        date = datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        messages.error(request, "日期格式错误，请输入正确的日期格式（YYYY-MM-DD）。")
        return redirect("monthly_ranking_form")

    data = load_data_by_date(date,request)
    if data is None or data.empty:
        messages.error(request, "未找到指定日期的数据文件或数据为空！")
        return redirect("monthly_ranking_form")

    # 设置 Matplotlib 支持中文
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定中文字体
    plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

    # 获取当月业绩排行榜
    filtered_data = data.sort_values(by="当月业绩", ascending=False)
    # 过滤掉数据为 0 的条目
    filtered_data = filtered_data[filtered_data["当月业绩"] > 0]

    # 为前三名添加小图标
    medals = ['🥇', '🥈', '🥉'] + [''] * (len(filtered_data) - 3)
    filtered_data["姓名"] = filtered_data["姓名"].apply(lambda x: medals.pop(0) + x)

    # 为条形图指定颜色
    colors = ['#FFD700', '#C0C0C0', '#CD7F32'] + ['#1E90FF'] * (len(filtered_data) - 3)

    # 绘制横向条形图并保存为图片
    plt.figure(figsize=(25, 20))  # 调整图表大小
    plt.barh(filtered_data["姓名"], filtered_data["当月业绩"], color=colors)  # 使用 plt.barh() 绘制横向条形图
    plt.xlabel("当月业绩", fontsize=20)
    plt.ylabel("姓名", fontsize=20)
    plt.title(f"月排行榜 - {date_str}", fontsize=25)
    plt.yticks(rotation=0, fontsize=20)  # 确保姓名标签水平显示
    plt.xticks(fontsize=20)

    # 添加网格线
    plt.grid(axis='x', linestyle='--', alpha=0.6)

    # 保存图表为图片
    chart_path = os.path.join(settings.MEDIA_ROOT, "monthly_ranking_chart.png")
    os.makedirs(os.path.dirname(chart_path), exist_ok=True)  # 确保目录存在
    plt.savefig(chart_path, bbox_inches='tight')  # 保存时确保内容完整
    plt.close()

    # 将图片路径传递到模板
    chart_url = settings.MEDIA_URL + "monthly_ranking_chart.png"

    return render(request, "sales_app/monthly_ranking.html", {
        "data": filtered_data.to_dict(orient="records"),
        "date": date_str,
        "chart_url": chart_url  # 传递图表的 URL
    })

# 荣誉殿堂
@login_required
def add_honor(request):
    if request.method == 'POST':
        form = HonorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('honor_hall')
    else:
        form = HonorForm()
    return render(request, "sales_app/add_honor.html", {"form": form})

@login_required
def honor_hall(request):
    return render(request, "sales_app/honor_hall.html")

#编辑荣誉
@login_required
def edit_honor(request, honor_id):
    honor = get_object_or_404(Honor, id=honor_id)
    if request.method == 'POST':
        form = HonorForm(request.POST, request.FILES, instance=honor)
        if form.is_valid():
            form.save()
            return redirect('honor_hall')
    else:
        form = HonorForm(instance=honor)
    return render(request, "sales_app/edit_honor.html", {"form": form, "honor": honor})

#删除荣誉
@login_required
def delete_honor(request, honor_id):
    honor = get_object_or_404(Honor, id=honor_id)
    if request.method == 'POST':
        honor.delete()
        return redirect('honor_hall')
    return render(request, "sales_app/delete_honor.html", {"honor": honor})

@login_required
def million_club(request):
    # 获取百万俱乐部的员工数据
    million_club_data = Honor.objects.filter(honor_type='百万俱乐部')
    return render(request, "sales_app/million_club.html", {"data": million_club_data})

@login_required
def king_team(request):
    # 获取王者战队的团队数据
    king_team_data = Honor.objects.filter(honor_type='王者战队')
    return render(request, "sales_app/king_team.html", {"data": king_team_data})

@login_required
def flying_star(request):
    # 获取飞跃之星的员工数据
    flying_star_data = Honor.objects.filter(honor_type='飞跃之星')
    return render(request, "sales_app/flying_star.html", {"data": flying_star_data})
#销售看板
@login_required
def sales_dashboard_form(request):
    return render(request, "sales_app/sales_dashboard_form.html")

@login_required
def sales_dashboard(request):
    date_str = request.GET.get("date")
    if not date_str:
        messages.error(request, "日期不能为空！")
        return redirect("sales_dashboard_form")

    try:
        date = datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        messages.error(request, "日期格式错误，请输入正确的日期格式（YYYY-MM-DD）。")
        return redirect("sales_dashboard_form")

    data = load_data_by_date(date, request)
    if data is None or data.empty:
        messages.error(request, "未找到指定日期的数据文件或数据为空！")
        return redirect("sales_dashboard_form")
    

    # 设置 Matplotlib 支持中文
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定中文字体
    plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

    # 生成销售业绩排名条形图
    plt.figure(figsize=(10, 6))
    sns.barplot(x="当天业绩", y="姓名", data=data.sort_values(by="当天业绩", ascending=False))
    plt.title("销售业绩排名")
    plt.xlabel("当天业绩")
    plt.ylabel("姓名")
    bar_chart = get_image()

    # 生成团队业绩占比圆环图
    plt.figure(figsize=(8, 8))
    data.groupby("团队")["当天业绩"].sum().plot(kind="pie", autopct='%1.1f%%', startangle=90, pctdistance=0.85)
    plt.title("团队业绩占比")
    plt.ylabel("")
    circle = plt.Circle((0, 0), 0.70, fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(circle)
    pie_chart = get_image()

    # 生成本月新增客户曲线图
    plt.figure(figsize=(10, 6))
    sns.lineplot(x="日期", y="新增客户", data=data)
    plt.title("本月新增客户")
    plt.xlabel("日期")
    plt.ylabel("新增客户")
    line_chart = get_image()


    return render(request, "sales_app/sales_dashboard.html", {
        "bar_chart": bar_chart,
        "pie_chart": pie_chart,
        "line_chart": line_chart,
        "date": date_str
    })

def get_image():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    return base64.b64encode(image_png).decode('utf-8')




# 加载指定日期的数据
def load_data_by_date(date, request):
    try:
        file_name = date.strftime("%Y-%m-%d") + ".xlsx"
        file_path = os.path.join("data/score", file_name)
        data = pd.read_excel(file_path)
        return data
    except FileNotFoundError:
        messages.error(request, f"未找到日期为 {date} 的数据文件！")
        return None
    except Exception as e:
        messages.error(request, f"加载数据文件失败：{e}")
        return None
