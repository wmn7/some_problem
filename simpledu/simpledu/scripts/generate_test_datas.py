import os
import json
from random import randint
from faker import Faker
from simpledu.models import db,User,Course,Chapter

#创建faker工厂对象
fake = Faker()

#生成一个教师用户
def iter_users():
    yield User(
        username = 'Jack Lee',
        email = 'jacklee@163.com',
        password = '123456',
        job = '研发工程师'
    )

#从datas读取实验楼课程数据,生产测试课程数据,讲课程教师
#设置为生成课程的用户
def iter_courses():
    author = User.query.filter_by(username='Jack Lee').first()

    #打印一下路径
    print(os.path.join(os.path.dirname(__file__),'data','courses.json'))

    with open(os.path.join(os.path.dirname(__file__),'data','courses.json')) as f:
        courses = json.load(f)
    for course in courses:
        yield Course(
            name = course['name'],
            description=course['description'],
            image_url = course['image_url'],
            author=author
        )

def iter_chapters():
    for course in Course.query:
        #每个课程生成3-10个章节
        for i in range(randint(3,10)):
            yield Chapter(
                #使用faker生产一个句子作为章节名称
                name = fake.sentence(),
                course=course,
                # 所以章节的视频设置成了楼＋课程中的某个视频
                vedio_url='https://labfile.oss.aliyuncs.com/courses/923/week2_mp4/2-1-1-mac.mp4',
                #视频时长
                vedio_duration='{}:{}'.format(randint(10, 30), randint(10, 59))

            )


def run():
    for user in iter_users():
        db.session.add(user)

    for course in iter_courses():
        db.session.add(course)
    
    for chapter in iter_chapters():
        db.session.add(chapter)

    try:
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()

