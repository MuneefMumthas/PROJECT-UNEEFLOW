
# variables for configuration

main_window = None

#data frames
df = None
df_selected = None
df_handled_missing_values = None
df_encoded = None

#variables
selected_target_variable = None
selected_input_variables = []

uri = None

#missing values screen saving
saved_actions = {}
prev_columns = None


#input variable screen saving
prev_input_columns = None
saved_selected_inputs = {}

current_step = None
total_missing = 0


profile_cache = {}

profile_temp_dirs = []

#saving encoding methods
saved_target_encoding = {}
saved_categorical_encoding = {}

#paths for assets
uneeflow_logo = 'assets/UNEE FLOW LOGO.png'
uneeflow_ctk_theme = 'assets/UneeFlow_theme.json'
uneeflow_logo_icon = 'assets/U Logo.ico'
uneeflow_data_profile_config = 'assets/config_default.yaml'


chat_bot = None


#train test split
test_size = None
train_size = None
split_random_state = None

#task type
task_type = None

#function to reset the config when needed
def reset_config():
    global df, df_selected, df_handled_missing_values, df_encoded
    global selected_target_variable, selected_input_variables
    global saved_actions, prev_columns, uri
    global current_step, total_missing
    global saved_target_encoding, saved_categorical_encoding
    global prev_input_columns, saved_selected_inputs

    #reseting necessary variables to their initial state
    #data frames
    df = None
    df_selected = None
    df_handled_missing_values = None
    df_encoded = None

    #variables
    selected_target_variable = None
    selected_input_variables = []
    saved_actions = {}
    prev_columns = None
    uri = None

    total_missing = 0

    prev_input_columns = None
    saved_selected_inputs = {}

    #encoding methods
    saved_target_encoding = {}
    saved_categorical_encoding = {}