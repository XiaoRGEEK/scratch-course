#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成课程索引HTML文件
遍历course文件夹，生成类似course.json的数据结构，然后生成index.html
包含步骤弹窗功能
"""

import os
import json
from pathlib import Path

API="https://xiaorgeek.github.io/scratch-course/"

def scan_course_directory():
    """扫描course目录，生成课程数据结构"""
    
    course_data = {
        "code": 200,
        "data": {}
    }
    
    course_path = Path("course")
    
    # 遍历所有子目录
    for category_dir in course_path.iterdir():
        if not category_dir.is_dir():
            continue
            
        category_name = category_dir.name
        print(f"扫描类别: {category_name}")
        
        # 遍历类别下的课程目录
        for lesson_dir in category_dir.iterdir():
            if not lesson_dir.is_dir():
                continue
                
            lesson_name = lesson_dir.name
            print(f"  扫描课程: {lesson_name}")
            
            # 生成课程键名
            course_key = f"{category_name}_{lesson_name}"
            
            # 确定标签
            tags = [category_name]
            
            # 查找课程文件
            sb3_files = list(lesson_dir.glob("*.sb3"))
            image_files = list(lesson_dir.glob("*.jpg")) + list(lesson_dir.glob("*.png"))
            
            # 获取SB3文件
            sb3_file = sb3_files[0] if sb3_files else None
            sb3_uri = f"{API}course/{category_name}/{lesson_name}/{sb3_file.name}" if sb3_file else None
            
            # 获取图片文件
            image_file = image_files[0] if image_files else None
            image_uri = f"{API}course/{category_name}/{lesson_name}/{image_file.name}" if image_file else None
            
            # 扫描步骤图片
            steps_dir = lesson_dir / "steps"
            steps = []
            if steps_dir.exists() and steps_dir.is_dir():
                step_files = sorted(list(steps_dir.glob("*.jpg")))
                for i, step_file in enumerate(step_files):
                    step_title = step_file.stem  # 去掉扩展名
                    step_image = f"{API}course/{category_name}/{lesson_name}/steps/{step_file.name}"
                    steps.append({
                        "title": step_title,
                        "image": step_image
                    })
            
            # 构建课程信息
            course_info = {
                "tags": tags,
                "name": lesson_name,
                "img": image_uri,
                "uri": sb3_uri,
                "steps": steps
            }
            
            course_data["data"][course_key] = course_info
    
    return course_data

def generate_course_json(course_data):
    """生成course.json文件"""
    with open('course.json', 'w', encoding='utf-8') as f:
        json.dump(course_data, f, ensure_ascii=False, indent=4)
    print("已生成 course.json 文件")

def generate_index_html(course_data):
    """生成index.html文件"""
    
    courses = course_data.get('data', {})
    
    # 按类别分组
    categories = {}
    for course_key, course_info in courses.items():
        tags = course_info.get('tags', [])
        if tags:
            category = tags[0]
            if category not in categories:
                categories[category] = {}
            categories[category][course_key] = course_info
    
    # 生成HTML内容
    html_content = generate_html_template(categories)
    
    # 写入index.html文件
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("已生成 index.html 文件")

def generate_html_template(categories):
    """生成HTML模板"""
    
    category_sections = []
    for category_name, courses in categories.items():
        section = generate_category_section(category_name, courses)
        category_sections.append(section)
    
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>课程目录 - Scratch编程课程</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Microsoft YaHei', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f5f5f5;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-align: center;
            padding: 40px 20px;
            margin-bottom: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }}
        
        header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        header p {{
            font-size: 1.2em;
            opacity: 0.9;
        }}
        
        .course-section {{
            background: white;
            margin-bottom: 30px;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        .section-title {{
            color: #667eea;
            font-size: 1.8em;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #667eea;
        }}
        
        .course-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}
        
        .course-card {{
            background: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 8px;
            padding: 20px;
            transition: all 0.3s ease;
            cursor: pointer;
        }}
        
        .course-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 5px 20px rgba(0,0,0,0.15);
            border-color: #667eea;
        }}
        
        .course-card h3 {{
            color: #495057;
            font-size: 1.3em;
            margin-bottom: 10px;
        }}
        
        .course-image {{
            width: 100%;
            height: 200px;
            object-fit: cover;
            border-radius: 6px;
            margin-bottom: 10px;
        }}
        
        .course-info {{
            font-size: 0.9em;
            color: #6c757d;
        }}
        
        .steps-count {{
            background: #667eea;
            color: white;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 0.8em;
            margin-left: 5px;
        }}
        
        .sb3-link {{
            display: inline-block;
            background: #28a745;
            color: white;
            padding: 8px 15px;
            text-decoration: none;
            border-radius: 5px;
            margin-top: 10px;
            font-size: 0.9em;
            transition: background 0.3s ease;
        }}
        
        .sb3-link:hover {{
            background: #218838;
        }}
        
        .no-link {{
            display: inline-block;
            background: #6c757d;
            color: white;
            padding: 8px 15px;
            text-decoration: none;
            border-radius: 5px;
            margin-top: 10px;
            font-size: 0.9em;
            cursor: not-allowed;
        }}
        
        .steps-button {{
            display: inline-block;
            background: #007bff;
            color: white;
            padding: 8px 15px;
            text-decoration: none;
            border-radius: 5px;
            margin-top: 10px;
            margin-left: 10px;
            font-size: 0.9em;
            transition: background 0.3s ease;
            cursor: pointer;
            border: none;
        }}
        
        .steps-button:hover {{
            background: #0056b3;
        }}
        
        .steps-button:disabled {{
            background: #6c757d;
            cursor: not-allowed;
        }}
        
        .modal {{
            display: none;
            position: fixed;
            z-index: 1000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0,0,0,0.8);
        }}
        
        .modal-content {{
            position: relative;
            margin: 5% auto;
            width: 80%;
            max-width: 800px;
            background: white;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
        }}
        
        .modal-image {{
            max-width: 100%;
            max-height: 70vh;
            border-radius: 8px;
            margin-bottom: 20px;
        }}
        
        .modal-title {{
            font-size: 1.2em;
            margin-bottom: 20px;
            color: #333;
        }}
        
        .modal-nav {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 20px;
        }}
        
        .nav-button {{
            background: #007bff;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 1em;
            transition: background 0.3s ease;
        }}
        
        .nav-button:hover {{
            background: #0056b3;
        }}
        
        .nav-button:disabled {{
            background: #6c757d;
            cursor: not-allowed;
        }}
        
        .close-button {{
            position: absolute;
            top: 10px;
            right: 15px;
            color: #aaa;
            font-size: 28px;
            font-weight: bold;
            cursor: pointer;
            background: none;
            border: none;
        }}
        
        .close-button:hover {{
            color: #000;
        }}
        
        .step-counter {{
            font-size: 1em;
            color: #666;
        }}
        
        footer {{
            text-align: center;
            margin-top: 40px;
            padding: 20px;
            color: #6c757d;
            border-top: 1px solid #e9ecef;
        }}
        
        @media (max-width: 768px) {{
            .course-grid {{
                grid-template-columns: 1fr;
            }}
            
            header h1 {{
                font-size: 2em;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Scratch编程课程目录</h1>
            <p>基于实际文件夹结构生成的课程目录</p>
        </header>
        
        {''.join(category_sections)}
        
        <footer>
            <p>&copy; 2025 Scratch编程课程. 所有课程资源仅供学习使用.</p>
        </footer>
    </div>
    
    <!-- 步骤弹窗 -->
    <div id="stepsModal" class="modal">
        <div class="modal-content">
            <button class="close-button" onclick="closeStepsModal()">&times;</button>
            <div id="modalTitle" class="modal-title"></div>
            <img id="modalImage" class="modal-image" src="" alt="步骤图片">
            <div class="modal-nav">
                <button id="prevButton" class="nav-button" onclick="prevStep()">上一张</button>
                <span id="stepCounter" class="step-counter">1 / 1</span>
                <button id="nextButton" class="nav-button" onclick="nextStep()">下一张</button>
            </div>
        </div>
    </div>
    
    <script>
        let currentSteps = [];
        let currentStepIndex = 0;
        
        function showStepsModal(stepsData) {{
            currentSteps = JSON.parse(stepsData);
            currentStepIndex = 0;
            updateModal();
            document.getElementById('stepsModal').style.display = 'block';
        }}
        
        // 为所有步骤按钮添加点击事件
        document.addEventListener('DOMContentLoaded', function() {{
            const stepsButtons = document.querySelectorAll('.steps-button');
            stepsButtons.forEach(button => {{
                button.addEventListener('click', function() {{
                    const stepsData = this.getAttribute('data-steps');
                    showStepsModal(stepsData);
                }});
            }});
        }});
        
        function closeStepsModal() {{
            document.getElementById('stepsModal').style.display = 'none';
            currentSteps = [];
            currentStepIndex = 0;
        }}
        
        function prevStep() {{
            if (currentStepIndex > 0) {{
                currentStepIndex--;
                updateModal();
            }}
        }}
        
        function nextStep() {{
            if (currentStepIndex < currentSteps.length - 1) {{
                currentStepIndex++;
                updateModal();
            }}
        }}
        
        function updateModal() {{
            if (currentSteps.length === 0) return;
            
            const step = currentSteps[currentStepIndex];
            document.getElementById('modalTitle').textContent = step.title;
            document.getElementById('modalImage').src = step.image;
            document.getElementById('stepCounter').textContent = `${{currentStepIndex + 1}} / ${{currentSteps.length}}`;
            
            // 更新按钮状态
            document.getElementById('prevButton').disabled = currentStepIndex === 0;
            document.getElementById('nextButton').disabled = currentStepIndex === currentSteps.length - 1;
        }}
        
        // 点击弹窗外部关闭
        window.onclick = function(event) {{
            const modal = document.getElementById('stepsModal');
            if (event.target === modal) {{
                closeStepsModal();
            }}
        }}
        
        // 键盘导航
        document.addEventListener('keydown', function(event) {{
            const modal = document.getElementById('stepsModal');
            if (modal.style.display === 'block') {{
                if (event.key === 'ArrowLeft') {{
                    prevStep();
                }} else if (event.key === 'ArrowRight') {{
                    nextStep();
                }} else if (event.key === 'Escape') {{
                    closeStepsModal();
                }}
            }}
        }});
    </script>
</body>
</html>"""
    
    return html

