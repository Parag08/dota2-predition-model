import tensorflow as tf
import os

def get_files_list(folder='./data/'):
    fileslist = os.listdir(folder)
    csv_list = []
    for csv in fileslist:
        if csv[-3:-1]+csv[-1] == 'csv':
            csv_list.append(csv)
    return csv_list

def get_tensor(file_list,total_colums=115):
    filename_queue = tf.train.string_input_producer(file_list)
    reader = tf.TextLineReader()
    _, csv_row = reader.read(filename_queue)
    record_defaults = [[0 for x in range(1)] for y in range(total_colums)]
    values = ['col'+str(x) for x in range(total_colums)]
    values = tf.decode_csv(csv_row,record_defaults=record_defaults)
    features = tf.stack(values)
    return features ,values

def iterate_through_csv_file(features,function,length=100):
    with tf.Session() as sess:
        tf.global_variables_initializer().run()
        coord = tf.train.Coordinator()
        threads = tf.train.start_queue_runners(coord=coord)
        for i in range(length):
            try:
                example_data, country_name = sess.run([features, function])
                print(example_data, country_name,i)
            except tf.errors.OutOfRangeError:
                break
        coord.request_stop()
        coord.join(threads)

