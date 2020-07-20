Reactome Query Analysis
---

## How to Run
```
docker run --name query-processor \
-e INDRA_DB_REST_URL={Enter API Endpoint} \
-v /PATH/TO/OUTPUT/FOLDER:/src/processor \
-t pritishaw/reactome-query-processing
```


## Results
Final Result : `output.tsv` present in folder mounted to `/src/processor`
