from django.utils import timezone

from django.http import HttpResponseRedirect, Http404
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.views import generic

from polls.models import Question

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_list'

    def get_queryset(self):
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, qid):
    p = get_object_or_404(Question, pk=qid)
    try:
        selected = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoestNotExist):
        return render(request, 'polls/detail.html', {
            'question': p,
            'error_message': "you didn't select a choice",})
    else:
        selected.votes += 1
        selected.save()
        return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))