def generate_category_section(title, courses):
    """生成类别部分HTML"""
    
    if not courses:
        return f"""
        <section class="course-section">
            <h2 class="section-title">{title}</h2>
            <p>暂无课程数据</p>
        </section>
        """
    
    course_cards = []
    for course_key, course_info in sorted(courses.items(), key=lambda x: x[1].get('name', '')):
        name = course_info.get('name', '未知课程')
        img_url = course_info.get('img', '')
        sb3_url = course_info.get('uri', '')
        steps = course_info.get('steps', [])
        
        # 生成图片HTML
        if img_url:
            img_html = f'<img src="{img_url}" alt="{name}" class="course-image">'
        else:
            img_html = ''
        
        # 生成下载链接HTML
        if sb3_url:
            link_html = f'<a href="{sb3_url}" class="sb3-link" target="_blank">下载SB3文件</a>'
        else:
            link_html = '<span class="no-link">暂无文件</span>'
        
        # 生成步骤按钮HTML
        steps_button = ''
        if steps:
            steps_data = json.dumps(steps, ensure_ascii=False)
            steps_button = f'<button class="steps-button" data-steps=\'{steps_data}\'>查看步骤</button>'
        
        # 生成课程卡片
        card = f"""
        <div class="course-card">
            <h3>{name}</h3>
            {img_html}
            <div class="course-info">
                <p>步骤数量: <span class="steps-count">{len(steps)}</span></p>
                {link_html}
                {steps_button}
            </div>
        </div>
        """
        course_cards.append(card)
    
    return f"""
    <section class="course-section">
        <h2 class="section-title">{title}</h2>
        <div class="course-grid">
            {''.join(course_cards)}
        </div>
    </section>
    """

def main():
    """主函数"""
    print("开始扫描course文件夹...")
    
    # 扫描文件夹生成课程数据
    course_data = scan_course_directory()
    
    # 生成course.json文件
    generate_course_json(course_data)
    
    # 生成index.html文件
    generate_index_html(course_data)
    
    print("所有文件生成完成！")

if __name__ == "__main__":
    main()