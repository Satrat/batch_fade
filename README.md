# Audio Batch Fade

Batch logarithmic fade out a folder of wav files.

### Depencies
* Numpy
* Librosa 

### To Use
```
python3 batchFade.py
```

```
positional arguments:
  path           folder to process

optional arguments:
  -h, --help     show this help message and exit
  --r SR         sample rate
  --f FADE_TIME  fade out time in ms
  --o OVERWRITE  Whether to overwrite original
  ```
