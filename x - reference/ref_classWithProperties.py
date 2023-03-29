class WizCoinException(Exception):
    pass


class ClassWithProperties:
    def __init__(self):
        pass
        self.someAttribute = "some initial value"

    @property
    def someAttribute(self):  # This is the "getter" method.
        return self._someAttribute

    @someAttribute.setter
    def someAttribute(self, value: str):  # This is the "setter" method.
        if not isinstance(value, str):
            raise WizCoinException(
                "someAttribute attr must be set to an str, not a "
                + value.__class__.__qualname__
            )
        self._someAttribute = value

    @someAttribute.deleter
    def someAttribute(self):  # This is the "deleter" method.
        del self._someAttribute


obj = ClassWithProperties()
print(obj.someAttribute)

obj.someAttribute =  "fish"
print(obj.someAttribute)

del obj.someAttribute
