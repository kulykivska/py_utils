class VisitorMeta(type):
    def __init__(cls, name, bases, dct) -> None:
        super().__init__(name, bases, dct)

        attributes = (getattr(cls, attribute_name) for attribute_name in dir(cls))
        methods = (attribute for attribute in attributes if callable(attribute))
        visit_methods = (method for method in methods if hasattr(method, '__visited_classes__'))

        cls.__visit_dispatcher__ = {}

        for visit_method in visit_methods:
            for visited_class in getattr(visit_method, '__visited_classes__'):
                cls.__visit_dispatcher__[visited_class] = visit_method


class Visitor(metaclass=VisitorMeta):
    def visit(self, obj):
        visit_method = self.__visit_dispatcher__[obj.__class__]

        return visit_method(self, obj)


def visit(*cls):
    def wrapper(fn):
        fn.__visited_classes__ = cls
        return fn

    return wrapper


class Visitable:
    def accept(self, visitor: Visitor):
        return visitor.visit(self)
