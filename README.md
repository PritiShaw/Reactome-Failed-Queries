Reactome Query Analysis
---

## How to Run
```
docker run --name query-processor \
-e INDRA_DB_REST_URL={Enter API Endpoint} \
-v /PATH/TO/R/script.Rmd:/src/script.Rmd \
-v /PATH/TO/Output/HTML/file.html:/src/output.html \
-v /PATH/TO/OUTPUT/FOLDER:/src/processor \
-t pritishaw/reactome-query-processing
```

