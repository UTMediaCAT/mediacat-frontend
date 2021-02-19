import ijson
with open("output.json", "r") as output:
    parser = ijson.parse(output)
    current = ""
    columns = ""
    column_set = False
    curr_col = ""
    multi_columns = []
    entry_id = ""
    with open('output.csv', 'w', encoding="utf-8") as file:
        for prefix, event, value in parser:
            # Adds columns
            if event == "map_key":
                if prefix == "":
                    entry_id = value
                else:
                    curr_col = value
                    if not column_set:
                        columns += curr_col + ","
            if prefix == entry_id+"." + curr_col:
                # Parses [, means there will be an array,
                # so an empty string is created
                if event == "start_array":
                    multi_columns.append("")
                # Parses ], means the array is done, so the last element
                # of the list is added to current row
                elif event == "end_array":
                    current += multi_columns[-1] + ","
                else:
                    if not value:
                        current += "null,"
                    elif type(value) == int:
                        current += str(value) + ","
                    else:
                        # Replaces commas to not mess up the csv structure
                        current += value.replace(",","") + ","
            # This means it's an item of a list, so we add it to the last
            # element of the list
            elif prefix == entry_id+"."+curr_col+".item":
                multi_columns[-1] += value + " "
            # Marks the end of the element
            elif entry_id != "" and prefix == entry_id and event == "end_map":
                if not column_set:
                    file.write(columns+"\n")
                    print("Column "+columns)
                    column_set = True
                file.write(current+"\n")
                print("Sent "+entry_id)
                current = ""
                curr_col = ""
                multi_columns = []
                entry_id = ""
        # print('prefix={}, event={}, value={}'.format(prefix, event, value))
