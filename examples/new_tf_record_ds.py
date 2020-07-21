import numpy as np
import time
import tensorflow as tf
from utils.load_data import serialize_example
from utils.load_data import _parse_function
from utils.load_data import show_some_records

# Create NumPy dataset
num_obs = int(1e2)
f0 = np.random.choice([False, True], num_obs)
f1 = np.random.randint(0, 5, num_obs)
strings = np.array([b'cat', b'dog', b'chicken', b'horse', b'goat'])
f2 = strings[np.random.randint(0, 5, num_obs)]
f3 = np.random.randn(num_obs)

# Print the proto message generated by a single obs
example_proto = serialize_example(False, 4, b'goat', 0.9876)
print(tf.train.Example.FromString(example_proto))

output_file = 'test.tfrecord'
tic = time.time()
with tf.io.TFRecordWriter(output_file) as writer:
    for i in range(num_obs):
        example = serialize_example(f0[i], f1[i], f2[i], f3[i])
        writer.write(example)
toc = time.time()
print(f'It took {toc - tic:4.2f} sec to write')

input_files = [output_file]
raw_ds = tf.data.TFRecordDataset(input_files)
show_some_records(1, raw_ds)

parsed_ds = raw_ds.map(_parse_function)
print('\nParsed nicely')
show_some_records(1, parsed_ds)
