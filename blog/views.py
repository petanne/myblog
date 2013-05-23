# Create your views here.
from django.shortcuts import render_to_response,render
from blog.models import Blog,Tag
from django.http import Http404,HttpResponse
import datetime
from django.template import Template,Context

from django.http import HttpResponseRedirect
#from django.template import RequestContext
from blog.models import Author
from blog.forms import BlogForm,TagForm
from django.core.urlresolvers import reverse


def blog_list(request):
    blogs = Blog.objects.all()
    return render_to_response("blog_list.html", {"blogs": blogs})

def blog_show(request,id=''):
    try:
        blog=Blog.objects.get(id=id)
    except Blog.DoesNotExist:
        raise Http404
    return render(request,"blog_show.html",{"blog":blog})

def blog_filter(request, id=''):
    tags = Tag.objects.all()
    tag = Tag.objects.get(id=id)
    blogs = tag.blog_set.all()
    return render_to_response("blog_filter.html",
                              {"blogs": blogs, "tag": tag, "tags": tags})


def blog_add(request):
    if request.method == 'POST':
        form = BlogForm(request.POST)
        tag = TagForm(request.POST)
        if form.is_valid() and tag.is_valid():
            cd = form.cleaned_data
            cdtag = tag.cleaned_data
            tagname = cdtag['tag_name']
            
            for taglist in tagname.split():
                Tag.objects.get_or_create(tag_name=taglist.strip())
                title = cd['caption']
                author = Author.objects.get(id=1)
                content = cd['content']
                blog = Blog(caption=title, author=author,content=content)
                blog.save()
                
            for taglist in tagname.split():
                blog.tags.add(Tag.objects.get(tag_name=taglist.strip()))
                blog.save()
                
            id = Blog.objects.order_by('-publish_time')[0].id
            #return HttpResponseRedirect('/blog/%s' % id)
            return HttpResponseRedirect(reverse("detailblog",args=(id,)))
            #return HttpResponseRedirect(reverse("detailblog",kwargs={"id":id}))
    else:
        form = BlogForm()
        tag = TagForm(initial={'tag_name': 'notags'})
    return render(request,'blog_add.html',locals())
        
def blog_update(request, id=""):
    id = id
    if request.method == 'POST':
        form = BlogForm(request.POST)
        tag = TagForm(request.POST)
        if form.is_valid() and tag.is_valid():
            cd = form.cleaned_data
            cdtag = tag.cleaned_data
            tagname = cdtag['tag_name']
            tagnamelist = tagname.split()
            
            for taglist in tagnamelist:
                Tag.objects.get_or_create(tag_name=taglist.strip())
            title = cd['caption']
            content = cd['content']
            blog = Blog.objects.get(id=id)
            if blog:
                blog.caption = title
                blog.content = content
                blog.save()
                for taglist in tagnamelist:
                    blog.tags.add(Tag.objects.get(tag_name=taglist.strip()))
                    blog.save()
                tags = blog.tags.all()
                for tagname in tags:
                    tagname = unicode(str(tagname), "utf-8")
                    if tagname not in tagnamelist:
                        notag = blog.tags.get(tag_name=tagname)
                        blog.tags.remove(notag)
            else:
                blog = Blog(caption=blog.caption,content=blog.content)
                blog.save()
            #return HttpResponseRedirect('/blog/%s' % id)
            return HttpResponseRedirect(reverse("detailblog",args=(id,)))
    else:
        try:
            blog = Blog.objects.get(id=id)
        except Exception:
            raise Http404
        form = BlogForm(initial={'caption': blog.caption,'content': blog.content}, auto_id=False)
        tags = blog.tags.all()
        if tags:
            taginit = ''
            for x in tags:
                taginit += str(x) + ' '
            tag = TagForm(initial={'tag_name': taginit})
        else:
            tag = TagForm()
    return render(request,'blog_add.html',
                              {'blog': blog, 'form': form, 'id': id, 'tag': tag},)

def blog_del(request, id=""):
    try:
        blog = Blog.objects.get(id=id)
    except Exception:
        raise Http404
    if blog:
        blog.delete()
        return HttpResponseRedirect(reverse("bloglist"))
    blogs = Blog.objects.all()
    return render_to_response("blog_list.html", {"blogs": blogs})

def blog_show_comment(request, id=''):
    blog = Blog.objects.get(id=id)
    return render_to_response('blog_comments_show.html', {"blog":blog})

def foobar(request,template):
    return render_to_response(template)

def current_time(request):
    now = datetime.datetime.now()
    t = Template('<html><body>It is now: {{ current_date }}</body></html>')
    html = t.render(Context({'current_date':now}))
    return HttpResponse(html)

def testform(request,template):
    form = BlogForm()
    return render(request,template,locals())
form = BlogForm()