from haystack import indexes
from .models import Post

#相对某个app下的数据进行全文检索，在该app下建立一个search_index.py 文件。
#创建一个 XXIndex 类，XX 为含有被检索的数据模型，并且继承SearchIndex,Indexable.
class PostIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Post

    def index_queryset(self, using=None):
        return self.get_model().objects.all()