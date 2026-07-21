app_name = "uxl_erp"
app_title = "UXL ERP"
app_publisher = "SSDolui"
app_description = "Customization of ERPNext and Cown customization"
app_email = "ssdolui.in@gmail.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "uxl_erp",
# 		"logo": "/assets/uxl_erp/logo.png",
# 		"title": "UXL ERP",
# 		"route": "/uxl_erp",
# 		"has_permission": "uxl_erp.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/uxl_erp/css/uxl_erp.css"
# app_include_js = "/assets/uxl_erp/js/uxl_erp.js"

# include js, css files in header of web template
# web_include_css = "/assets/uxl_erp/css/uxl_erp.css"
# web_include_js = "/assets/uxl_erp/js/uxl_erp.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "uxl_erp/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
    # "Customer": "public/js/cus_erpnext/doctype/customer.js",
    "Sales Order": "public/js/cus_erpnext/doctype/sales_order.js",
    "Item": "public/js/cus_erpnext/doctype/item.js",
    "Item Group": "public/js/cus_erpnext/doctype/item_group.js",
    "Sales Invoice": "public/js/cus_erpnext/doctype/sales_invoice.js",
}
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "uxl_erp/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "uxl_erp.utils.jinja_methods",
# 	"filters": "uxl_erp.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "uxl_erp.install.before_install"
# after_install = "uxl_erp.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "uxl_erp.uninstall.before_uninstall"
# after_uninstall = "uxl_erp.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "uxl_erp.utils.before_app_install"
# after_app_install = "uxl_erp.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "uxl_erp.utils.before_app_uninstall"
# after_app_uninstall = "uxl_erp.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "uxl_erp.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }


# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }
doc_events = {
    # "Customer": {
    #     "before_insert": "uxl_erp.cus_erpnext.doctype.customer.validate_create",
    #     "on_trash": "uxl_erp.cus_erpnext.doctype.customer.validate_delete"
    # },
    "Sales Order":{
        "validate":"uxl_erp.cus_erpnext.doctype.sales_order.validate",
        "set_value":"uxl_erp.cus_erpnext.doctype.sales_order.set_value",
    }
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"uxl_erp.tasks.all"
# 	],
# 	"daily": [
# 		"uxl_erp.tasks.daily"
# 	],
# 	"hourly": [
# 		"uxl_erp.tasks.hourly"
# 	],
# 	"weekly": [
# 		"uxl_erp.tasks.weekly"
# 	],
# 	"monthly": [
# 		"uxl_erp.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "uxl_erp.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "uxl_erp.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "uxl_erp.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["uxl_erp.utils.before_request"]
# after_request = ["uxl_erp.utils.after_request"]

# Job Events
# ----------
# before_job = ["uxl_erp.utils.before_job"]
# after_job = ["uxl_erp.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"uxl_erp.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

# Translation
# ------------
# List of apps whose translatable strings should be excluded from this app's translations.
# ignore_translatable_strings_from = []

before_migrate = "uxl_erp.setup.custom_field_added.apply"

after_migrate = "uxl_erp.setup.form_customization.apply"

fixtures = [
    {
        "dt": "Custom Field",
        "filters": [
            ["module","=","Cus ERPNext"]
        ]
    },
    {
        "dt": "Property Setter",
        "filters": [
            ["module","=","Cus ERPNext"]
        ]
    },
    {
        "dt": "Item Group",
        "filters": [
            ["item_group_name","=","Trade Item"]
        ]
    }
]