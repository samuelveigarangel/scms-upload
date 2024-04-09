import sys

from packtools.sps.validation.aff import AffiliationsListValidation
from packtools.sps.validation.article_and_subarticles import (
    ArticleLangValidation,
    ArticleAttribsValidation,
    ArticleIdValidation,
    ArticleSubjectsValidation,
    ArticleTypeValidation,
)
from packtools.sps.validation.article_authors import ArticleAuthorsValidation

from packtools.sps.validation.article_data_availability import (
    DataAvailabilityValidation,
)
from packtools.sps.validation.article_doi import ArticleDoiValidation
from packtools.sps.validation.article_lang import ArticleLangValidation
from packtools.sps.validation.article_license import ArticleLicenseValidation
from packtools.sps.validation.article_toc_sections import ArticleTocSectionsValidation
from packtools.sps.validation.article_xref import ArticleXrefValidation
from packtools.sps.validation.dates import ArticleDatesValidation
from packtools.sps.validation.journal_meta import JournalMetaValidation
from packtools.sps.validation.preprint import PreprintValidation
from packtools.sps.validation.related_articles import RelatedArticlesValidation

from core.utils.requester import fetch_data
from upload import choices
from upload.models import ValidationResult
from tracker.models import UnexpectedEvent


def doi_callable_get_data(doi):
    return {}


def orcid_callable_get_validate(orcid):
    return {}


def add_app_data(data, app_data):
    # TODO
    data["country_codes"] = []


def add_journal_data(data, journal, issue):
    # TODO
    # específico do periódico
    data["language_codes"] = []

    if issue:
        data["subjects"] = issue.subjects_list
        data["expected_toc_sections"] = issue.toc_sections
    else:
        data["subjects"] = journal.subjects_list
        data["expected_toc_sections"] = journal.toc_sections

    # {
    #     'issns': {
    #                 'ppub': '0103-5053',
    #                 'epub': '1678-4790'
    #             },
    #     'acronym': 'hcsm',
    #     'journal-title': 'História, Ciências, Saúde-Manguinhos',
    #     'abbrev-journal-title': 'Hist. cienc. saude-Manguinhos',
    #     'publisher-name': ['Casa de Oswaldo Cruz, Fundação Oswaldo Cruz'],
    #     'nlm-ta': 'Rev Saude Publica'
    #     }
    data["journal"] = journal.data
    data["expected_license_code"] = journal.license_code


def add_sps_data(data, version, sps_data):
    """
    results: [
        {
            "key": "value",
            "value": {"key": "value"}
        }
    ]
    """
    # TODO
    # depende do SPS / JATS / Critérios
    url = "https://core.scielo.org/api/v1/xml_validation/"
    content = fetch_data(url, params={'version': version}, json=True, timeout=1)
    results = content.get("results")
    for c in results:
        data[c.get("key")] = c.get("value")


def validate_xml_content(sps_pkg_name, xmltree, data):
    # TODO adicionar error_category
    # VE_XML_CONTENT_ERROR: generic usage
    # VE_BIBLIOMETRICS_DATA_ERROR: used in metrics
    # VE_SERVICES_DATA_ERROR: used in reports
    # VE_DATA_CONSISTENCY_ERROR: data consistency
    # VE_CRITERIA_ISSUES_ERROR: required by the criteria document

    error_category_and_function_items = (
        (choices.VE_BIBLIOMETRICS_DATA_ERROR, validate_affiliations),
        (choices.VE_BIBLIOMETRICS_DATA_ERROR, validate_authors),
        (choices.VE_BIBLIOMETRICS_DATA_ERROR, validate_languages),
        (choices.VE_CRITERIA_ISSUES_ERROR, validate_article_attributes),
        (choices.VE_CRITERIA_ISSUES_ERROR, validate_data_availability),
        (choices.VE_CRITERIA_ISSUES_ERROR, validate_licenses),
        (choices.VE_DATA_CONSISTENCY_ERROR, validate_article_id_other),
        (choices.VE_DATA_CONSISTENCY_ERROR, validate_article_languages),
        (choices.VE_DATA_CONSISTENCY_ERROR, validate_article_type),
        (choices.VE_DATA_CONSISTENCY_ERROR, validate_dates),
        (choices.VE_DATA_CONSISTENCY_ERROR, validate_doi),
        (choices.VE_DATA_CONSISTENCY_ERROR, validate_journal),
        (choices.VE_DATA_CONSISTENCY_ERROR, validate_preprint),
        (choices.VE_DATA_CONSISTENCY_ERROR, validate_related_articles),
        (choices.VE_DATA_CONSISTENCY_ERROR, validate_subjects),
        (choices.VE_DATA_CONSISTENCY_ERROR, validate_toc_sections),
        (choices.VE_DATA_CONSISTENCY_ERROR, validate_xref),
    )
    for error_category, f in error_category_and_function_items:
        for item in f(sps_pkg_name, xmltree, data):
            if item["validation_type"] in ("value in list", "value", "match"):
                error_category = choices.VE_DATA_CONSISTENCY_ERROR
            item["error_category"] = item.get("error_category") or error_category
            yield item


