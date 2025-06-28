
# variables for configuration

main_window = None

df = None
df_selected = None
df_handled_missing_values = None

selected_target_variable = None
saved_actions = {}
prev_columns = None
uri = None

current_step = None
total_missing = 0

profile_cache = {}

profile_temp_dirs = []


uneeflow_logo = 'assets/UNEE FLOW LOGO.png'
uneeflow_ctk_theme = 'assets/UneeFlow_theme.json'
uneeflow_logo_icon = 'assets/U Logo.ico'
uneeflow_data_profile_config = 'assets/config_default.yaml'

from model.chat_bot import ChatBot
chat_bot = ChatBot()