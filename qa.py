import requests
import re
import dateutil.parser


def search(query):
    """
    Uses the wbsearchentities action to return entities matching a description.

    >>> search("John S. Pistole")[0]['id']
    'Q1701660'
    """

    result = requests.get(
        f"https://www.wikidata.org/w/api.php?action=wbsearchentities&search={query}&language=en&format=json"
    ).json()

    return result["search"]


def get_label(entity):
    """
    >>> get_label("http://www.wikidata.org/entity/Q613726")
    'yottagram'

    >>> get_label("Q613726")
    'yottagram'
    """

    entity = entity.split("/")[-1]

    result = requests.get(
        f"https://www.wikidata.org/w/api.php?action=wbgetentities&ids={entity}&props=labels&languages=en&format=json"
    ).json()

    return result["entities"][entity]["labels"]["en"]["value"]


def get_prop_value(entity, prop):
    """
    >>> get_prop_value("Q193", "P2067")
    '568360 yottagram'
    """
    result = requests.get(
        f"https://www.wikidata.org/w/api.php?action=wbgetentities&ids={entity}&props=claims&language=en&format=json"
    ).json()

    try:
        claim = result["entities"][entity]["claims"][prop][0]["mainsnak"]
    except KeyError:
        return None

    if "amount" in claim["datavalue"]["value"]:
        value = claim["datavalue"]["value"]["amount"].lstrip("+")
    elif "time" in claim["datavalue"]["value"]:
        value = claim["datavalue"]["value"]["time"]
    elif "id" in claim["datavalue"]["value"]:
        value = get_label(claim["datavalue"]["value"]["id"])
    else:
        value = claim["datavalue"]["value"]

    try:
        value += " " + get_label(claim["datavalue"]["value"]["unit"])
    except:
        pass

    return value


def search_prop(query):
    """
    Returns the property matching a query

    >>> search_prop("mass")['id']
    'P2067'
    >>> search_prop("color")['id']
    'P462'
    >>> search_prop("hair color")['id']
    'P1884'
    """
    result = requests.get(
        f"https://www.wikidata.org/w/api.php?action=wbsearchentities&search={query}&type=property&language=en&format=json"
    ).json()

    return result["search"][0]


def answer(question):
    """
    >>> answer("What is the mass of Saturn?")
    'Mass of Saturn (sixth planet from the Sun and the second-largest planet in the Solar System, after Jupiter) is 568360 yottagram.'

    >>> answer("What is the birthdate of Barack H. Obama?")
    'Birthdate of Barack Obama (44th president of the United States) is +1961-08-04T00:00:00Z.'

    >>> answer("What is the official website of Anderson, IN?")
    'Official Website of Anderson (county seat of Madison County, Indiana, United States) is http://www.cityofanderson.com/.'
    """

    pass


if __name__ == "__main__":
    while True:
        print("")
        question = input("Q: ")

        print(answer(question))
