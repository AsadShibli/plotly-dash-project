import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import html
import json
from dash import dcc
from dash.dependencies import Input,Output,State
from dash import dash_table



external_stylesheets = [
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
        'crossorigin': 'anonymous'
    }
]



app = dash.Dash(__name__, external_stylesheets=['https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css'])
server = app.server

df = pd.read_csv("car.csv")



# Available options for brand and model_date
brands = ['All','MG', 'Toyota', 'Honda', 'KIA', 'Nissan', 'Suzuki',
          'Mercedes Benz', 'Range Rover', 'Daihatsu', 'Changan', 'BMW',
          'Hyundai', 'Mazda', 'Haval', 'DFSK', 'Mitsubishi', 'Audi',
          'Chevrolet', 'Porsche', 'United', 'Others', 'FAW', 'Lexus',
          'Prince', 'Chrysler', 'Subaru', 'Peugeot', 'Ford', 'Land Rover',
          'Master', 'Volkswagen', 'Chery', 'Willys', 'Proton', 'Jeep',
          'MINI', 'SsangYong', 'Isuzu', 'Daewoo', 'Daehan', 'BAIC', 'Tesla',
          'Cadillac', 'Datsun', 'Adam', 'Hummer', 'Alfa Romeo', 'Sogo',
          'Golf', 'Jaguar', 'Dodge', 'Hino', 'Buick', 'Morris', 'JW Forland',
          'Bentley', 'JAC', 'Fiat', 'Roma', 'JMC', 'Ferrari', 'Geely',
          'ZOTYE', 'Opel', 'Vauxhall', 'Oldsmobile', 'GMC', 'Citroen',
          'Classic Cars', 'Mushtaq', 'Volvo']


dates = ['All','2023', '2022', '2021', '2020', '2019', '2018', '2017',
               '2016', '2015', '2014', '2013', '2012', '2011', '2010']


#top_5 price table
top_5_price = df[df['price'].notnull()]['price'].astype(float).nlargest(5).values.tolist()

temp_df = df[df["price"].isin(top_5_price)]
temp_df = temp_df.iloc[:,1:]
temp_df.drop("description",axis=1,inplace=True)

table_columns = [{"name": i, "id": i} for i in temp_df.columns]

fig = px.bar(temp_df, "brand", "price",title="Brand-wise Prices")
fig.update_layout(title={
        'y':0.88,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
        title_font_size=25)
app.layout = html.Div(children=[
    html.Div(children=[
        html.H1("Used Car Information",id="header", className="col-md-12")

    ], className="row"),
    html.Div(children=[

        # car img
        html.Div(id="car_img", children=[
            html.Img(
                src="https://purepng.com/public/uploads/large/purepng.com-lamborghinilamborghinilamborghini-automobilelamborghini-carssports-car-1701527505254qtosu.png")
        ], className="col-md-6"),

        # select boxes and input btn
        html.Div(id="input-box",children=[
            html.Div(children=[
                html.H4("Select Brand"),
                dcc.Dropdown(
                        id='brand-dropdown',
                        options=[{'label': i, 'value': i} for i in brands],
                        value='All'
            )]  ,className="col-md-12"),

            html.Div(children=[
                html.H4("Select Year"),
                dcc.Dropdown(
                    id='year-dropdown',
                    options=[{'label': i, 'value': i} for i in dates],
                    value="All",
                )] ,className="col-md-12"),
            html.Div(children=[
                html.Button('Submit', id='submit-btn',className="btn-dark",n_clicks=0)
            ], className="col-md-12")

        ], className="col-md-6"),

    ], className="row"),
    html.Div(children=[
        html.Div(children=[
            html.Div(children=[

                html.Div(children=[

                    html.Div(id="table",children=[

                    ])
                ],className="card-body table-responsive")
            ],className="card",style={"padding-top":"20px"})
        ],className="col-md-12")
    ], className="row",style={"padding-top":"20px"}),
    html.Div(children=[
        html.Div([
            html.Div([
                html.Div([
                    html.Div(children=[
                    html.H3("Top 5 expensive car"),
                    dash_table.DataTable(
                        id='top-5-table',
                        columns=table_columns,
                        data=temp_df.to_dict('records')

                    )
                ],className="card-body table-responsive")
            ],className="card" ,style={"margin-top":"50px"})
        ],className="col-md-6"),
        html.Div([
            dcc.Graph(figure=fig)
        ], className="col-md-6")
    ], className="row")
], className="container")]
)





@app.callback(Output('table', 'children'),
              Input('submit-btn', 'n_clicks'),
              State('brand-dropdown', 'value'),
              State('year-dropdown', 'value'))
def update_output(n_clicks, brand, year):
    if n_clicks > 0:
        if brand == 'All' and year == 'All':
            filtered_df = df
        elif brand == 'All':
            filtered_df = df[df['model_date'] == year]
        elif year == 'All':
            filtered_df = df[df['brand'] == brand]
        else:
            filtered_df = df[(df['brand'] == brand) & (df['model_date'] == year)]

        my_table  = dash_table.DataTable(
            columns = [{"name":col,"id":col} for col in filtered_df.columns],
            data = filtered_df.to_dict("records"),
            page_size= 10
        )
        return my_table

if __name__ == '__main__':
    app.run_server(debug=True)


