'''
    Simple interface to HmSearch using subprocess

    http://hmsearch.io/
    https://github.com/commonsmachinery/hmsearch
'''

import os
import subprocess


class HmSearch(object):
    '''
    Use:

        Initialise by specifying location of `hmsearch` directory (default: current):
            >>> db = hmsearch.HmSearch(source='/path/to/hmsearch/')

        Either connect to an existing database:
            >>> db = hmsearch.HmSearch(source='/path/to/dir/', database='/path/to/db.kch')
        or create a new database:
            >>> db.create('hashes.kch', hash_size=128, max_error=10, max_hashes=1000000)

        Search for a hash:
            >>> result = db.lookup('f0d0d4c494f4fcccfffff0ff7f270002')
            >>> type(result)
            <type 'list'>

        Add a list of new hashes
            >>> hashes = ['y2dfd4c494f4fc5cfffff0f17f270002',
                          'f0d04vc494f4fcccffguff0ff7f270006']

            >>> db.insert(hashes)
    '''

    def __init__(self, source=None, database=None):
        if source is not None:
            self.source = source
        else:
            self.source = os.path.join(os.getcwd(), 'hmsearch')

        self.database = database

    def _run_cmd(self, script, *params):
        if not os.path.isfile(os.path.join(self.source, script)):
            raise Exception('Cannot find {} in {}'.format(script, self.source))

        cmd = [os.path.join(self.source, script)] + [str(p) for p in params]
        try:
            response = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            raise Exception(e.output)

        if response:
            return response

    def create(self, database, hash_size, max_error, max_hashes):
        self._run_cmd('hm_initdb', database, hash_size, max_error, max_hashes)
        if self.database is None:
            self.database = database

    def lookup(self, hash_str):
        results = []
        response = self._run_cmd('hm_lookup', self.database, hash_str)
        lines = response.split('\n')
        for i in lines:
            if not i:
                continue

            key, distance = i.split(' ')
            results.append((key, distance))

        return results

    def insert(self, hashes):
        hashes = ' '.join(hashes)

        p = subprocess.Popen([os.path.join(self.source, 'hm_insert'), self.database],
                             stdout=subprocess.PIPE,
                             stdin=subprocess.PIPE,
                             stderr=subprocess.STDOUT)

        p.communicate(hashes)[0]
