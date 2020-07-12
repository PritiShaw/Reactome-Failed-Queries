python3 mergeOutputs.py
mkdir Output_Batch1
mv pmid-list.txt Output_Batch1
mv eutils_output.csv Output_Batch1
mv abstracts.txts Output_Batch1
mv text.out Output_Batch1
git add .
git commit -m "Batch 1"
git push