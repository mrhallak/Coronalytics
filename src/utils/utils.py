def generate_document(body: dict, current_execution_date: str) -> dict:
    """This function helps by convering
    the data scraped from JHU to a
    document that we will store in 
    ElasticSearch.
    
    Arguments:
        body {dict} -- JSON object received
        current_execution_date {str} -- DAG's execution date
    
    Returns:
        dict -- Transformed object
    """    
    doc = {
        "updated": current_execution_date,
        "confirmed": body["Confirmed"],
        "deaths": body["Deaths"],
        "recovered": body["Recovered"],
        "location": {"lon": body["Long_"], "lat": body["Lat"]},
        "country_name": body["Country_Region"],
    }

    return doc
