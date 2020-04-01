import tensorflow as tf
from tensorflow.keras.layers import Input, Activation, Dense
from tensorflow.keras import Model

def build_encoder(X_len, enc_dim, bottleneck, activations):
    
    X = Input(shape=(X_len,))
    X_int = Dense(enc_dim)(X)
    X_int = Activation(activations)(X_int)
    Enc = Dense(bottleneck)(X_int)

    encoder = Model(inputs=[X], outputs=[Enc])

    return encoder

def build_decoder(Y_len, dec_dim, bottleneck, activations):
    
    Enc = Input(shape=(bottleneck,))
    Enc_act = Activation(activations)(Enc)
    Y_int = Dense(dec_dim)(Enc_act)
    Y_int = Activation(activations)(Y_int)
    Y = Dense(Y_len)(Y_int)

    decoder = Model(inputs=[Enc], outputs=[Y])
    
    return decoder

def build_encoder_decoder(X_len, Y_len, enc_dim, dec_dim,
                          bottleneck, activations='Linear'):

    encoder = build_encoder(X_len, enc_dim, bottleneck, activations)
    decoder = build_decoder(Y_len, dec_dim, bottleneck, activations)
    Y = decoder(encoder.output)

    model = Model(inputs=encoder.input,
                  outputs=Y)
    return model