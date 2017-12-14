
# encoding = utf-8
# Always put this line at the beginning of this file
import ta_datadog_declare

import os
import sys

from alert_actions_base import ModularAlertBase
import modalert_datadog_event_helper

class AlertActionWorkerdatadog_event(ModularAlertBase):

    def __init__(self, ta_name, alert_name):
        super(AlertActionWorkerdatadog_event, self).__init__(ta_name, alert_name)

    def validate_params(self):

        if not self.get_global_setting("dd_uri"):
            self.log_error('dd_uri is a mandatory setup parameter, but its value is None.')
            return False

        if not self.get_global_setting("api_key"):
            self.log_error('api_key is a mandatory setup parameter, but its value is None.')
            return False

        if not self.get_global_setting("app_key"):
            self.log_error('app_key is a mandatory setup parameter, but its value is None.')
            return False

        if not self.get_param("title"):
            self.log_error('title is a mandatory parameter, but its value is None.')
            return False

        if not self.get_param("alert_type"):
            self.log_error('alert_type is a mandatory parameter, but its value is None.')
            return False

        if not self.get_param("priority"):
            self.log_error('priority is a mandatory parameter, but its value is None.')
            return False
        return True

    def process_event(self, *args, **kwargs):
        status = 0
        try:
            if not self.validate_params():
                return 3
            status = modalert_datadog_event_helper.process_event(self, *args, **kwargs)
        except (AttributeError, TypeError) as ae:
            self.log_error("Error: {}. Please double check spelling and also verify that a compatible version of Splunk_SA_CIM is installed.".format(ae.message))
            return 4
        except Exception as e:
            msg = "Unexpected error: {}."
            if e.message:
                self.log_error(msg.format(e.message))
            else:
                import traceback
                self.log_error(msg.format(traceback.format_exc()))
            return 5
        return status

if __name__ == "__main__":
    exitcode = AlertActionWorkerdatadog_event("TA-datadog", "datadog_event").run(sys.argv)
    sys.exit(exitcode)
