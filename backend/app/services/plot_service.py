import json
import plotly.express as px
from plotly.utils import PlotlyJSONEncoder
from app.services.data_service import data_service


class PlotService:
    def __init__(self):
        self.available_plots = {
            "scatter": {"x": ["numeric"], "y": ["numeric"], "color": ["categorical", "numeric"]},
            "histogram": {"x": ["numeric", "categorical"], "color": ["categorical"]},
            "box": {"x": ["categorical"], "y": ["numeric"], "color": ["categorical"]},
            "bar": {"x": ["categorical"], "y": ["numeric"], "color": ["categorical"]},
            "violin": {"x": ["categorical"], "y": ["numeric"], "color": ["categorical"]}
        }

    def get_available_plots(self):
        return list(self.available_plots.keys())

    def get_plot_variables(self, plot_type):
        if plot_type not in self.available_plots:
            raise ValueError(f"Plot type '{plot_type}' is not supported.")

        requirements = self.available_plots[plot_type]
        numeric_cols = data_service.get_numeric_columns()
        categorical_cols = data_service.get_categorical_columns()

        variables = {}
        for axis, allowed_types in requirements.items():
            variables[axis] = []
            if "numeric" in allowed_types:
                variables[axis].extend(numeric_cols)
            if "categorical" in allowed_types:
                variables[axis].extend(categorical_cols)

        return variables

    @staticmethod
    def generate_plot(plot_type, x_column, y_column=None, color_by=None, filters=None):
        if filters:
            filters = json.loads(filters)
        df = data_service.get_filtered_data(filters)

        plot_args = {'x': x_column}
        if y_column not in [None, '']:
            plot_args['y'] = y_column
        if color_by not in [None, '']:
            plot_args['color'] = color_by

        if plot_type == "scatter":
            fig = px.scatter(df, **plot_args)
        elif plot_type == "histogram":
            fig = px.histogram(df, **plot_args)
        elif plot_type == "box":
            fig = px.box(df, **plot_args)
        elif plot_type == "bar":
            if y_column is None:
                df_count = df[x_column].value_counts().reset_index()
                df_count.columns = [x_column, 'count']
                plot_args['y'] = 'count'
                fig = px.bar(df_count, **plot_args)
            else:
                fig = px.bar(df, **plot_args)
        elif plot_type == "violin":
            fig = px.violin(df, **plot_args)
        else:
            raise ValueError(f"Plot type '{plot_type}' is not supported.")

        fig_dict = {'data': fig.to_dict()}

        return json.dumps(fig_dict, cls=PlotlyJSONEncoder)


plot_service = PlotService()
