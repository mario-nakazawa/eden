# -*- coding: utf-8 -*-

from collections import OrderedDict

from gluon import current
from gluon.storage import Storage

def config(settings):
    """
        Template for WA-COP + CAD Cloud Integration
    """

    T = current.T

    # =========================================================================
    # System Settings
    #
    settings.base.system_name = T("Sahana: Washington Common Operating Picture (WA-COP)")
    settings.base.system_name_short = T("Sahana")

    # Prepop default
    settings.base.prepopulate += ("WACOP", "default/users", "WACOP/Demo")

    # Theme (folder to use for views/layout.html)
    settings.base.theme = "WACOP"

    # -------------------------------------------------------------------------
    # Self-Registration and User Profile
    #
    # Users can self-register
    settings.security.self_registration = False
    # Users need to verify their email
    settings.auth.registration_requires_verification = True
    # Users need to be approved
    settings.auth.registration_requires_approval = True
    settings.auth.registration_requests_organisation = True
    settings.auth.registration_organisation_required = True

    # Approval emails get sent to all admins
    settings.mail.approver = "ADMIN"

    settings.auth.registration_link_user_to = {"staff": T("Staff")}
    settings.auth.registration_link_user_to_default = ["staff"]
    settings.auth.registration_roles = {"organisation_id": ["USER"],
                                        }

    settings.auth.show_utc_offset = False
    settings.auth.show_link = False

    # -------------------------------------------------------------------------
    # Security Policy
    #
    settings.security.policy = 7 # Apply Controller, Function and Table ACLs
    settings.security.map = True

    # -------------------------------------------------------------------------
    # L10n (Localization) settings
    #
    settings.L10n.languages = OrderedDict([
        ("en", "English"),
        ("es", "Español"),
    ])
    # Default Language
    settings.L10n.default_language = "en"
    # Default timezone for users
    settings.L10n.utc_offset = "-0800"
    # Unsortable 'pretty' date format
    settings.L10n.date_format = "%b %d %Y"
    # Number formats (defaults to ISO 31-0)
    # Decimal separator for numbers (defaults to ,)
    settings.L10n.decimal_separator = "."
    # Thousands separator for numbers (defaults to space)
    settings.L10n.thousands_separator = ","
    # Default Country Code for telephone numbers
    settings.L10n.default_country_code = 1
    # Enable this to change the label for 'Mobile Phone'
    settings.ui.label_mobile_phone = "Cell Phone"
    # Enable this to change the label for 'Postcode'
    settings.ui.label_postcode = "ZIP Code"

    settings.msg.require_international_phone_numbers = False
    # PDF to Letter
    settings.base.paper_size = T("Letter")

    # Uncomment this to Translate CMS Series Names
    # - we want this on when running s3translate but off in normal usage as we use the English names to lookup icons in render_posts
    #settings.L10n.translate_cms_series = True
    # Uncomment this to Translate Location Names
    #settings.L10n.translate_gis_location = True

    # -------------------------------------------------------------------------
    # GIS settings
    #
    # Restrict the Location Selector to just certain countries
    settings.gis.countries = ("US",)
    # Levels for the LocationSelector
    levels = ("L1", "L2", "L3")

    # Uncomment to pass Addresses imported from CSV to a Geocoder to try and automate Lat/Lon
    #settings.gis.geocode_imported_addresses = "google"

    # Until we add support to S3LocationSelector to set dropdowns from LatLons
    settings.gis.check_within_parent_boundaries = False
    # GeoNames username
    settings.gis.geonames_username = "mcop"
    # Uncomment to hide Layer Properties tool
    #settings.gis.layer_properties = False
    # Uncomment to display the Map Legend as a floating DIV
    settings.gis.legend = "float"
    # Uncomment to prevent showing LatLon in Location Represents
    settings.gis.location_represent_address_only = "icon"
    # Resources which can be directly added to the main map
    settings.gis.poi_create_resources = None

    # -------------------------------------------------------------------------
    # Event/Incident Management
    #
    settings.event.incident_teams_tab = "Units"

    def customise_event_incident_controller(**attr):

        # Custom rheader tabs
        attr = dict(attr)
        attr["rheader"] = wacop_event_rheader

        return attr

    settings.customise_event_incident_controller = customise_event_incident_controller

    # -------------------------------------------------------------------------
    # Modules
    #
    settings.modules = OrderedDict([
        # Core modules which shouldn't be disabled
        ("default", Storage(
            name_nice = "Home",
            restricted = False, # Use ACLs to control access to this module
            access = None,      # All Users (inc Anonymous) can see this module in the default menu & access the controller
            module_type = None  # This item is not shown in the menu
        )),
        ("admin", Storage(
            name_nice = "Administration",
            #description = "Site Administration",
            restricted = True,
            access = "|1|",     # Only Administrators can see this module in the default menu & access the controller
            module_type = None  # This item is handled separately for the menu
        )),
        ("appadmin", Storage(
            name_nice = "Administration",
            #description = "Site Administration",
            restricted = True,
            module_type = None  # No Menu
        )),
    #    ("errors", Storage(
    #        name_nice = "Ticket Viewer",
    #        #description = "Needed for Breadcrumbs",
    #        restricted = False,
    #        module_type = None  # No Menu
    #    )),
       ("sync", Storage(
           name_nice = "Synchronization",
           #description = "Synchronization",
           restricted = True,
           access = "|1|",     # Only Administrators can see this module in the default menu & access the controller
           module_type = None  # This item is handled separately for the menu
       )),
        ("translate", Storage(
            name_nice = "Translation Functionality",
            #description = "Selective translation of strings based on module.",
            module_type = None,
        )),
        ("gis", Storage(
            name_nice = "Map",
            #description = "Situation Awareness & Geospatial Analysis",
            restricted = True,
            module_type = 1,     # 1st item in the menu
        )),
        ("pr", Storage(
            name_nice = "Persons",
            description = "Central point to record details on People",
            restricted = True,
            access = "|1|",     # Only Administrators can see this module in the default menu (access to controller is possible to all still)
            module_type = None
        )),
        ("org", Storage(
            name_nice = "Organizations",
            #description = 'Lists "who is doing what & where". Allows relief agencies to coordinate their activities',
            restricted = True,
            module_type = 10
        )),
        # All modules below here should be possible to disable safely
        ("hrm", Storage(
            name_nice = "Contacts",
            #description = "Human Resources Management",
            restricted = True,
            module_type = None,
        )),
        ("cms", Storage(
                name_nice = "Content Management",
                restricted = True,
                module_type = 10,
            )),
        ("event", Storage(
                name_nice = "Events",
                restricted = True,
                module_type = 2,
            )),
        ("fire", Storage(
                name_nice = "Fire",
                restricted = True,
                module_type = None,
            )),
        ("police", Storage(
                name_nice = "Police",
                restricted = True,
                module_type = None,
            )),
        ("project", Storage(
                name_nice = "Tasks",
                restricted = True,
                module_type = None,
            )),
        ("doc", Storage(
            name_nice = "Documents",
            #description = "A library of digital resources, such as photos, documents and reports",
            restricted = True,
            module_type = None,
        )),
        ("stats", Storage(
            name_nice = "Statistics",
            restricted = True,
            module_type = None
        )),
    ])

    # -------------------------------------------------------------------------
    def customise_pr_group_resource(r, tablename):

        current.response.s3.crud_strings[tablename] = Storage(
            label_create = T("Create Resource"),
            title_display = T("Resource Details"),
            title_list = T("Resources"),
            title_update = T("Edit Resource"),
            label_list_button = T("List Resources"),
            label_delete_button = T("Delete Resource"),
            msg_record_created = T("Resource added"),
            msg_record_modified = T("Resource updated"),
            msg_record_deleted = T("Resource deleted"),
            msg_list_empty = T("No Resources currently registered"))

        from s3 import S3SQLCustomForm
        crud_form = S3SQLCustomForm((T("Name"), "name"))

        current.s3db.configure(tablename,
                               crud_form = crud_form,
                               )

    settings.customise_pr_group_resource = customise_pr_group_resource

# =============================================================================
def wacop_event_rheader(r, tabs=[]):
    """ EVENT custom resource headers """

    if r.representation != "html":
        # Resource headers only used in interactive views
        return None

    from s3 import s3_rheader_resource, S3ResourceHeader

    tablename, record = s3_rheader_resource(r)
    if tablename != r.tablename:
        resource = current.s3db.resource(tablename, id=record.id)
    else:
        resource = r.resource

    rheader = None
    rheader_fields = []

    if record:
        T = current.T

        if tablename == "event_incident":

            if not tabs:
                tabs = [(T("Incident Details"), None),
                        (T("Units"), "group"),
                        (T("Tasks"), "task"),
                        (T("SitReps"), "sitrep"),
                        ]

            rheader_fields = [["name",
                               ],
                              ["zero_hour",
                               ],
                              ["comments",
                               ],
                              ]

        rheader = S3ResourceHeader(rheader_fields, tabs)(r,
                                                         table=resource.table,
                                                         record=record,
                                                         )
    return rheader

# END =========================================================================
