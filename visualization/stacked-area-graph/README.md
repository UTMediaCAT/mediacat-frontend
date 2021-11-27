# How to generate a stacked area graph

1. first run the script in `post-processor-to-csv`
2. move the existing `input_for_stacked_area_graph.csv` and `data_for_stacked_area_chart.csv` to a folder in `old`. Use the date it was generated as the folder name. ex `old/15-11-2021/`
3. then run `python parse_data_for_stacked_area_graph.py` (use `python3` for mac/linux) (takes around 8+ min)
4. after that finishes, run the `postprocessing_stacked_area_chart_new.ipynb` file. The stacked area graph will be generated in this file. You can download or screenshot the stacked area graph
5. In addition `data_for_stacked_area_chart.csv` will be generate. This is the raw data used for the stacked area graph

# How to generate twitter csvs for each source
1. go to the `twitter-data-for-scope` folder
2. move any data in `/output/` to a folder in old.  Use the date it was generated as the folder name. ex `old/15-11-2021/`
3. run `python find_scope_data.py`(use `python3` for mac/linux) 
4. the csvs will be in the `output` folder
5. Cross check these csvs with `data_for_stacked_area_chart.csv`. If the data does not make sense then there is an issue with one of the scripts

# Extra
- right now the scripts have been coded to work only with twitter data since the articles do not have dates yet.

