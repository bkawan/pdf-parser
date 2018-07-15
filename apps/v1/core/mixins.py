from django.http import JsonResponse


class AjaxableResponseMixin:
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    ajax_response_obj_properties = []  # to return extra data for ajax response but limit to object properties only

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super().form_valid(form)
        if self.request.is_ajax():
            data = {
                'message':"Successfully saved",
                # 'score':self.object.score
            }
            if self.ajax_response_obj_properties:
                for property in self.ajax_response_obj_properties:
                    data.update({property:self.object.__dict__.get(property)})
            return JsonResponse(data)
        else:
            return response