def validate_affiliations(sps_pkg_name, xmltree, data):
    xml = AffiliationsListValidation(xmltree)

    try:
        yield from xml.validade_affiliations_list(data["country_codes"])
    except Exception as exc:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        UnexpectedEvent.create(
            exception=exc,
            exc_traceback=exc_traceback,
            detail={
                "function": "upload.xml_validation.validate_affiliations",
                "sps_pkg_name": sps_pkg_name,
            },
        )


def validate_languages(sps_pkg_name, xmltree, data):
    xml = ArticleLangValidation(xmltree)

    try:
        yield from xml.validate_language(data["language_codes"])
    except Exception as exc:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        UnexpectedEvent.create(
            exception=exc,
            exc_traceback=exc_traceback,
            detail={
                "function": "upload.xml_validation.validate_languages",
                "sps_pkg_name": sps_pkg_name,
            },
        )


def validate_article_attributes(sps_pkg_name, xmltree, data):
    xml = ArticleAttribsValidation(xmltree)

    try:
        yield from xml.validate_dtd_version(data["dtd_versions"])
    except Exception as exc:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        UnexpectedEvent.create(
            exception=exc,
            exc_traceback=exc_traceback,
            detail={
                "function": "upload.xml_validation.validate_dtd_version",
                "sps_pkg_name": sps_pkg_name,
            },
        )

    try:
        yield from xml.validate_specific_use(data["sps_versions"])
    except Exception as exc:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        UnexpectedEvent.create(
            exception=exc,
            exc_traceback=exc_traceback,
            detail={
                "function": "upload.xml_validation.validate_specific_use",
                "sps_pkg_name": sps_pkg_name,
            },
        )


def validate_article_id_other(sps_pkg_name, xmltree, data):
    xml = ArticleIdValidation(xmltree)

    try:
        yield from xml.validate_article_id_other()
    except Exception as exc:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        UnexpectedEvent.create(
            exception=exc,
            exc_traceback=exc_traceback,
            detail={
                "function": "upload.xml_validation.validate_article_id_other",
                "sps_pkg_name": sps_pkg_name,
            },
        )


def validate_subjects(sps_pkg_name, xmltree, data):
    xml = ArticleSubjectsValidation(xmltree)

    try:
        yield from xml.validate_without_subjects()
    except Exception as exc:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        UnexpectedEvent.create(
            exception=exc,
            exc_traceback=exc_traceback,
            detail={
                "function": "upload.xml_validation.validate_without_subjects",
                "sps_pkg_name": sps_pkg_name,
            },
        )


def validate_article_type(sps_pkg_name, xmltree, data):
    xml = ArticleTypeValidation(xmltree)

    try:
        yield from xml.validate_article_type(data["article_types"])
    except Exception as exc:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        UnexpectedEvent.create(
            exception=exc,
            exc_traceback=exc_traceback,
            detail={
                "function": "upload.xml_validation.validate_article_type",
                "sps_pkg_name": sps_pkg_name,
            },
        )
    try:
        yield from xml.validate_article_type_vs_subject_similarity(
            data["subjects"], data["expected_article_type_vs_subject_similarity"]
        )
    except Exception as exc:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        UnexpectedEvent.create(
            exception=exc,
            exc_traceback=exc_traceback,
            detail={
                "function": "upload.xml_validation.validate_article_type_vs_subject_similarity",
                "sps_pkg_name": sps_pkg_name,
            },
        )


