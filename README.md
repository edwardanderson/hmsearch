# HmSearch

Simple Python interface to [HmSearch](http://hmsearch.io/) using subprocess


## Install

Save `hmsearch.py` in your project directory
```
wget https://github.com/edwardanderson/hmsearch/raw/master/hmsearch.py 
```

Install dependencies and download the [HmSearch GitHub](https://github.com/commonsmachinery/hmsearch) repository
```
sudo apt-get install libkyotocabinet-dev kyotocabinet-utils
git clone https://github.com/commonsmachinery/hmsearch
cd hmsearch
make
```

## Use

~~~python
import hmsearch

# Initialise by specifying the location of the `hmsearch` repository
db = hmsearch.HmSearch(source='/path/to/hmsearch/')

# Create a new database
db.create('hashes.kch', hash_size=128, max_error=10, max_hashes=1000000)
~~~

~~~python
# Connect to an existing database
db = hmsearch.HmSearch(database='hashes.kch')

# Add some hashes
hashes = ['0049697068f4ccfcfeff3f00eb768520',
          '0048697068f4cc6cfeff3f006b768500',
          '0040697068f4cc6cfeff3f006bb68500']

db.insert(hashes)

# Search for a hash
result = db.lookup('0048697068f4cc6cfeff3f006b768500')
print(result)
~~~

~~~
[('0040697068f4cc6cfeff3f006bb68500', '3'), ('0048697068f4cc6cfeff3f006b768500', '0'), ('0049697068f4ccfcfeff3f00eb768520', '5')]
~~~
