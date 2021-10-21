[![Build Status](https://travis-ci.org/UTMediaCAT/mediacat-frontend.svg?branch=master)](https://travis-ci.org/UTMediaCAT/mediacat-frontend)

# mediacat-frontend

Visualization: Work has been done on the aspect of helping the team visualize date in the #7-visualizations branch

Scope Parser: preliminary checks on the scope data before feeding it into the domain crawler

## visualization (/visualization/ folder)

-   network-graph
    -   graph representation of the post-processor data
    -   Edges: from source to citer
    -   Nodes: url or text alias
-   pie-chart
    -   pie chart representation of the top cited sources
-   stacked-area-graph
    -   represents the change in the number of citations for multiple sources over a period of time
    -   x-axis: years, y-axis: number of citations
-   post-processor-to csv
    -   converts the output from the post-processor (json file) to a csv format

## scope_parser (/scope_parser/ folder)

do `python3 main.py scope.csv` to validate and check the full scope for any obvious errors. If successful, it outputs the list of domains in the correct format for the crawler (domain.csv) and links that gave errors (error.csv). It takes in the input of the full scope that was manually provided.

or `python3 main.py scope.csv` for validation + scope parser reformating

or `python3 mainNoValid.py scope.csv` skips validation then reformats the scope