def validate_authors(sps_pkg_name, xmltree, data):
    xml = ArticleAuthorsValidation(xmltree)

    try:
        yield from xml.validate_authors_orcid_format()
    except Exception as exc:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        UnexpectedEvent.create(
            exception=exc,
            exc_traceback=exc_traceback,
            detail={
                "function": "upload.xml_validation.validate_authors_orcid_format",
                "sps_pkg_name": sps_pkg_name,
            },
        )
    try:
        yield from xml.validate_authors_orcid_is_registered(
            data["callable_get_orcid_data"]
        )
    except Exception as exc:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        UnexpectedEvent.create(
            exception=exc,
            exc_traceback=exc_traceback,
            detail={
                "function": "upload.xml_validation.validate_authors_orcid_is_registered",
                "sps_pkg_name": sps_pkg_name,
            },
        )
    try:
        yield from xml.validate_authors_orcid_is_unique()
    except Exception as exc:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        UnexpectedEvent.create(
            exception=exc,
            exc_traceback=exc_traceback,
            detail={
                "function": "upload.xml_validation.validate_authors_orcid_is_unique",
                "sps_pkg_name": sps_pkg_name,
            },
        )
    try:
        yield from xml.validate_authors_role(data["credit_taxonomy"])
    except Exception as exc:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        UnexpectedEvent.create(
            exception=exc,
            exc_traceback=exc_traceback,
            detail={
                "function": "upload.xml_validation.validate_authors_role",
                "sps_pkg_name": sps_pkg_name,
            },
        )


def validate_data_availability(sps_pkg_name, xmltree, data):
    xml = DataAvailabilityValidation(xmltree)

    try:
        yield from xml.validate_data_availability(
            data["data_availability_specific_uses"]
        )
    except Exception as exc:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        UnexpectedEvent.create(
            exception=exc,
            exc_traceback=exc_traceback,
            detail={
                "function": "upload.xml_validation.validate_data_availability",
                "sps_pkg_name": sps_pkg_name,
            },
        )


def validate_doi(sps_pkg_name, xmltree, data):
    xml = ArticleDoiValidation(xmltree)

    try:
        yield from xml.validate_all_dois_are_unique()
    except Exception as exc:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        UnexpectedEvent.create(
            exception=exc,
            exc_traceback=exc_traceback,
            detail={
                "function": "upload.xml_validation.validate_all_dois_are_unique",
                "sps_pkg_name": sps_pkg_name,
            },
        )
    try:
        yield from xml.validate_doi_registered(data["callable_get_doi_data"])
    except Exception as exc:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        UnexpectedEvent.create(
            exception=exc,
            exc_traceback=exc_traceback,
            detail={
                "function": "upload.xml_validation.validate_doi_registered",
                "sps_pkg_name": sps_pkg_name,
            },
        )
    try:
        yield from xml.validate_main_article_doi_exists()
    except Exception as exc:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        UnexpectedEvent.create(
            exception=exc,
            exc_traceback=exc_traceback,
            detail={
                "function": "upload.xml_validation.validate_main_article_doi_exists",
                "sps_pkg_name": sps_pkg_name,
            },
        )
    try:
        yield from xml.validate_translations_doi_exists()
    except Exception as exc:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        UnexpectedEvent.create(
            exception=exc,
            exc_traceback=exc_traceback,
            detail={
                "function": "upload.xml_validation.validate_translations_doi_exists",
                "sps_pkg_name": sps_pkg_name,
            },
        )


def validate_article_languages(sps_pkg_name, xmltree, data):
    xml = ArticleLangValidation(xmltree)

    try:
        yield from xml.validate_article_lang()
    except Exception as exc:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        UnexpectedEvent.create(
            exception=exc,
            exc_traceback=exc_traceback,
            detail={
                "function": "upload.xml_validation.validate_article_lang",
                "sps_pkg_name": sps_pkg_name,
            },
        )


def validate_licenses(sps_pkg_name, xmltree, data):
    xml = ArticleLicenseValidation(xmltree)
    # yield from xml.validate_license(license_expected_value)

    try:
        yield from xml.validate_license_code(data["expected_license_code"])
    except Exception as exc:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        UnexpectedEvent.create(
            exception=exc,
            exc_traceback=exc_traceback,
            detail={
                "function": "upload.xml_validation.validate_license_code",
                "sps_pkg_name": sps_pkg_name,
            },
        )


