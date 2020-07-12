python3 mergeOutputs.py /mnt/e/GSoC20/Reactome-Failed-Queries/eutils_output.csv /mnt/e/GSoC20/Reactome-Failed-Queries/text.out
mkdir Output_Batch1
mv pmid_list.txt Output_Batch1
mv eutils_output.csv Output_Batch1
mv abstract.txts Output_Batch1
mv text.out Output_Batch1
git add .
git commit -m "Batch 1"
git push