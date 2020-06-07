
## UK Postcode Class
#  @summary This class represents the parsed form of a UK postcode.
class Postcode(object):

    def __init__(self):
        self.outward_area = ""
        self.outward_district = ""
        self.inward_sector = ""
        self.inward_unit = ""
        

if __name__ == "__main__":
    #from wintersdeep_postcode import tests
    print(Postcode.BasicRegex)