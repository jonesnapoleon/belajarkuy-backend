import tensorflow as tf

class Checkpoint(tf.keras.callbacks.Callback):
    def __init__(self, filepath):
        super(Checkpoint, self).__init__()
        self.filepath = filepath

    def on_epoch_end(self, epoch, logs={}):
        print('Saving Checkpoint')
        train_acc = logs.get('accuracy')
        val_acc = logs.get('val_accuracy')
        train_f1 = logs.get('f1_score')
        val_f1 = logs.get('val_f1_score')
        self.model.save_weights(f'{self.filepath} (acc_{train_acc:.2f}-val_acc_{val_acc:.2f}-train_f1_{train_f1:.2f}-val_f1_{val_f1:.2f}).h5')