from django.http import HttpResponseRedirect
from django.utils.translation import gettext as _
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from wagtail.contrib.modeladmin.views import CreateView

from .models import OfficialJournal, NonOfficialJournalTitle, JournalMission


class OfficialJournalCreateView(CreateView):

    def form_valid(self, form):
        self.object = form.save_all(self.request.user)
        return HttpResponseRedirect(self.get_success_url())


class OfficialJournalAdmin(ModelAdmin):
    model = OfficialJournal
    inspect_view_enabled = True
    menu_label = _('Journals')
    create_view_class = OfficialJournalCreateView
    menu_icon = 'folder'
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False

    list_display = (
        'title',
        'foundation_year',
        'ISSN_print',
        'ISSN_electronic',
        'ISSNL',
    )
    list_filter = (
        'foundation_year',
    )
    search_fields = (
        'foundation_year',
        'ISSN_print',
        'ISSN_electronic',
        'ISSNL',
        'creator',
        'updated_by',
    )


class NonOfficialJournalTitleCreateView(CreateView):

    def form_valid(self, form):
        self.object = form.save_all(self.request.user)
        return HttpResponseRedirect(self.get_success_url())


class NonOfficialJournalTitleAdmin(ModelAdmin):
    model = NonOfficialJournalTitle
    inspect_view_enabled = True
    menu_label = _('Non Offical Journal Titles')
    create_view_class = NonOfficialJournalTitleCreateView
    menu_icon = 'folder'
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False

    list_display = (
        'official_journal_id',
        'non_official_journal_title',
    )
    list_filter = (
        'official_journal_id',
    )
    search_fields = (
        'official_journal_id',
        'non_official_journal_title',
    )


class JournalMissionAdmin(ModelAdmin):
    model = JournalMission
    menu_label = _('Journal Mission')
    menu_icon = 'folder'
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False

    list_display = (
        'official_journal_id',
        'official_journal'
    )
    list_filter = (
        'official_journal_id',
        'official_journal'
    )
    search_fields = (
        'official_journal_id',
        'official_journal'
    )


modeladmin_register(OfficialJournalAdmin)
modeladmin_register(NonOfficialJournalTitleAdmin)
modeladmin_register(JournalMissionAdmin)

