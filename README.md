# Key-value store one hour

This repo contains the code for a simple key-value store that I live-coded during a one-hour-long presentation on
databases at the Recurse Center.

Its purpose is purely educational. It aims at demonstrating how some of the underlying principles of log-structured
storage engines can be implemented in practice.

## Getting started

```shell
# Run the script
python3 main.py
```

## Step-by-step implementation

This key-value store was implemented following these steps:

* **Step 1: insertion**
  ([commit](https://github.com/MaudGautier/key-value-store-one-hour/commit/a89c43178cf17f9dc86056ce4a218811868cc2f2)):
  We add key-value pairs by appending them to a datafile.
* **Step 2: lookups**
  ([commit](https://github.com/MaudGautier/key-value-store-one-hour/commit/3c12a36ae095fe80de4a773c4e992a87286c07c0)):
  We retrieve the value associated to a given key by reading the datafile line by line
  and return the last (i.e. most recently written) value for that key.
* **Step 3: hash index**
  ([commit](https://github.com/MaudGautier/key-value-store-one-hour/commit/fac6cc0710a161c2208a14c676ad6ab8d08d18a3)):
  We add a hash index (i.e. in-memory hash-map that maps every key to its corresponding byte
  offset in the datafile). This allows to speed up reads by improving time complexity for lookups from `o(n)` (linear
  time) to `o(1)` (constant time).
* **Step 4: compaction**
  ([commit](https://github.com/MaudGautier/key-value-store-one-hour/commit/19a9829eeacd4e3e35f1353218d49fbe4dab91f4)):
  The compaction operation allows to overcome the limitation of append-only files by reclaiming
  disk space. It works by recording the most recent value for each key and rewrite all these records in a compacted
  file (which does not contain any obsolete key).
* **Step 5: merging**
  ([commit](https://github.com/MaudGautier/key-value-store-one-hour/commit/06d86a9adda77a49fb2e8e2dfb003ab399ab75f9)):
  The merging operation performs both compaction and merging so that we can reclaim disk space (
  compaction) and avoid the overhead of maintaining too many datafiles (merging).

With just those 5 simple steps, we get an implementation that is close in essence to what is done
in [Bitcask](https://docs.riak.com/riak/kv/2.2.3/setup/planning/backend/bitcask/index.html), a storage engine used in
[Riak](https://docs.riak.com/riak/kv/latest/index.html).

For reference, the article explaining the core ideas behind the design of Bitcask can be
found [here](https://riak.com/assets/bitcask-intro.pdf).

