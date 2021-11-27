import csv
import ijson
from datetime import date
DATA_PATH = '../../../data/current/'

def find_twitter_data_by_ids(ids_to_find:list[str], filename:str):
    print("ran find_twitter_data_by_ids")
    current = ""
    columns = ""
    column_set = False
    curr_col = ""
    multi_columns = []
    entry_id=""
    num_ids_found = 0
    id_found =False
    
    parser = ijson.parse(open(DATA_PATH+'interest_output.json', 'r'))

    # output_dd_mm_yyyy.csv
    today = date.today()
    date_string = today.strftime("%d-%m-%Y")
    output_file_name = 'output/'+filename+'_'+date_string+'.csv'

    with open(output_file_name,'w', encoding="utf-8") as file:
        data_type =''
        for prefix, event, value in parser:
            if num_ids_found>=len(ids_to_find):
                break
            if event == "map_key" and prefix=="":
                id_found = value in ids_to_find
                if id_found:
                    print("found")
            if id_found:
                # Adds columns
                if event == "map_key":
                    if prefix == "":
                        entry_id = value
                    else:
                        curr_col = value
                        if not column_set:
                            columns+=curr_col+","

                if prefix == entry_id+"."+curr_col:
                    # Parses [, means there will be an array, so an empty string is created
                    if event == "start_array":
                        multi_columns.append("")
                    # Parses ], means the array is done, so the last element of the list
                    # is added to current row
                    elif event == "end_array":
                        current+=multi_columns[-1]+","
                    else:
                        if not value:
                            current +="null,"
                        elif type(value) == int:
                            current +=str(value)+","
                        else:
                            # Replaces commas to not mess up the csv structure
                            current+=value.replace(",","")+","
                # This means it's an item of a list, so we add it to the last element of the list
                elif prefix == entry_id+"."+curr_col+".item":
                    multi_columns[-1]+=value+" "
                if prefix.endswith('.type'):
                    data_type = value
                # Marks the end of the element
                elif entry_id != "" and prefix == entry_id and event == "end_map":
                    if not column_set:
                        file.write(columns+"\n")
                        print("Column "+columns)
                        column_set = True
                    # only print twitter refs
                    if data_type == 'twitter':
                        file.write(current+"\n")
                        print("Sent "+entry_id)
                    current = ""
                    data_type=""
                    curr_col = ""
                    multi_columns = []
                    entry_id = ""
                    num_ids_found +=1
        #print('prefix={}, event={}, value={}'.format(prefix, event, value))
    print("DONE! check "+output_file_name)
    file.close()


if __name__ == '__main__':
    freeze_support()