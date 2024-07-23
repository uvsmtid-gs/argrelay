from datetime import datetime

from dateutil.tz import tz

from argrelay.check_env.CheckEnvResult import CheckEnvResult
from argrelay.check_env.PluginCheckEnvServerResponseValueAbstract import PluginCheckEnvServerResponseValueAbstract
from argrelay.custom_integ.SchemaPluginCheckEvnServerResponseValueAbstract import field_values_to_command_lines_
from argrelay.enum_desc.CheckEnvField import CheckEnvField


class PluginCheckEnvServerResponseValueStartTime(PluginCheckEnvServerResponseValueAbstract):

    def __init__(
        self,
        plugin_instance_id: str,
        plugin_config_dict: dict,
    ):
        super().__init__(
            plugin_instance_id,
            plugin_config_dict = plugin_config_dict or {
                field_values_to_command_lines_: {
                    CheckEnvField.server_start_time.name: "argrelay.check_env server_start_time",
                },
            },
        )

    def verify_online_value(
        self,
        field_name,
        field_value,
    ) -> CheckEnvResult:
        check_env_result: CheckEnvResult = super().verify_online_value(
            field_name,
            field_value,
        )
        # Put formated time to the message:
        if check_env_result.result_category.VerificationSuccess:
            from_zone = tz.tzutc()
            into_zone = tz.tzlocal()
            utc_time = datetime.utcfromtimestamp(int(field_value))
            utc_time = utc_time.replace(tzinfo = from_zone)
            check_env_result.result_message = utc_time.astimezone(into_zone).isoformat()
        return check_env_result
