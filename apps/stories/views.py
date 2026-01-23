from django.shortcuts import render


def index_view(request):
    """View for the home/index page"""
    return render(request, 'index.html')


def author_view(request):
    """View for the author page"""
    return render(request, 'author.html')


def blog_details_view(request):
    """View for the blog details page"""
    return render(request, 'blog-details.html')


def column_layout_view(request):
    """View for the column layout grid page"""
    return render(request, 'column-layout-grid.html')


def coming_soon_view(request):
    """View for the coming soon page"""
    return render(request, 'coming-soon.html')


def error_view(request):
    """View for the error page"""
    return render(request, 'error.html')
