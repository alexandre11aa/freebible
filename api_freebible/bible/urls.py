from bible.views.bible import BibliaViewSet
from bible.views.book import LivroViewSet 
#from bible.views.chapter import CapituloViewSet
#from bible.views.versicle import VersiculoViewSet

from rest_framework.routers import DefaultRouter

router_bible_version = DefaultRouter()
router_book = DefaultRouter()
#router_chapter = DefaultRouter()
#router_versicle = DefaultRouter()

# Registrando o CustomUserViewSet no roteador
router_bible_version.register('bible_version', BibliaViewSet)
router_book.register('book', LivroViewSet)
#router_chapter.register('chapter', CapituloViewSet)
#router_versicle.register('versicle', VersiculoViewSet)

urlpatterns = router_bible_version.urls
urlpatterns = router_book.urls
#urlpatterns = router_chapter.urls
#urlpatterns = router_versicle.urls