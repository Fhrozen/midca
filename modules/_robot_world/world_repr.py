from MIDCA import time

class Location:
	
	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z	

class DetectedObject:
	
	'''
	Often an object will be initialized with one ID, and later multiple ids will be 
	discovered to belong to the same object and added to the ids field.
	'''
	
	def __init__(self, *ids):
		self.ids = ids

class DetectionEvent:
	
	'''
	
	'''
	
	def __init__(self, id = None, type = None, loc = None, **kwargs):
		self.time = time.now()
		self.id = id
		self.type = type
		self.loc = loc
	
class SimpleWorld:
	
	'''
	In this simple world representation it is assumed that each object ID designates
	only one object - in other words, cases of misidentification and cases where an
	ID refers to a set of similar objects that cannot be differentiated will not be
	represented.
	Also, generally only the most recent piece of information will be used. This applies
	to type and position info. It is possible to access earlier information using the
	location_history() and sighting_history() methods.
	'''
	
	def __init__(self):
		self.sightings = {}
		self.objectsByID = {}
	
	def sighting(self, detectionEvent):
		id = detectionEvent.id
		#retrieve the object by id. If not found, create a new object with this id.
		if id in self.objectsByID:
			object = self.objectsByID[id]
		else:
			object = new DetectedObject(id)
			self.objectsByID[id] = object
		if object not in self.sightings:
			self.sightings[object] = []
		self.sightings[object].append(detectionEvent)
	
	def get_object(self, objectOrID):
		if not isinstance(objectOrID, DetectedObject):
			try:
				object = self.objectsByID[objectOrID]
			except KeyError:
				return None
		else:
			object = objectOrID
	
	def current_location(self, objectOrID, maxTimeSinceSeen):
		'''
		If the given object or an object with the given ID has been sighted within the 
		last maxTimeSinceSeen at a specific location, will return that location. Otherwise
		will return None.
		'''
		currentTime = time.now()
		object = self.get_object(objectOrID)
		if object and object in sightings:
			for detectionEvent in sightings[object].reverse():
				if detectionEvent.time - currentTime > maxTimeSinceSeen:
					return None #too long since last sighting
				if detectionEvent.loc != None:
					return detectionEvent.loc
			return None
		else:
			return None
	
	def last_sighting(self, objectOrID):
		'''
		Will return the last DetectionEvent for indicated object, if one exists. Else
		returns None.
		'''			
		object = self.get_object(objectOrID)
		if object and object in sightings and sightings[object]:
			return sightings[object][-1]
		return None
	
	def get_type(self, objectOrID):
		'''
		returns the last reported type for the designated object. Returns None if no
		type has been reported.
		'''
		object = self.get_object(objectOrID)
		if object and object in sightings:
			for detectionEvent in sightings[object].reverse():
				if detectionEvent.type:
					return detectionEven.type
		return None
	
	def location_history(self, objectOrID):
		'''
		returns a list of tuples (loc, time) for the locations of the designated object.
		These are ordered by sighting time earliest -> latest. 
		'''
		object = self.get_object(objectOrID)
		if object and object in sightings:
			return [(detectedObject.loc, detectedObject.time) for detectedObject in 
			sightings[object] if detectedObject.loc]
		return []
	
	def sighting_history(self, objectOrID):
		'''
		returns a list DetectionEvents; all those recorded for the designated object.
		'''
		object = self.get_object(objectOrID)
		if object and object in sightings:
			return [detectedObject for detectedObject in sightings[object]]
		return []
