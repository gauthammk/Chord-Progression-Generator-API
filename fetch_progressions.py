import requests
import pandas as pd
import json


# read API key from file
def getAPIKey():
    with open('API_Key.txt', 'r') as APIKeyFile:
        APIKey = APIKeyFile.read()
    return APIKey


# mine one chord progressions
def mineOneChordProgressions(baseUri, APIKey):

    # define endpoint
    chordProgressionsEndpoint = baseUri + 'trends/nodes'

    # add API key as a Bearer token for authorization
    headers = {"Authorization": "Bearer " + APIKey}

    # make request
    response = requests.get(chordProgressionsEndpoint, headers=headers)

    # get the response as a json string
    oneChordProgressionsJson = response.text

    # form the dataframe by reading the response as json
    oneChordProgressionsDf = pd.read_json(oneChordProgressionsJson)

    # discard chord progressions with low probabilty(< 0.01) since very few songs have these progressions
    lowProbabilityIndices = oneChordProgressionsDf[oneChordProgressionsDf['probability'] < 0.01].index
    oneChordProgressionsDf.drop(lowProbabilityIndices, inplace=True)
    print(oneChordProgressionsDf)

    # write to file as csv
    oneChordProgressionsDf.to_csv(
        'one_chord_progressions.csv', index=False)


def mineTwoChordProgressions(baseUri, APIKey):

    # define endpoint
    chordProgressionsEndpoint = baseUri + 'trends/nodes?cp='

    # add API key as a Bearer token for authorization
    headers = {"Authorization": "Bearer " + APIKey}

    # define the list to store two chord progressions
    twoChordProgressionsList = []

    # get chord progression paths from file
    oneChordProgressionsDf = pd.read_csv('one_chord_progressions.csv')
    oneChordProgressionPaths = oneChordProgressionsDf['chord_ID'].tolist()

    # loop through each of the chords in the one chord progression file
    for currentChordPath in oneChordProgressionPaths:

        # construct a request endpoint by appending to the chord in the file
        twoChordProgressionsEndpoint = chordProgressionsEndpoint + \
            str(currentChordPath)
        print('Finding: ', twoChordProgressionsEndpoint)
        # get results
        response = requests.get(
            twoChordProgressionsEndpoint, headers=headers)

        # append each two chord progression to the string (after removing the '[]' brackets since we need to build the whole json object in one list)
        twoChordProgressionsList.append(response.text[1:-1])

    # manual transformation into json format
    twoChordProgressionsJson = '[' + ','.join(twoChordProgressionsList) + ']'
    print(twoChordProgressionsJson)

    # form the dataframe by reading the response as json
    twoChordProgressionsDf = pd.read_json(twoChordProgressionsJson)

    # discard chord progressions with low probabilty(< 0.01) since very few songs have these progressions
    lowProbabilityIndices = twoChordProgressionsDf[twoChordProgressionsDf['probability'] < 0.03].index
    twoChordProgressionsDf.drop(lowProbabilityIndices, inplace=True)
    print(twoChordProgressionsDf)

    # write to file as csv
    twoChordProgressionsDf.to_csv('two_chord_progressions.csv', index=False)
    
def mineThreeChordProgressions(baseUri, APIKey):

    # define endpoint
    chordProgressionsEndpoint = baseUri + 'trends/nodes?cp='

    # add API key as a Bearer token for authorization
    headers = {"Authorization": "Bearer " + APIKey}

    # define the list to store three chord progressions
    threeChordProgressionsList = []

    # get chord progression paths from file
    twoChordProgressionsDf = pd.read_csv('two_chord_progressions.csv')
    twoChordProgressionPaths = twoChordProgressionsDf['chord_ID'].tolist()

    # loop through each of the chords in the two chord progression file
    for currentChordPath in twoChordProgressionPaths:

        # construct a request endpoint by appending to the chord in the file
        threeChordProgressionsEndpoint = chordProgressionsEndpoint + \
            str(currentChordPath)
        print('Finding: ', threeChordProgressionsEndpoint)
        # get results
        response = requests.get(
            threeChordProgressionsEndpoint, headers=headers)

        # append each three chord progression to the string (after removing the '[]' brackets since we need to build the whole json object in one list)
        threeChordProgressionsList.append(response.text[1:-1])

    # manual transformation into json format
    threeChordProgressionsJson = '[' + ','.join(threeChordProgressionsList) + ']'
    print(threeChordProgressionsJson)

    # form the dataframe by reading the response as json
    threeChordProgressionsDf = pd.read_json(threeChordProgressionsJson)

    # discard chord progressions with low probabilty(< 0.05) since very few songs have these progressions
    lowProbabilityIndices = threeChordProgressionsDf[threeChordProgressionsDf['probability'] < 0.05].index
    threeChordProgressionsDf.drop(lowProbabilityIndices, inplace=True)
    print(threeChordProgressionsDf)

    # write to file as csv
    threeChordProgressionsDf.to_csv('three_chord_progressions.csv', index=False)


# main runner
baseUri = 'https://api.hooktheory.com/v1/'
APIKey = getAPIKey()
# mineOneChordProgressions(baseUri, APIKey)
# mineTwoChordProgressions(baseUri, APIKey)
mineThreeChordProgressions(baseUri, APIKey)
