from django.shortcuts import render, get_object_or_404
from apps.stories.models import Story,StoryTag
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_not_required
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.template.loader import render_to_string

def story_list(request, tag_slug=None):
    ''' display list stories with published '''
    stories = Story.objects.filter(status='published',).select_related('author')

    query = request.GET.get('q')
    if query:
        stories = stories.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(author__first_name__icontains=query) |
            Q(author__last_name__icontains=query) |
            Q(author__username__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()

    tag = None
    if tag_slug: 
        tag = get_object_or_404(StoryTag, slug=tag_slug) 
        stories = stories.filter(tags=tag)

    stories = stories.distinct()   

    '''pagination'''
    paginator = Paginator(stories, 12)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    # If AJAX: render only the partial with story cards (no header/footer/breadcrumb)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string(
            'stories/partials/story_cards.html',
            {'page_obj': page_obj, 'tag': tag},
            request=request
        )
        # build next_page_url (preserve filters)
        next_page_url = None
        if page_obj.has_next():
            params = request.GET.copy()
            params['page'] = page_obj.next_page_number()
            next_page_url = f"{request.path}?{params.urlencode()}"

        return JsonResponse({
            'html': html,
            'has_next': page_obj.has_next(),
            'next_page': page_obj.next_page_number() if page_obj.has_next() else None,
            'next_page_url': next_page_url,
        })

    # Normal full page render (header/footer/breadcrumb present)
    next_page_url = None
    if page_obj.has_next():
        params = request.GET.copy()
        params['page'] = page_obj.next_page_number()
        next_page_url = f"{request.path}?{params.urlencode()}"

    
    context = {
        'page_obj': page_obj,
        'stories': stories,
        'tag': tag,
        'query': query,
        'results_count': stories.count(),
         'next_page_url': next_page_url,
        'ajax': False,
    }


    return render(request, 'stories/stories_list.html', context=context)




















def index_view(request):
    """View for the home/index page"""
    return render(request, 'index.html')


def author_view(request):
    """View for the author page"""
    return render(request, 'author.html')


def blog_details_view(request):
    """View for the blog details page"""
    return render(request, 'blog-details.html')

def coming_soon_view(request):
    """View for the coming soon page"""
    return render(request, 'coming-soon.html')


def error_view(request):
    """View for the error page"""
    return render(request, 'error.html')
