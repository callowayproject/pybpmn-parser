# Moddle Integration

1. Parse a Moddle file into a ModdlePackage
2. Convert the ModdlePackage's types into a dataclass
3. Depending on the type:
   - Extend another element
   - Subclass another element into a new element

## How to determine whether to extend, subclass, or add a new element

- If the element has a non-empty `extends` property, it is extending another element
- If the element has a non-empty `superClass` property (other than `Element`), it is subclassing another element
- Otherwise, it is adding a new element

## Extending another element

We can ignore extending other elements. The default behavior is to add additional properties to the element.

## Subclassing another element

- Create a new dataclass that subclasses all the super classes in the `superClass` property, unless it is `Element`
- call the `register_element` method on the new dataclass to register and generate the new class.
