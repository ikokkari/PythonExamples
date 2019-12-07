import numpy as np

# A handy function to "smooth" progress of time from 0 to 1. Makes a
# lot of graphics and sound nicer and more lifelike.

def ease(t, exp):
    t -= np.floor(t)
    if t < .5:
        return .5 * np.power(2 * t, exp)
    else:
        return 1 - .5 * np.power(2*(1-t), exp)

# A function that is zero everywhere, except in a triangle from s to e.

def blip(t, s, e, m = 1):
    w = (e - s) / 2
    if t <= s or t >= e:
        return 0
    elif t < s + w:
        return m * (t - s) / w
    else:
        return m * (e - t) / w

# Sine wave.

def sinewave(t, f, sf=44100):
    ts = np.linspace(0, t, t * sf, endpoint=False)
    fs = np.sin(2 * np.pi * ts * f)
    return fs

# Sawtooth wave.

def sawtooth(t, tr, sf=44100):
    ts = np.linspace(0, t, t * sf, endpoint=False)
    fs = 2 * (ts / tr - np.floor(ts / tr)) - 1
    return fs

# Mix two sound vectors with the given weights over time.

def mix(s1, s2, sf = 44100, wt = lambda t: 0.5):
    res = np.zeros(max(len(s1), len(s2)))
    for i in range(max(len(s1), len(s2))):
        if i < len(s1):
            f1 = s1[i]
        else:
            f1 = 0
        if i < len(s2):
            f2 = s2[i]
        else:
            f2 = 0
        t = i / sf
        w = wt(t)
        res[i] = w * f1 + (1-w) * f2
    return res

# Add some echo to the sound.

def echo(s, delay = 2000, times = 5):
    res = np.zeros(len(s))
    for i in range(len(s)):
        res[i] = s[i]
        for k in range(1, times + 1):
            j = i - k * delay    
            if j > 0:
                res[i] = res[i] + s[j] * 1 / k
    return res

# from http://nifty.stanford.edu/2017/hug-fractal-sound/

def fractal(t, period, sf = 44100):
    res = np.zeros(int(t * sf))
    state = 0
    for i in range(len(res)):
        state += 1
        weirdstate = state & (state >> 3) & (state >> 8) % period
        res[i] = 2 * weirdstate / period - 1
    return res
        
if __name__ == "__main__":    
    from scipy.io.wavfile import read, write    

    # We can create our own sounds mathematically...
    data = mix(sinewave(10, 300), sawtooth(10, 1 / 100), 
               wt = lambda t: np.sin(np.pi*t))
    data = mix(data, fractal(10, 99), wt = lambda t: 1 - .8 * blip(t, 4, 9, 1))
    scaled = np.int16(data/np.max(np.abs(data)) * 32767)
    write('r1.wav', 44100, scaled)
    
    # ... or read an existing sound from the given wav file.    
    freq, req = read('273050__shadowisp__new-song-request.wav')
    data = echo(req, delay = 8000, times = 10)
    scaled = np.int16(data/np.max(np.abs(data)) * 32767)
    write('r2.wav', 44100, scaled)