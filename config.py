
# variables for configuration

main_window = None

#data frames
df = None
df_selected = None
df_handled_missing_values = None
df_encoded = None
df_not_encoded = None

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
X_train = None
X_test = None
y_train = None
y_test = None

#task and model type
task_type = None#
selected_model = None
trained_model = None
model_random_state = None

#predictions
predictions = None

col_transformer = None
ohe_columns = []
ordinal_encode_cols = []
transformers = []
target_class_labels = None
pipe = None
label_encoder = None

file_name = None

#flag to confirm if the export was successful
export_confirmation = False

model_package = None


#function to reset the config when needed
def reset_config():
    global df, df_selected, df_handled_missing_values, df_encoded, df_not_encoded
    global selected_target_variable, selected_input_variables
    global saved_actions, prev_columns, uri
    global current_step, total_missing
    global saved_target_encoding, saved_categorical_encoding
    global prev_input_columns, saved_selected_inputs
    global X_train, X_test, y_train, y_test
    global trained_model
    global predictions
    global col_transformer, ohe_columns, ordinal_encode_cols, transformers, target_class_labels, pipe, label_encoder
    global file_name, export_confirmation

    #reseting necessary variables to their initial state
    #data frames
    df = None
    df_selected = None
    df_handled_missing_values = None
    df_encoded = None
    df_not_encoded = None

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

    #train test split
    X_train = None
    X_test = None
    y_train = None
    y_test = None

    trained_model = None

    predictions = None

    col_transformer = None
    ohe_columns = []
    ordinal_encode_cols = []
    transformers = []
    target_class_labels = None
    pipe = None
    label_encoder = None

    file_name = None
    export_confirmation = False