def validate_toc_sections(sps_pkg_name, xmltree, data):
    xml = ArticleTocSectionsValidation(xmltree)

    try:
        yield from xml.validade_article_title_is_different_from_section_titles()
    except Exception as exc:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        UnexpectedEvent.create(
            exception=exc,
            exc_traceback=exc_traceback,
            detail={
                "function": "upload.xml_validation.validade_article_title_is_different_from_section_titles",
                "sps_pkg_name": sps_pkg_name,
            },
        )
    try:
        yield from xml.validate_article_toc_sections(data["expected_toc_sections"])
    except Exception as exc:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        UnexpectedEvent.create(
            exception=exc,
            exc_traceback=exc_traceback,
            detail={
                "function": "upload.xml_validation.validate_article_toc_sections",
                "sps_pkg_name": sps_pkg_name,
            },
        )


def validate_xref(sps_pkg_name, xmltree, data):
    xml = ArticleXrefValidation(xmltree)

    try:
        yield from xml.validate_id()
    except Exception as exc:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        UnexpectedEvent.create(
            exception=exc,
            exc_traceback=exc_traceback,
            detail={
                "function": "upload.xml_validation.validate_id",
                "sps_pkg_name": sps_pkg_name,
            },
        )
    try:
        yield from xml.validate_rid()
    except Exception as exc:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        UnexpectedEvent.create(
            exception=exc,
            exc_traceback=exc_traceback,
            detail={
                "function": "upload.xml_validation.validate_rid",
                "sps_pkg_name": sps_pkg_name,
            },
        )


def validate_dates(sps_pkg_name, xmltree, data):
    xml = ArticleDatesValidation(xmltree)

    try:
        yield from xml.validate_article_date(data["future_date"])
    except Exception as exc:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        UnexpectedEvent.create(
            exception=exc,
            exc_traceback=exc_traceback,
            detail={
                "function": "upload.xml_validation.validate_article_date",
                "sps_pkg_name": sps_pkg_name,
            },
        )
    try:
        yield from xml.validate_collection_date(data["future_date"])
    except Exception as exc:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        UnexpectedEvent.create(
            exception=exc,
            exc_traceback=exc_traceback,
            detail={
                "function": "upload.xml_validation.validate_collection_date",
                "sps_pkg_name": sps_pkg_name,
            },
        )
    try:
        yield from xml.validate_history_dates(
            data["events_order"], data["required_events"]
        )
    except Exception as exc:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        UnexpectedEvent.create(
            exception=exc,
            exc_traceback=exc_traceback,
            detail={
                "function": "upload.xml_validation.validate_history_dates",
                "sps_pkg_name": sps_pkg_name,
            },
        )
    try:
        yield from xml.validate_number_of_digits_in_article_date()
    except Exception as exc:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        UnexpectedEvent.create(
            exception=exc,
            exc_traceback=exc_traceback,
            detail={
                "function": "upload.xml_validation.validate_number_of_digits_in_article_date",
                "sps_pkg_name": sps_pkg_name,
            },
        )


def validate_journal(sps_pkg_name, xmltree, data):
    xml = JournalMetaValidation(xmltree)

    try:
        yield from xml.validate(data["journal"])
    except Exception as exc:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        UnexpectedEvent.create(
            exception=exc,
            exc_traceback=exc_traceback,
            detail={
                "function": "upload.xml_validation.validate_journal",
                "sps_pkg_name": sps_pkg_name,
            },
        )


def validate_preprint(sps_pkg_name, xmltree, data):
    xml = PreprintValidation(xmltree)

    try:
        yield from xml.preprint_validation()
    except Exception as exc:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        UnexpectedEvent.create(
            exception=exc,
            exc_traceback=exc_traceback,
            detail={
                "function": "upload.xml_validation.preprint_validation",
                "sps_pkg_name": sps_pkg_name,
            },
        )


def validate_related_articles(sps_pkg_name, xmltree, data):
    xml = RelatedArticlesValidation(xmltree)

    try:
        yield from xml.related_articles_doi()
    except Exception as exc:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        UnexpectedEvent.create(
            exception=exc,
            exc_traceback=exc_traceback,
            detail={
                "function": "upload.xml_validation.validate_related_articles",
                "sps_pkg_name": sps_pkg_name,
            },
        )
    try:
        yield from xml.related_articles_matches_article_type_validation(
            data["article_type_correspondences"]
        )
    except Exception as exc:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        UnexpectedEvent.create(
            exception=exc,
            exc_traceback=exc_traceback,
            detail={
                "function": "upload.xml_validation.related_articles_matches_article_type_validation",
                "sps_pkg_name": sps_pkg_name,
            },
        )
