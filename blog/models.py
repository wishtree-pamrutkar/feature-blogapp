from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.timezone import now

class Category(models.Model):
    category = models.CharField(max_length=30)

    @staticmethod
    def get_all_categories():
        Category.objects.all()


    def __str__(self):
        return self.category

class Post(models.Model):
    sno = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    slug = models.CharField(max_length=130)
    timeStamp = models.DateTimeField(blank=True,auto_now=True)
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User,related_name='blog_posts',blank=True)

    def get_absolute_url(self):
        return reverse('blogPost',args=(str(self.id)))


    def total_likes(self):
        return self.likes.count()

    @staticmethod
    def get_all_post():
        return Post.objects.all()

    @staticmethod
    def get_all_post_by_categoryid(category_id):
        if category_id:
            return Post.objects.filter(category = category_id)
        else:
            return Post.get_all_post();

    def num_likes(self):
        return self.likes.all().count()



    def __str__(self):
        return self.title + " by " + str(self.author)

LIKE_CHOICES = (

    ('Like', 'Like'),
    ('Unlike','Unlike')
)

class BlogComment(models.Model):
    sno = models.AutoField(primary_key=True)
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return self.comment[0:13] + "..." + "by" + " " + self.user.username


# class author(models.Model):
#     user = models.ForeignKey(User,on_delete=models.CASCADE)

#     post = models.ForeignKey(Post, on_delete=models.CASCADE)
#     value = models.CharField(choices=LIKE_CHOICES,max_length=10)
#
#     def __str__(self):
#         return str(self.post)



0