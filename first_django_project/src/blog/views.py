from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from .models import BlogPost
from .forms import BlogPostModelForm
from django.contrib.admin.views.decorators import staff_member_required 


# def  blog_post_detail_view(request, slug):
# 	# try:
# 	# 	obj = BlogPost.objects.get(id=post_id)
# 	# except:
# 	# 	raise Http404

# 	obj = get_object_or_404(BlogPost, slug=slug)
# 	# queryset = BlogPost.objects.filter(slug=slug)
# 	# if queryset.count() == 0:
# 	# 	raise Http404
# 	# obj = queryset.first()
# 	template_name = 'blog_post_detail.html'
# 	context = {"object" : obj}
# 	return render(request, template_name, context)

@staff_member_required
def blog_post_create_view(request):
	form = BlogPostModelForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		obj = form.save(commit = False)
		obj.user = request.user
		obj.save()
		form = BlogPostModelForm()
	template_name = 'forms.html'
	context = {'form' : form}
	return render(request, template_name, context)

def blog_post_list_view(request):
	qs = BlogPost.objects.all()
	template_name = 'list_view.html'
	context = {'object_list': qs}
	return render(request, template_name, context)

def blog_post_detail_view(request, slug):
	obj = get_object_or_404(BlogPost, slug=slug)
	template_name = 'detail.html'
	context = {"object" : obj}
	return render(request, template_name, context)

@staff_member_required
def blog_post_update_view(request, slug):
	print(request.FILES)
	obj = get_object_or_404(BlogPost, slug=slug)
	form = BlogPostModelForm(request.POST or None, request.FILES or None, instance = obj)
	if form.is_valid():
		form.save()
	template_name = 'forms.html'
	context = {"form": form, "title" : f"Update {obj.title}"}
	return render(request, template_name, context)

@staff_member_required
def blog_post_delete_view(request, slug):
	obj = get_object_or_404(BlogPost, slug=slug)
	template_name = 'delete.html'
	if request.method == "POST":
		obj.delete()
		return redirect("/blog")
	context = {"object" : obj}
	return render(request, template_name, context)