import sqlite3
from datetime import datetime

def init_sample_data():
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    
    # 添加示例文章
    sample_posts = [
        ('第一篇博客文章', '这是我的第一篇博客文章内容。在这里，我们可以分享各种有趣的想法和经验。', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        ('技术分享', '这是一篇关于技术的分享文章。我们将讨论一些常见的编程问题和解决方案。', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        ('生活随笔', '记录生活中的点点滴滴，分享日常的所见所闻。', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    ]
    
    cursor.executemany('INSERT INTO posts (title, content, created) VALUES (?, ?, ?)', sample_posts)
    conn.commit()
    conn.close()
    print('示例数据已添加到数据库中')

if __name__ == '__main__':
    init_sample_data()