import fileinput
import sys
import re

data = []

#Example lines:
#Dog Lifetime Neutered Male,HOUND MIX,BROWN,BASHFUL,15147,2018,9/10/2015 11:12
#Dog Senior Lifetime Neutered Male,AUS SHEPHERD,MULTI,TUCKER,15237,2018,1/28/2013 10:44
#WHAT THE HELL TINA
#Dog Senior Citizen or Disability Spayed Female,BEAGLE MIX,BROWN,"CHRISTINA ""TINA""",15025,2018,11/27/2017 15:37
#APPARENTLY TUCKER IS A VERY GOOD BOY
#Dog Individual License - FREE,SHEPHERD MIX,BLACK,HUNTER,15146,2018,11/27/2017 12:12
#employee: What is your dog's color?; customer: "bobby'DROP FROM..."; employee: *presses the period key*"
#Dog Senior Citizen or Disability Spayed Female,MIXED,.,ROSIE,15202,2018,11/27/2017 15:37
#customer behind that one is also a programmer; this time with breed:
#Dog Individual Spayed Female,.,BLACK/BROWN,PIPPEN,15044,2018,11/29/2017 8:46
#We call her little taj tables:
#Dog Senior Citizen or Disability Female,POMERANIAN,WHITE/BLACK/BROWN,TAJ'aa,15132,2018,11/27/2017 15:37
#more names for regexp grouble: katy "smoosh", LILY=LULU 
#note: throws away times on expiration year. whatever.
line_pattern = re.compile("([a-zA-Z\ \-]*),([a-zA-Z\-\ \/\.&\(\)]*),([a-zA-Z\-\ \/\.]*),([=a-zA-Z0-9`\-\ &\.\(\){\"\"}\'\/]*),([\d\-]*),([\d\/]*),([^\s]*)")

ln = 0 #line counter for skipping the first line. hack
for line in open("2018_all_unique.csv","r"):
  ln += 1
  if(ln==1): continue
  m = line_pattern.match(line)
  assert m is not None, line
  
  #Note: license type leaks gender info :)
  if('Spayed' in m.group(1)): gender = 'm'
  elif('Neutered' in m.group(1)): gender = 'f'
  else: gender = None

  #LicenseType,Breed,Color,DogName,OwnerZip,ExpYear,ValidDate 
  lineAsDict = {
    'licenseType': m.group(1),
    'sterile': 'Spayed' in m.group(1) or 'Neutered' in m.group(1),
    'gender':  gender,
    'breed': m.group(2),
    'color': m.group(3),
    'name': m.group(4),
    'ownerZip': m.group(5),
    'expYear': m.group(6),
    'validDate': m.group(7)
  }
  data.append(lineAsDict)

#########################
# percent sterile.
########################
sterileCount = 0
for doggo in data:
  if doggo['sterile']: sterileCount += 1
print "%d/%d doggos are spayed or neutered (%f pcnt)" % (sterileCount, len(data), 100*(1.0*sterileCount)/len(data))

####################
# Gender
####################

male = 0
female = 0
idk = 0
for doggo in data:
  if(doggo["gender"] == 'm'): male += 1
  elif(doggo["gender"] == 'f'): female += 1
  else: idk += 1
print male, female, idk

###########################
#### most popular names:
###########################

names = dict()
for doggo in data:
  if(doggo["name"] in names.keys()):
    names[doggo["name"]] += 1
  else:
    names.update({doggo["name"]: 1})
for key, value in sorted(names.iteritems(), key=lambda (k,v): (v,k)):
  print key, value

###########################
#### most popular breeds:
###########################

breeds = dict()
for doggo in data:
  if(doggo["breed"] in breeds.keys()):
    breeds[doggo["breed"]] += 1
  else:
    breeds.update({doggo["breed"]: 1})
for key, value in sorted(breeds.iteritems(), key=lambda (k,v): (v,k)):
  print key, value

