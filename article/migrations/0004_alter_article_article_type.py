# Generated by Django 3.2.18 on 2023-04-12 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0003_alter_articletitle_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='article_type',
            field=models.CharField(choices=[('abstract', 'Abstract'), ('addendum', 'Addendum'), ('announcement', 'Announcement'), ('article-commentary', 'Article-Commentary'), ('book-review', 'Book-Review'), ('books-received', 'Books-Received'), ('brief-report', 'Brief-Report'), ('calendar', 'Calendar'), ('case-report', 'Case-Report'), ('clinical-trial', 'Clinical-Trial'), ('collection', 'Coleção'), ('correction', 'Correction'), ('data-article', 'Data-Article'), ('discussion', 'Discussion'), ('dissertation', 'Dissertation'), ('editorial', 'Editorial'), ('editorial-material', 'Editorial-Material'), ('guideline', 'Guideline'), ('in-brief', 'In-Brief'), ('interview', 'Interview'), ('introduction', 'Introduction'), ('letter', 'Letter'), ('meeting-report', 'Meeting-Report'), ('news', 'News'), ('obituary', 'Obituary'), ('oration', 'Oration'), ('other', 'Other'), ('partial-retraction', 'Partial-Retraction'), ('product-review', 'Product-Review'), ('rapid-communication', 'Rapid-Communication'), ('reply', 'Reply'), ('reprint', 'Reprint'), ('research-article', 'Research-Article'), ('retraction', 'Retraction'), ('review-article', 'Review-Article'), ('technical-report', 'Technical-Report'), ('translation', 'Translation')], max_length=32, verbose_name='Article type'),
        ),
    ]
