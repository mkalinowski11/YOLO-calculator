import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
#
import cv2
import numpy as np
#
from equation_processing.equation import Equation
from equation_processing.equation_processing import find_equation_ids, get_equations
from yolo_model import Yolov5Model, IMG_SIZE
from image_processing.image_utils import decode_image, encode_image
#
MODEL_PATH = 'model/best2.pt'
yolo_model = Yolov5Model(model_path=MODEL_PATH, img_size=IMG_SIZE)

def Header(name, app):
    title = html.H1(name, style={"margin-top": 5})
    return dbc.Row([dbc.Col(title, md=8)])

def image_card(src, header=None):
    return dbc.Card(
        [
            dbc.CardHeader(header),
            dbc.CardBody(html.Img(src=src, style={"width": "100%"})),
        ]
    )

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

controls = [
    dcc.Upload(
        dbc.Card(
            "Drag and Drop or Click",
            body=True,
            style={
                "textAlign": "center",
                "borderStyle": "dashed",
                "borderColor": "black",
            },
        ),
        id="img-upload",
        #
        multiple=False,
    )
]

app.layout = dbc.Container(
    [
        Header("Photo Calculator", app),
        html.Hr(),
        dbc.Row([dbc.Col(c) for c in controls]),
        html.Br(),
        dbc.Spinner(
            dbc.Row(
                [
                    *[dbc.Col(html.Div(id=img_id)) for img_id in ["original-img","prediction-image"]],
                    html.Button(id='predict-button-state', n_clicks=0, children='Predict')
                ]
            )
        ),
        dcc.Store(id='store-data', storage_type='memory'),
        dcc.Store(id='prediction-data', storage_type='memory'),
        dcc.Store(id='store-data-len', storage_type='memory'),
        dcc.Store(id='pred-data-len', storage_type='memory')
    ],
    fluid=False,
)

@app.callback(
    [Output("store-data", "data")],
    [Input("img-upload", "contents")]
)
def upload_data(input_data):
    if input_data is None:
        return dash.no_update
    image_to_display = image_card(input_data[-1], header="Original Image")
    #return input_data, image_to_display
    return input_data,

@app.callback([Output("original-img", "children"), Output('prediction-image', 'children'),
               State('prediction-data', 'data'),
               Input("img-upload", "contents")]
)
def update_images(prediction_data, uploaded_data):
    input_data_im = dash.no_update
    prediction_data_im = dash.no_update
    if uploaded_data is not None:
        input_data_im = image_card(uploaded_data, "Uploaded image")
    return input_data_im, prediction_data_im

@app.callback([Output('prediction-data', 'data'),
               Input('predict-button-state', 'n_clicks'),
               State('store-data', 'data')]
)
def update_output(n_clicks, data_list):
    # if data_list is None:
    #     return dash.no_update
    # prediction_images = []
    # for image in data_list:
    #     image = decode_image(img_str = image)
    #     opencvImage = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    #     prediction = model.predict(image)
    #     _, cords = get_yolo_bbox_data(prediction)
    #     opencvImage = plot_yolo_bbox(cords, opencvImage, treshold = 0.4)
    #     b64_string = encode_image(opencvImage)
    #     prediction_images.append(b64_string)
    # return prediction_images,
    return dash.no_update

if __name__ == '__main__':
    app.run_server(debug=True)