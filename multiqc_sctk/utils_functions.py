#!/usr/bin/env python


def update_dict(headers, rows_list, col_map, prefix=""):
    """update the data dict and headers dict"""

    table = dict()
    for row in rows_list:
        is_percentage = False
        col_name = row[0]
        col_data = row[1]

        # Sanitize numeric data
        col_data = col_data.replace(",", "")

        if "Percentage" in col_name:
            is_percentage = True

        # Convert to float when possible
        try:
            col_data = float(col_data)
        except:
            col_data = col_data

        if col_name in col_map.keys():
            if prefix == "":
                col_id = col_map[col_name]
                col_desc = col_name
            else:
                col_id = f"{prefix} {col_map[col_name]}"
                col_desc = f"{prefix}: {col_name}"
            table[col_id] = col_data
            headers[col_id] = {"title": col_id, "description": col_desc}
            if is_percentage:
                headers[col_id].update({"suffix": "%", "max": 100, "min": 0})

    return table, headers


def set_hidden_cols(headers, col_names):
    """Set the hidden columns"""

    for col_name in col_names:
        try:
            headers[col_name]["hidden"] = True
        except KeyError:
            pass

    return headers


def update_plot_data(tag, self_plot_data, json_dict, s_name):
    plot_data = self_plot_data.get(tag, [dict(), dict()])
    plot_data[0].update({s_name: transform_data(json_dict[tag]['density']['data'])})
    plot_data[1].update({s_name: transform_data(json_dict[tag]['cumsum']['data'])})
    
    return plot_data

def transform_data(data):
    """Transform x:list,y:list data to a dict of x_val:y_val"""

    value_dict = dict()
    for idx, row in enumerate(data["x"]):
        value_dict[row] = data["y"][idx]

    return value_dict
