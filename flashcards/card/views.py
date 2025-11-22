from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import CreateView, UpdateView, ListView, DeleteView

from card.forms import BasicCardForm, IdentificationCardForm, ImageOcclusionCardForm
from card.models import BasicCard, IdentificationCard, ImageOcclusionCard


#
class ReviewDeckView(View):
#     def get(self, card):
#         return HttpResponse(f'Card: {card}')
#
#     def get_specific_card(self, card):
#         return HttpResponse(f'Card: {card}')
#
#
    pass
#

class CreateCardView(View):
    template_name = "create_cards.html"

    def get(self,request):
        context = {
            "basic_card_form": BasicCard(),
            "identification_card_form": IdentificationCard(),
            "image_occlusion_card_form": ImageOcclusionCard(),
        }
        return render(request, self.template_name, context)

    def post(self,request):
        form_type = request.POST.get('form_type')

        if form_type == "basic_card_form":
            form = BasicCardForm(request.POST)
            form.save()
        elif form_type == "identification_card_form":
            form = IdentificationCardForm(request.POST)
            form.save()
        elif form_type == "image_occlusion_card_form":
            form = ImageOcclusionCardForm(request.POST)
            form.save()
        else:
            return redirect("index.html")

        if form.is_valid():
            form.save()
            return redirect("index.html")

        return self.get(request)




class CardListView(LoginRequiredMixin, ListView):
    pass

class CardUpdateView(LoginRequiredMixin, UpdateView):
    pass

class CardDeleteView(LoginRequiredMixin, DeleteView):
    pass

class AddCardView(View):
    template_name = 'card/add-card.html'

    def get(self, request):
        return render(request, self.template_name)
class ViewBack(View):
    template_name = 'card/study_back.html'

    def get(self, request):
        return render(request, self.template_name)
class ViewFront(View):
    template_name = 'card/study_front.html'

    def get(self, request):
        return render(request, self.template_name)
