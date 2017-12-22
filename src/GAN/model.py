import tensorflow as tf
import numpy as np

def conv_layer(x, scope, filters=64, stride=(1,1), kernel_size=(3,3), name=''):
    with tf.variable_scope(scope):
        x = tf.layers.conv2d(x, filters=filters, kernel_size=kernel_size, strides=stride, name=name)
    return x

def batch_norm(scope, x, is_training=True, name=''):
    with tf.variable_scope(scope):
        x = tf.layers.batch_normalization(x, training=is_training, name=name)
    return x


def get_nr_variables(vars):
    tot_nb_params = 0
    for v in vars:
        shape = v.get_shape() # e.g [D,F] or [W,H,C]
        params = 1
        for dim in range(0, len(shape)):
            params *= int(shape[dim])

        tot_nb_params += params

    return tot_nb_params

def deconv2d(input_, output_shape,
             variable_scope,
             height, width,
             stride1, stride2,
             name=''):

    with tf.variable_scope(variable_scope) as vs:
        # filter : [height, width, output_channels, in_channels]
        w = tf.get_variable(name + 'w', [height, width, output_shape[-1], input_.shape[-1]],
                            initializer=tf.random_normal_initializer(stddev=0.02))

        deconv = tf.nn.conv2d_transpose(input_, w, output_shape=output_shape,
                                                strides=[1, stride1, stride2, 1], name=name)

        biases = tf.get_variable(name + 'biases', [output_shape[-1]], initializer=tf.constant_initializer(0.0))
        deconv = tf.reshape(tf.nn.bias_add(deconv, biases), deconv.get_shape())

        return deconv

def MIDINetDiscriminator(x, is_training=True, reuse=False):
    with tf.variable_scope("Discriminator", reuse=reuse) as vs:
        x = conv_layer(x, vs, filters=14, stride=(2,129), kernel_size=(2,129), name='conv-1')
        x = tf.nn.leaky_relu(x, alpha=0.2)
        x = batch_norm(vs, x, is_training, 'd-batch-norm-1')

        x = conv_layer(x, vs, filters=77, stride=(2,2), kernel_size=(4, 1), name='conv-2')
        x = tf.nn.leaky_relu(x, alpha=0.2)
        x = batch_norm(vs, x, is_training, 'd-batch-norm-2')

        x = tf.contrib.layers.flatten(x)
        x = tf.layers.dense(x, 1024, activation=tf.nn.tanh, name='dense-1')
        x = tf.nn.leaky_relu(x, alpha=0.2)
        x = batch_norm(vs, x, is_training, 'd-batch-norm-3')

        x = tf.layers.dense(x, 1, activation=tf.nn.sigmoid, name='output')

    variables = tf.contrib.framework.get_variables(vs)
    print "Discriminator variables:", get_nr_variables(variables)

    return x, variables

def MIDINetGenerator(batch_size, sequence_length, feature_size, reuse=False, is_training=True):

    with tf.variable_scope("Generator", reuse=reuse) as vs:
        x = tf.random_normal(mean=0., stddev=1.0, shape=[batch_size, 100],
                             name='g_noise')  # random gaussian sample of z_dim

        x = tf.layers.dense(x, 1024, name='dense-1')
        x = tf.nn.leaky_relu(x, alpha=0.2)

        x = tf.layers.dense(x, 256+16, name='dense-2')
        x = tf.nn.leaky_relu(x, alpha=0.2)

        x = tf.reshape(x, shape=[batch_size, 16, 17, 1])

        x = deconv2d(x, [batch_size, sequence_length/4, int(np.ceil(feature_size/4.)), 128], vs, 2, 1, 2, 2, 'deconv-1')
        x = tf.nn.leaky_relu(x, alpha=0.2)
        x = batch_norm(vs, x, is_training, 'g-batch-norm-1')

        x = deconv2d(x, [batch_size, sequence_length/2, int(np.ceil(feature_size/2.)), 128], vs, 2, 1, 2, 2, 'deconv-2')
        x = tf.nn.leaky_relu(x, alpha=0.2)
        x = batch_norm(vs, x, is_training, 'g-batch-norm-2')

        x = deconv2d(x, [batch_size, sequence_length, feature_size, 128], vs, 2, 1, 2, 2, 'deconv-3')
        x = tf.nn.leaky_relu(x, alpha=0.2)
        x = batch_norm(vs, x, is_training, 'g-batch-norm-3')

        x = deconv2d(x, [batch_size, sequence_length, 129, 1], vs, 129, 2, 1, 1, 'deconv-4')
        x = tf.nn.softmax(x, dim=2)


        if reuse == False:
            tf.summary.image('generator_image', tf.transpose(x, [0,2,1,3]))

    variables = tf.contrib.framework.get_variables(vs)
    print "Generator variables:", get_nr_variables(variables)

    return x, variables

def MIDINetGeneratorFFNN(batch_size, sequence_length, feature_size, reuse=False):
    with tf.variable_scope("Generator", reuse=reuse) as vs:
        x = tf.random_normal(mean=0., stddev=1.0, shape=[batch_size, 100], name='g_noise')  # random gaussian sample of z_dim

        x = tf.layers.dense(x, 512, name='dense-1')
        x = tf.nn.leaky_relu(x, alpha=0.2)

        x = tf.layers.dense(x, 512, name='dense-2')
        x = tf.nn.leaky_relu(x, alpha=0.2)

        x = tf.layers.dense(x, 512, name='dense-3')
        x = tf.nn.leaky_relu(x, alpha=0.2)

        x = tf.layers.dense(x, sequence_length * 129, activation=tf.nn.sigmoid, name='g_output_layer')
        x = tf.reshape(x, [batch_size, sequence_length, 129, 1])

        x = tf.nn.softmax(100*x, dim=2)

        if reuse == False:
            tf.summary.image('generator_image', x)

    variables = tf.contrib.framework.get_variables(vs)
    print "Generator variables:", get_nr_variables(variables)

    return x, variables

def column_distance_loss(x):
    '''
    Computes the distance of neighbouring columns of the image
    :param x: Tensor of shape [B,H,W,Ch]
    :return: loss
    '''

    # pad the left and right column with 0 values
    x = tf.pad(x, [[0,0], [1,1], [0,0], [0,0]], "CONSTANT", constant_values=0)

    # take all columns except the last one
    # and subtract all columns except the first one
    # this is equal to subtracting all neighbouring columns in an iterative manner
    x = (x[:,0:-2,:,:] - x[:,1:-1,:,:]) ** 2

    # reduce over all dimensions
    loss = tf.reduce_mean(x, axis=3)
    loss = tf.reduce_mean(loss, axis=2)
    loss = tf.reduce_mean(loss, axis=1)

    return loss


