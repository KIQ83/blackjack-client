import tensorflow as tf
import tensorflow.contrib.eager as tfe
import os

class Model(object):

	train_dataset = None

	def __init__(self):
		tf.enable_eager_execution()
		self.train_dataset = self.parseCSVFile()

		self.model = tf.keras.Sequential([
			tf.keras.layers.Dense(100, activation="softplus", input_shape=(2,)),  # input shape required
			tf.keras.layers.Dense(100, activation="sigmoid"),
			tf.keras.layers.Dense(1)
		])

		self.train(self.model, self.train_dataset, self.optimizer())


	def parseCSVFile(self, fileName = 'inputs2.csv'):
		#train_dataset_fp = tf.keras.utils.get_file(fname=fileName, origin=None)

		train_dataset = tf.data.TextLineDataset([fileName])
		train_dataset = train_dataset.map(self.parseCSVLine)     # parse each row
		train_dataset = train_dataset.shuffle(buffer_size=1000)  # randomize
		train_dataset = train_dataset.batch(32)

		return train_dataset

	def parseCSVLine(self, line):
		# sets field types
		# example_defaults = [[0.], [0.], [0.], [0.], [0.], [0.], [0.], [0.], [0.], [0.], [0.], [0.], [0.], [0.], [0.], [0.], [0.], [0.], [0.], [0.], [0.], [0.], [0.], [0.], [0.], [0.], [0.], [0.], [0]]
		example_defaults = [[0.], [0.], [0]]
		parsed_line = tf.decode_csv(line, example_defaults)
		# First 4 fields are features, combine into single tensor
		# features = tf.reshape(parsed_line[:-1], shape=(28,))
		features = tf.reshape(parsed_line[:-1], shape=(2,))
		# Last field is the label
		label = tf.reshape(parsed_line[-1], shape=())

		return features, label

	def loss(self, model, x, y):
		y_ = tf.reshape(model(x), shape=y.get_shape())
		return tf.losses.mean_squared_error(labels=y, predictions=y_)

	def grad(self, model, inputs, targets):
		with tfe.GradientTape() as tape:
			loss_value = self.loss(model, inputs, targets)
			#print(str(loss_value))
		return tape.gradient(loss_value, model.variables)

	def optimizer(self):
		return tf.train.GradientDescentOptimizer(learning_rate=0.01)

	def train(self, model, train_dataset, optimizer):
		train_loss_results = []
		train_accuracy_results = []
		num_epochs = 201

		for epoch in range(num_epochs):
			epoch_loss_avg = tfe.metrics.Mean()
			epoch_accuracy = tfe.metrics.Accuracy()

			# Training loop - using batches of 32
			for x, y in tfe.Iterator(train_dataset):
				# Optimize the model
				grads = self.grad(model, x, y)
				optimizer.apply_gradients(zip(grads, model.variables),
				                      global_step=tf.train.get_or_create_global_step())

				# Track progress
				epoch_loss_avg(self.loss(model, x, y))  # add current batch loss
				# compare predicted label to actual label
				epoch_accuracy(tf.argmax(model(x), axis=1, output_type=tf.int32), y)

			# end epoch
			train_loss_results.append(epoch_loss_avg.result())
			train_accuracy_results.append(epoch_accuracy.result())

			print("Epoch {:03d}: Loss: {:.3f}, Accuracy: {:.3%}".format(epoch, epoch_loss_avg.result(), epoch_accuracy.result()))

