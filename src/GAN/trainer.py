import tensorflow as tf

from GAN.model import MIDINetDiscriminator, MIDINetGenerator, MIDINetGeneratorFFNN, column_distance_loss

from MIDIUtil.defaults import *
from MIDIUtil.MelodyWriter import MelodyWriter
from MIDIUtil.Melody import Melody
from MIDIUtil.Note import Note

import numpy as np

class Trainer:
    def __init__(self, config, data_loader):
        self.config = config
        self.data_loader = data_loader
        self.batch_size = config.batch_size

        self.build_models()

        self.step = tf.Variable(0, name='step', trainable=False)
        self.step_increment = tf.assign(self.step, self.step + 1)

        self.max_step = config.max_step
        self.log_step = config.log_step
        self.model_dir = config.model_dir
        self.load_path = config.load_path

        self.saver = tf.train.Saver()
        self.summary_writer = tf.summary.FileWriter(self.model_dir)
        self.summary_op = tf.summary.merge_all()

        sv = tf.train.Supervisor(logdir=self.model_dir,
                                 is_chief=True,
                                 saver=self.saver,
                                 summary_op=None,
                                 summary_writer=self.summary_writer,
                                 save_model_secs=300,
                                 global_step=self.step,
                                 ready_for_local_init_op=None)

        gpu_options = tf.GPUOptions(allow_growth=True)
        sess_config = tf.ConfigProto(allow_soft_placement=True,
                                     gpu_options=gpu_options)

        self.sess = sv.prepare_or_wait_for_session(config=sess_config)

        self.log_dir = config.sample_dir
        self.midi_writer = MelodyWriter()

    def build_models(self):
        self.x = tf.placeholder(shape=[self.batch_size, MAXIMUM_SEQUENCE_LENGTH, 129, 1], dtype=tf.float32)

        self.G, self.vars_G = MIDINetGenerator(self.batch_size, MAXIMUM_SEQUENCE_LENGTH, 129, reuse=False)
        self.G_test, _      = MIDINetGenerator(1, MAXIMUM_SEQUENCE_LENGTH, 129, reuse=True, is_training=False)

        self.D, self.vars_D = MIDINetDiscriminator(self.x, reuse=False)
        self.D_G, _         = MIDINetDiscriminator(self.G, reuse=True)

        self.D_loss = - tf.reduce_mean( tf.log(self.D) + tf.log(1 - self.D_G) )
        self.G_loss = - tf.reduce_mean( tf.log(self.D_G) )  # - 0.1 * column_distance_loss(self.G)) # as said in https://github.com/soumith/ganhacks
        #tf.summary.scalar("d_loss", self.D_loss)
        #tf.summary.scalar("g_loss", self.G_loss)

        # for batch norm moving average + moving variance
        #update_ops = tf.get_collection(tf.GraphKeys.UPDATE_OPS)
        #with tf.control_dependencies(update_ops):
        self.D_train_step = tf.train.AdamOptimizer(learning_rate=1e-5).minimize(self.D_loss, var_list=[self.vars_D])
        self.G_train_step = tf.train.AdamOptimizer(learning_rate=5e-5).minimize(self.G_loss, var_list=[self.vars_G])

    def train(self):
        for iteration in range(0, self.max_step):
            for _ in range(0, 1):
                fetch_list = [self.summary_op,
                              self.D_train_step,
                              self.D_loss,
                              self.D]
                feed_dict = {self.x : self.data_loader.train_batch(self.batch_size)}
                summary, _, d_loss, D = self.sess.run(fetch_list, feed_dict)

            for _ in range(0, 2):
                fetch_list = [self.summary_op,
                              self.G_train_step,
                              self.G_loss,
                              self.G]
                feed_dict = {}
                summary, _, g_loss, G = self.sess.run(fetch_list, feed_dict)

            self.sess.run(self.step_increment)
            self.summary_writer.add_summary(summary, self.step.eval(session=self.sess))

            if iteration % self.log_step == 0:
                print "G_loss: ", g_loss
                print "D_loss: ", d_loss
                print "--------------------------"

                self.generateTrack(iteration)
                #self.save_output_to_file(self.data_loader.train_batch(1)[0,:,:,0], "test-batch.mid")
                #print G.shape, np.max(G, axis=2)

    def generateTrack(self, iteration):
        feed_dict = {}
        G = self.sess.run(self.G_test, feed_dict)
        self.save_output_to_file(G[0,:,:,0], self.log_dir + '-' + str(iteration) + ".mid")

    def save_output_to_file(self, output, filename):
        melody = Melody()
        for i in range(0, output.shape[0]):
            note = Note(midiPitch=np.argmax(output[i, :]))
            melody.notes.append(note)

        self.midi_writer.writeToFile(filename, melody)

