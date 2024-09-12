import PointsBetMyko as pb
import grequests

dataNfl = pb.getDataNfl()
pbRequestLinks = pb.makeRequestLinks(dataNfl)
responses = (grequests.get(u['url'], headers=u['headers'])
             for u in pbRequestLinks)
responses = grequests.map(responses)
pb.gigaDump2(responses)
