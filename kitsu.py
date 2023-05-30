import requests


class Kitsu:

  def __init__(self, type, _pageLimit):
    self.pageLimit = _pageLimit
    self.baseUrl = "https://kitsu.io/api/edge/{type}?".format(type=type)
    self.headers = {
      "accept": "application/vnd.api+json",
      "content-type": "application/vnd.api+json"
    }

  def urlFilter(self, url, filter, keyword):
    if url[-1] != '?':
      _url = "&"
    else:
      _url = ""

    _url = url + _url + "filter[{filter}]={keyword}".format(filter=filter,
                                                            keyword=keyword)
    return _url

  def urlSort(self, url, *keywords):
    if url[-1] != '?':
      _url = "&"
    else:
      _url = ""

    sorts = ",".join(keywords)

    _url = url + _url + "sort={sorts}".format(sorts=sorts)
    return _url

  def urlPaginate(self, url, offset):
    if url[-1] != '?':
      _url = "&"
    else:
      _url = ""

    _url = url + _url + "page[limit]={limit}&page[offset]={offset}".format(
      limit=self.pageLimit, offset=(int(offset) - 1) * self.pageLimit)
    return _url

  # returns None if invalid url
  def getJson(self, url):
    r = requests.get(url, headers=self.headers).json()
    try:
      return r["data"]
    except KeyError:
      return None

  def toMediaList(self, json):
    return [Media(obj) for obj in json]


class Media:

  def __init__(self, jsonList: dict):
    self.title = jsonList["attributes"]["canonicalTitle"]
    self.type = jsonList["type"]
    self.startDate = jsonList["attributes"]["startDate"]
    self.endDate = jsonList["attributes"]["endDate"]
    self.status = jsonList["attributes"]["status"]
    self.ratingRank = jsonList["attributes"]["ratingRank"]
    self.popularityRank = jsonList["attributes"]["popularityRank"]
    self.averageRating = jsonList["attributes"]["averageRating"]
    self.description = jsonList["attributes"]["description"]
    self.posterImg = jsonList["attributes"]["posterImage"]["large"]

    if self.type == "anime":
      self.episodeCount = jsonList["attributes"]["episodeCount"]
      self.subtype = jsonList["attributes"]["subtype"]
    else:
      self.episodeCount = jsonList["attributes"]["chapterCount"]
      self.subtype = ""

  def getDict(self):
    return vars(self)


class MediaOutput:

  def __init__(self) -> None:
    pass

  def getDetails(self, media: Media):
    output = {
      "Title": media.title,
      "Type": media.type.capitalize() + media.subtype,
      "Episodes/Chapters": media.episodeCount,
      "Status": media.status,
      "Start": media.startDate,
      "End": media.endDate,
      "Rank": media.ratingRank,
      "Popularity": media.popularityRank,
      "Avg. Score": media.averageRating
    }

    return output

  def getDescription(self, media: Media):
    return media.description

  def getImageUrl(self, media: Media):
    return media.posterImg
