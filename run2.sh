python3 mergeOutputs.py /mnt/e/GSoC20/Reactome-Failed-Queries/eutils_output.csv /mnt/e/GSoC20/Reactome-Failed-Queries/text.out
mkdir Output_Batch2
mv pmid_list.txt Output_Batch2
mv eutils_output.csv Output_Batch2
mv abstract.txts Output_Batch2
mv text.out Output_Batch2
git add .
git commit -m "Batch 2"
git push