class Version(tuple):
	def _as_str_tuple(self):
		return tuple(str(x) for x in self)

	def __str__(self):
		base_version = ".".join(self._as_str_tuple()[:-1])
		if len(self) <= 3:
			return base_version
		else:
			return "-".join(
				(
					base_version,
					self._as_str_tuple()[-1]
				)
			)

	def url(self):
		return "/".join(self._as_str_tuple())
