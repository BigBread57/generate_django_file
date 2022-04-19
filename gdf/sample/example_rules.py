import rules
from rules.predicates import is_authenticated


rules.add_perm('{{app_name}}.view_{{lower_main_class}}', is_authenticated)
rules.add_perm('{{app_name}}.add_{{lower_main_class}}', is_authenticated)
rules.add_perm('{{app_name}}.change_{{lower_main_class}}', is_authenticated)
rules.add_perm('{{app_name}}.delete_{{lower_main_class}}', is_authenticated)
rules.add_perm('{{app_name}}.list_{{lower_main_class}}', is_authenticated)
