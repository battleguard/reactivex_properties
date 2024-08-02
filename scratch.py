class MyClass:
    def __init__(self, value):
        self._value = value

    def get_value(self):
        """The 'value' property."""
        return self._value

    def set_value(self, new_value):
        print(f'property set {new_value=}')
        self._value = new_value

    value = property(get_value, set_value, None, "foo")
    value2_hello_world = property()

# Create an instance of MyClass
obj = MyClass(42)

# Access the property object from the class
property_obj: property = MyClass.value

# Print information about the property
print("Property name:", property_obj.fget.__name__)
print("Docstring:", property_obj.fget.__doc__)
print("Getter function:", property_obj.fget)
print("Setter function:", property_obj.fset)
print("Deleter function:", property_obj.fdel)
print("doc function:", property_obj.__doc__)
print(dir(property_obj))
print(MyClass.value2_hello_world.__doc__)
property_obj.fset(obj, 10)
