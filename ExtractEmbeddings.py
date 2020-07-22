from numpy import expand_dims
from keras.models import load_model

model = load_model('C:/Users\ASUS\PycharmProjects\AttendanceSystem\Models/facenet_keras.h5')

def getEmbeddings(facePixels):
    # scale pixel values
    facePixels = facePixels.astype('float32')
    # standardize pixel values across channels (global)
    mean, std = facePixels.mean(), facePixels.std()
    facePixels = (facePixels - mean) / std
    # transform face into one sample
    samples = expand_dims(facePixels, axis=0)
    # make prediction to get embedding
    yhat = model.predict(samples)
    return yhat[0]