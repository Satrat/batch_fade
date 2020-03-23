import librosa
import numpy as np
import argparse
from os import listdir
from os.path import isfile, isdir, join, exists

def getFadeOutArray(fade_time, sr):
    fade_samples = fade_time / 1000.0 * sr
    print(np.linspace(1.0, 0.0, num=fade_samples))
    return np.linspace(1.0, 0.0, num=fade_samples)

def getFadeInArray(fade_time, sr):
    fade_samples = fade_time / 1000.0 * sr
    print(np.linspace(0.0, 1.0, num=fade_samples))
    return np.linspace(0.0, 1.0, num=fade_samples)

def getFileList(dir):
    if exists(dir) and isdir(dir):
        files = [join(dir, f) for f in listdir(dir) if f.endswith(".wav") and isfile(join(dir, f))]
        return files
    else:
        raise Exception("Folder does not exist!")

def fadeFile(fade_out_array, fade_in_array, data):
    num_fade_samples = len(fade_out_array)
    if num_fade_samples > data.shape[0]:
        raise Exception("file too short to fade!")

    data[-num_fade_samples:] = data[-num_fade_samples:] * fade_out_array
    fade_in = data[:num_fade_samples] * fade_in_array
    data = data[num_fade_samples:]
    data[-num_fade_samples:] += fade_in

    return data
    #fade_in = data[:num_fade_samples] * fade_in_array
    
    #data[-num_fade_samples:] = np.add(fade_in, data[-num_fade_samples:])
    #data = data[num_fade_samples:]

def fadeList(fade_list,fade_out_array, fade_in_array, sr, overwrite):
    for f in fade_list:
        data, _ = librosa.core.load(f, mono=True, sr=sr)
        data = librosa.core.to_mono(data)
        data = fadeFile(fade_out_array, fade_in_array, data)

        if overwrite:
            new_file_path = f
        else:
            new_file_path = f.replace(".wav", "-fo.wav")

        print("writing {}...".format(new_file_path))
        librosa.output.write_wav(new_file_path,data,sr=sr)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Batch logarithmic fade out a folder of wav files.')
    parser.add_argument('path', type=str, help="folder to process")
    parser.add_argument('--r', dest='sr', type=int, default=44100, help="sample rate")
    parser.add_argument('--f', dest='fade_time', type=int, default=500, help="fade out time in ms")
    parser.add_argument('--o', dest='overwrite', type=bool, default=False, help="Whether to overwrite original")
    args = parser.parse_args()

    fade_out_array = getFadeOutArray(args.fade_time, args.sr)
    fade_in_array = getFadeInArray(args.fade_time, args.sr)
    file_list = getFileList(args.path)
    fadeList(file_list,fade_out_array, fade_in_array, args.sr, args.overwrite)