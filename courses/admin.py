from django.contrib import admin
from .models import Subject, Course, Module
from django import forms
from django.urls import path
import csv
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Register your models here.
class ExportCsvMixin:
    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"

class CsvImportForm(forms.Form):
    csv_file = forms.FileField()

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin, ExportCsvMixin):
	list_display = ['title', 'slug']
	prepopulated_fields = {'slug': ('title',)}
	change_list_template = "entities/subjects_changelist.html"
	def get_urls(self):
		urls = super().get_urls()
		my_urls = [
            path('import-csv/', self.import_csv),
        ]
		return my_urls + urls

	def import_csv(self, request):
		if request.method == "POST":
			csv_file = request.FILES["csv_file"]
			readers= csv.reader(csv_file)
            # Create Hero objects from passed in data
            # ...
			print(readers)
			self.message_user(request, "Your csv file has been imported")
			return redirect("..")
		form = CsvImportForm()
		payload = {"form": form}
		return render(
            request, "admin/csv_form.html", payload
        )

class ModuleInline(admin.StackedInline):
	model = Module

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
	list_display = ['title', 'subject', 'created']
	list_filter = ['created', 'subject']
	search_fields = ['title', 'overview']
	prepopulated_fields = {'slug': ('title',)}
	inlines = [ModuleInline]