python3 ./python/script.py
cd /src/R
R -e "rmarkdown::render('/src/script.Rmd', output_file='/src/output.html')" 
