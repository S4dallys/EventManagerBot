from kitsu import Kitsu, Media, MediaOutput

mo = MediaOutput()

def parseUrl(ks: Kitsu, url):
    json = ks.getJson(url)

    if json == None:
        print("Failed")
        raise TypeError
    
    mediaList = ks.toMediaList(json)

    if len(mediaList) != 0:
        return mediaList
    else:
        print("Empty")
        raise TypeError

def getAnimeOrManga(mediaType: str, flags):
    ks = Kitsu(mediaType, 8)
    url = ks.baseUrl
    do_not_sort = False

    if flags.get('keyword') != None:
        url = ks.urlFilter(url, "text", flags.get('keyword').replace("%", "%20"))
        do_not_sort = True

    if flags.get('year') != None:
        url = ks.urlFilter(url, "seasonYear", flags.get('year'))
        do_not_sort = True

    if flags.get('status') != None:
        url = ks.urlFilter(url, "status", flags.get('status'))
        

    if flags.get('subtype') != None:
        url = ks.urlFilter(url, "subtype", flags.get('subtype'))
    
    if flags.get('cat') != None:
        url = ks.urlFilter(url, "categories", flags.get('cat'))


    if flags.get('page') != None:
        url = ks.urlPaginate(url, flags.get('page'))
    else:
        url = ks.urlPaginate(url, "1")
      
    if not do_not_sort:
        url = ks.urlSort(url, "-averageRating")
      

    mediaList = parseUrl(ks, url)

    
    return [
        {"details": mo.getDetails(anime),
         "description": mo.getDescription(anime),
          "image-url":  mo.getImageUrl(anime)} 
          for anime in mediaList]

def getMedia(mediaType: str, offset):
  ks = Kitsu(mediaType, 1)
  url = ks.baseUrl

  url = ks.urlPaginate(url, offset)
  url = ks.urlSort(url, "-averageRating")
    
  media = parseUrl(ks, url)[0]
  
  return {"details": mo.getDetails(media),
       "description": mo.getDescription(media),
        "image-url":  mo.getImageUrl(media)} 







#  note: SORTING BY RATINGRANK DOESN'T WORK IF URL IS FILTERED BY CATEGORY
# url = ks.urlFilter(url, "categories", "romance")
# url = ks.urlSort(url, "popularityRank")
# url = ks.urlPaginate(url, 0)









