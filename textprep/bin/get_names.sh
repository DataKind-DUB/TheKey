#
# Scrapes known resources for first names and surnames, compiles a single ordered list of unique entries.
#

# This is the top-N names we want to retrieve
THRESHOLD=2500

wget http://www2.census.gov/topics/genealogy/2000surnames/names.zip
unzip names.zip

head -${THRESHOLD} app_c.csv | grep -v "name" | cut -d',' -f1 > names_freq.txt
cat app_c.csv | grep -v "name" | cut -d',' -f1 > names_all.txt
rm names.zip
echo "Got lists from US Census"
wc -l names_all.txt
wc -l names_freq.txt

#
# CMU names list
#
wget http://www.cs.cmu.edu/afs/cs/project/ai-repository/ai/util/areas/nlp/corpora/names/male.txt
wget http://www.cs.cmu.edu/afs/cs/project/ai-repository/ai/util/areas/nlp/corpora/names/female.txt
cat male.txt female.txt | grep -v "^#" > cmu_names.txt
wc -l cmu_names.txt

