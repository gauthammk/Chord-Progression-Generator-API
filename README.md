# Chord Progression Generator

**_A handy tool to automatically generate chord progressions based on a selected mood._**

## Dataset creation

> Get an API key from https://www.hooktheory.com

After authentication, run the dataset creation script:

```
python3 fetch_progressions.py
```

The dataset is created by first finding one chord progressions, discarding the progressions with low probability(< 0.0.1), finding two chord progressions from the previously obtained one chord progressions, discarding the low probability ones, and so on.

## Resources

- This project uses the [Hooktheory API](https://www.hooktheory.com/api/trends/docs)
